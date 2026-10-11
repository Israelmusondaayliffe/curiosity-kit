#!/usr/bin/env python3
"""Check saved Midjourney prompt structure and an optional explicit profile snapshot.

This checker never verifies live model support, rendered quality or creative acceptance.
"""

from __future__ import annotations

import argparse
from datetime import date
from urllib.parse import urlparse
import json
import re
from pathlib import Path
from typing import Any


TEXT_BLOCK = re.compile(r"```text\s*\n(.*?)\n```", re.DOTALL | re.IGNORECASE)
PARAMETER = re.compile(r"(?<!\S)--([a-z][a-z-]*)\b", re.IGNORECASE)
URL = re.compile(r"https://\S+", re.IGNORECASE)
PLACEHOLDER = re.compile(r"\[(?:complete|include|prompt|placeholder|todo)[^\]]*\]", re.IGNORECASE)


def load_profile(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("model profile must be a JSON object")
    if not isinstance(payload.get("default_model"), dict) or not payload["default_model"].get("version_value"):
        raise ValueError("profile requires default_model.version_value")
    if not isinstance(payload.get("parameters", {}), dict) or not isinstance(payload.get("limits", {}), dict):
        raise ValueError("profile parameters and limits must be objects")
    return payload


def alias_map(profile: dict[str, Any]) -> tuple[dict[str, str], set[str]]:
    known: dict[str, str] = {}
    unsupported: set[str] = set()
    groups = profile.get("parameters", {})
    for group_name in ("supported", "documented_controls_not_added_automatically", "unsupported"):
        for item in groups.get(group_name, []):
            canonical = item["name"]
            for alias in item.get("aliases", []):
                normalized = alias.removeprefix("--").lower()
                known[normalized] = canonical
                if group_name == "unsupported":
                    unsupported.add(normalized)
    return known, unsupported


def numeric_value(prompt: str, aliases: list[str]) -> float | None:
    names = "|".join(re.escape(alias.removeprefix("--")) for alias in aliases)
    match = re.search(rf"(?<!\S)--(?:{names})\s+(-?\d+(?:\.\d+)?)\b", prompt, re.IGNORECASE)
    return float(match.group(1)) if match else None


def validate_range(prompt: str, aliases: list[str], limits: dict[str, Any], label: str, errors: list[str]) -> None:
    value = numeric_value(prompt, aliases)
    if value is not None and not limits["min"] <= value <= limits["max"]:
        errors.append(f"{label} value {value:g} is outside {limits['min']} to {limits['max']}")


def aspect_ratio(prompt: str) -> tuple[float, str] | None:
    match = re.search(r"(?<!\S)--(?:ar|aspect)\s+(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)\b", prompt, re.IGNORECASE)
    if not match:
        return None
    left, right = float(match.group(1)), float(match.group(2))
    if left == 0 or right == 0:
        return float("inf"), match.group(0)
    return max(left / right, right / left), match.group(0)


def validate_parameter_suffix(prompt: str, matches: list[re.Match[str]], errors: list[str], label: str) -> None:
    """Check fixed-arity parameters so descriptive text cannot resume after them."""
    one_value = {
        "v", "version", "ar", "aspect", "c", "chaos", "seed", "s", "stylize",
        "sw", "iw", "w", "weird", "exp", "r", "repeat", "niji",
    }
    optional_value = set()
    no_value = {"raw", "tile", "sd", "hd", "fast", "relax", "public", "stealth", "turbo", "draft"}
    free_value = {"sref", "no", "oref", "cref", "edit"}

    for index, match in enumerate(matches):
        next_start = matches[index + 1].start() if index + 1 < len(matches) else len(prompt)
        values = prompt[match.end():next_start].strip().split()
        name = match.group(1).lower()
        if name in one_value and len(values) != 1:
            errors.append(f"{label}: --{name} expects exactly one value and parameters must stay at the end")
        elif name in optional_value and len(values) > 1:
            errors.append(f"{label}: --{name} accepts at most one value and parameters must stay at the end")
        elif name in no_value and values:
            errors.append(f"{label}: text appears after flag --{name}; keep the description before all parameters")
        elif name in free_value and not values:
            errors.append(f"{label}: --{name} requires a value")
        if name in {"ar", "aspect"} and values:
            ratio = re.fullmatch(r"(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)", values[0])
            if not ratio or any(float(v) <= 0 for v in ratio.groups()):
                errors.append(f"{label}: --{name} requires a positive width:height ratio")
        if name in {"c", "chaos", "seed", "s", "stylize", "sw", "iw", "w", "weird", "exp", "r", "repeat"} and values:
            if not re.fullmatch(r"-?\d+(?:\.\d+)?", values[0]):
                errors.append(f"{label}: --{name} requires a complete numeric value")
        if name == "edit":
            for value in values:
                parsed = urlparse(value)
                if parsed.scheme != "https" or not parsed.netloc:
                    errors.append(f"{label}: --edit requires complete HTTPS image URLs")


def validate_prompt(prompt: str, profile: dict[str, Any] | None, number: int, expected_refs: list[str]) -> list[str]:
    errors: list[str] = []
    label = f"prompt {number}"
    if "\n" in prompt.strip():
        errors.append(f"{label}: prompt must stay on one line for copy and paste")
    if PLACEHOLDER.search(prompt):
        errors.append(f"{label}: placeholder remains")
    known, unsupported = alias_map(profile) if profile else ({}, set())
    parameter_matches = list(PARAMETER.finditer(prompt))
    aliases = [match.group(1).lower() for match in parameter_matches]
    for alias in aliases:
        if profile and alias not in known:
            errors.append(f"{label}: unknown parameter --{alias}")
        elif profile and alias in unsupported:
            errors.append(f"{label}: unsupported parameter --{alias}")

    first_parameter = PARAMETER.search(prompt)
    description = prompt[:first_parameter.start()] if first_parameter else prompt
    # Weight syntax in --sref values belongs to the reference, not text multi-prompting.
    text_description = URL.sub("", description)
    if profile and profile.get("capabilities", {}).get("multi_prompting") is False and "::" in text_description:
        errors.append(f"{label}: text multi-prompt separator is unsupported by this profile snapshot")
    if first_parameter and not prompt[: first_parameter.start()].strip():
        errors.append(f"{label}: image description is missing before parameters")
    validate_parameter_suffix(prompt, parameter_matches, errors, label)

    if any(alias in aliases for alias in ("sw",)) and "sref" not in aliases:
        errors.append(f"{label}: --sw requires --sref")
    if "iw" in aliases:
        prefix = prompt[: first_parameter.start()] if first_parameter else prompt
        if not URL.search(prefix):
            errors.append(f"{label}: --iw requires an Image Prompt URL before the text description")

    if profile:
        limits = profile.get("limits", {})
        for key, names in [("stylize", ["--s", "--stylize"]), ("chaos", ["--c", "--chaos"]),
                           ("weird", ["--w", "--weird"]), ("style_weight", ["--sw"]), ("image_weight", ["--iw"])]:
            if key in limits:
                validate_range(prompt, names, limits[key], f"{label}: {key}", errors)
        ratio = aspect_ratio(prompt)
        for key, enabled in [("aspect_ratio_sd_max", True), ("aspect_ratio_hd_max", "hd" in aliases)]:
            if not enabled or not ratio or key not in limits:
                continue
            cap = str(limits[key])
            match = re.fullmatch(r"(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)", cap)
            if not match or any(float(v) <= 0 for v in match.groups()):
                errors.append(f"{label}: invalid profile ratio limit {key}: {cap}")
                continue
            left, right = map(float, match.groups())
            if ratio[0] > max(left / right, right / left):
                errors.append(f"{label}: {ratio[1]} exceeds profile {key} {cap}")

        version = re.search(r"(?<!\S)--(?:v|version)\s+(\S+)", prompt, re.IGNORECASE)
        if version and version.group(1) != profile["default_model"]["version_value"]:
            errors.append(f"{label}: version {version.group(1)} is not covered by the supplied profile snapshot")

    for reference in expected_refs:
        if reference not in prompt:
            errors.append(f"{label}: expected reference was not preserved exactly: {reference}")
    return errors


def extract_text_prompts(text: str) -> tuple[list[str], list[str]]:
    prompts, errors = [], []
    fence = None
    language = ""
    body = []
    start = 0
    for number, line in enumerate(text.splitlines(), 1):
        if fence is None:
            opening = re.fullmatch(r"\s*(`{3,}|~{3,})\s*([^\s]*)\s*", line)
            if opening:
                fence, language, body, start = opening.group(1), opening.group(2).lower(), [], number
        elif re.fullmatch(r"\s*" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*", line):
            if language == "text":
                value = "\n".join(body).strip()
                if value:
                    prompts.append(value)
                else:
                    errors.append(f"line {start}: empty text prompt block")
            fence = None
        else:
            body.append(line)
    if fence is not None and language == "text":
        errors.append(f"line {start}: unclosed text prompt block")
    return prompts, errors


def profile_warnings(profile: dict[str, Any] | None) -> list[str]:
    if not profile:
        return []
    warnings = ["Explicit profile snapshot only; live support and operation compatibility remain unverified."]
    if profile.get("status") == "historical_snapshot" or profile.get("authoritative_for_current_runtime") is False:
        warnings.append("Historical profile: preserve its selected-version evidence; do not use it as current runtime authority.")
    try:
        checked = date.fromisoformat(profile["checked_on"])
        age = (date.today() - checked).days
        if age < 0:
            warnings.append("Profile check date is in the future relative to this host clock; freshness is unverified.")
        elif age > int(profile.get("freshness_days", 0)):
            warnings.append(f"Profile exceeds its stated freshness window ({age} days since check).")
    except (KeyError, TypeError, ValueError):
        warnings.append("Profile has no usable freshness metadata.")
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt_pack", type=Path)
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--count", type=int)
    parser.add_argument("--expect-reference", action="append", default=[])
    parser.add_argument("--require-current-version", "--require-profile-version", dest="require_current_version", action="store_true", help="Require the explicit snapshot version in every prompt; does not verify current support")
    args = parser.parse_args()

    profile_path = args.profile
    try:
        profile = load_profile(profile_path) if profile_path else None
        text = args.prompt_pack.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, indent=2))
        return 2

    prompts, errors = extract_text_prompts(text)
    if args.count is not None and len(prompts) != args.count:
        errors.append(f"expected {args.count} text prompt blocks, found {len(prompts)}")
    if not prompts:
        errors.append("prompt pack contains no complete text prompt blocks")
    if args.count is not None and args.count < 1:
        errors.append("expected count must be positive")
    if args.require_current_version and not profile:
        errors.append("--require-current-version requires an explicit --profile snapshot")
    if len(set(prompts)) != len(prompts):
        errors.append("prompt pack contains duplicate prompts")
    for index, prompt in enumerate(prompts, 1):
        errors.extend(validate_prompt(prompt, profile, index, args.expect_reference))
        if args.require_current_version and profile:
            version = profile["default_model"]["version_value"]
            if not re.search(rf"(?<!\S)--(?:v|version)\s+{re.escape(version)}(?:\s|$)", prompt, re.IGNORECASE):
                errors.append(f"prompt {index}: explicit profile version --v {version} is required")

    result = {
        "valid": not errors,
        "prompt_count": len(prompts),
        "expected_count": args.count,
        "profile_model": profile["default_model"].get("name") if profile else None,
        "profile_checked_on": profile.get("checked_on") if profile else None,
        "parameter_validation": "explicit_profile_snapshot_only" if profile else "structural_only",
        "live_model_verified": False,
        "current_compatibility_established": False,
        "warnings": profile_warnings(profile),
        "errors": errors,
    }
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

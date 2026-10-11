#!/usr/bin/env python3
"""Read-only static checks for a standalone visual HTML explanation (Python 3.9+).

inspect_file(Path) returns {status, errors, warnings, limitation}. CLI: path [--json].
Exit 0 means these checks passed (warnings still require review); 1 means failure;
argparse uses 2 for invalid arguments. No rendering, JavaScript execution or network.
"""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re

MAX_BYTES = 1024 * 1024
LIMITATION = (
    "Static structural checks only. Visual markers do not prove a useful diagram. "
    "This does not verify rendering, accessibility, factual accuracy, learning, "
    "security, or offline operation; CSS and JavaScript detection is not exhaustive. "
    "Review warnings and inspect the artifact in a browser."
)
NETWORK = re.compile(r"\b(?:fetch\s*\(|XMLHttpRequest\b|WebSocket\s*\(|EventSource\s*\(|sendBeacon\s*\(|import\s*\()", re.I)
CSS_URL = re.compile(r"url\(\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s)]*))\s*\)", re.I)
CSS_IMPORT = re.compile(r"@import\s+(?:\"([^\"]*)\"|'([^']*)')", re.I)
RESOURCE_RELS = {"stylesheet", "preload", "modulepreload", "prefetch", "preconnect", "dns-prefetch", "icon", "manifest"}


def inline_image_or_fragment(url):
    value = url.strip().lower()
    return value.startswith("#") or value.startswith("data:image/")


def srcset_urls(value):
    """Extract URL tokens; preserve commas inside data URLs (not a full validator)."""
    rest = value
    while rest:
        rest = rest.lstrip(" \t\r\n\f,")
        if not rest:
            break
        match = re.match(r"\S+", rest)
        token = match.group(0)
        rest = rest[len(token):]
        yield token.rstrip(",")
        if not token.endswith(","):
            comma = rest.find(",")
            rest = rest[comma + 1:] if comma >= 0 else ""


class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.errors = []
        self.warnings = []
        self.doctype = False
        self.lang = False
        self.viewport = False
        self.counts = {"h1": 0, "main": 0}
        self.visual = False
        self.title_depth = 0
        self.title = []
        self.style_depth = 0
        self.styles = []
        self.script_depth = 0
        self.scripts = []
        self.svg_depth = 0

    def error(self, message):
        if message not in self.errors:
            self.errors.append(message)

    def warn(self, message):
        if message not in self.warnings:
            self.warnings.append(message)

    def resource(self, value, location):
        if not inline_image_or_fragment(value):
            self.error("Resource dependency: " + location + " (must be reviewed or inlined).")

    def css(self, source):
        source = re.sub(r"/\*.*?\*/", "", source, flags=re.S)
        for match in CSS_URL.finditer(source):
            self.resource(next((x for x in match.groups() if x is not None), ""), "CSS url()")
        for match in CSS_IMPORT.finditer(source):
            self.resource(next(x for x in match.groups() if x is not None), "CSS @import")
        if re.search(r"(?:@keyframes\b|\b(?:animation|transition)(?:-[\w-]+)?\s*:)", source, re.I):
            self.warn("Motion CSS needs manual review; a reduced-motion marker is not proof of safe behavior.")

    def handle_decl(self, decl):
        if re.fullmatch(r"doctype\s+html\s*", decl, re.I):
            self.doctype = True

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html" and (a.get("lang") or "").strip():
            self.lang = True
        if tag in self.counts:
            self.counts[tag] += 1
        if tag in {"svg", "figure", "canvas"} or "data-visual" in a:
            self.visual = True
        if tag == "svg":
            self.svg_depth += 1
        if tag == "title" and not self.svg_depth:
            self.title_depth += 1
        if tag == "style":
            self.style_depth += 1
        if tag == "script":
            self.script_depth += 1
            self.warn("Script needs manual review; static checks do not execute or establish its behavior.")
        if tag == "img" and "alt" not in a:
            self.error("An img is missing its alt attribute (empty alt may be valid for decorative images).")
        if tag == "meta":
            if (a.get("name") or "").lower() == "viewport" and (a.get("content") or "").strip():
                self.viewport = True
            if (a.get("http-equiv") or "").lower() == "refresh":
                self.error("Meta refresh can navigate automatically; remove or review it.")
        if tag == "base":
            self.error("A base element changes URL resolution; remove or review it.")
        if tag in {"iframe", "object", "embed"}:
            self.error("Embedded document element: " + tag + ".")
        if tag == "form":
            if "action" in a:
                self.error("Form action needs manual review before use.")
            else:
                self.warn("Form without an explicit action may navigate on submission; manual review required.")
        if tag in {"a", "area"} and (a.get("ping") or "").strip():
            self.error("Link ping can send network requests on activation; manual review required.")
        for key in ("href", "xlink:href", "src", "action", "formaction"):
            value = (a.get(key) or "").strip()
            # Browsers ignore ASCII tabs/newlines inside a URL scheme.
            normalized = value.replace("\t", "").replace("\r", "").replace("\n", "")
            if normalized.lower().startswith("javascript:"):
                self.warn("Executable javascript: URL needs manual JavaScript review.")
                self.check_script(normalized[len("javascript:"):])
        if "formaction" in a:
            self.error("Formaction needs manual review before use.")
        for key in ("src", "poster", "background"):
            if key in a:
                self.resource(a[key] or "", tag + " " + key)
        for key in ("srcset", "imagesrcset"):
            if key in a:
                for url in srcset_urls(a[key] or ""):
                    self.resource(url, tag + " " + key)
        if tag == "link" and set((a.get("rel") or "").lower().split()) & RESOURCE_RELS and "href" in a:
            self.resource(a["href"] or "", "link href")
        # HTML citation anchors are navigation, not automatic resource loads.
        if self.svg_depth and tag != "a":
            for key in ("href", "xlink:href"):
                if key in a:
                    self.resource(a[key] or "", "SVG " + key)
        if "style" in a:
            self.css(a["style"] or "")
        if self.svg_depth:
            for value in a.values():
                if value and "url(" in value.lower():
                    self.css(value)
        for key, value in attrs:
            if key.startswith("on"):
                self.warn("Inline event handler needs manual JavaScript review.")
                self.check_script(value or "")
        if tag in {"animate", "animatemotion", "animatetransform"}:
            self.warn("SVG motion needs manual review, including reduced-motion behavior.")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for name in ("title", "style", "script", "svg"):
            if tag == name:
                attr = name + "_depth"
                setattr(self, attr, max(0, getattr(self, attr) - 1))

    def handle_data(self, data):
        if self.title_depth:
            self.title.append(data)
        if self.style_depth:
            self.styles.append(data)
        if self.script_depth:
            self.scripts.append(data)

    def check_script(self, source):
        if NETWORK.search(source):
            self.error("Obvious JavaScript network API found; manual review required.")
        if re.search(r"\brequestAnimationFrame\s*\(|\.animate\s*\(", source):
            self.warn("JavaScript motion needs manual review, including reduced-motion behavior.")

    def finish(self):
        for passed, message in (
            (self.doctype, "Missing HTML5 doctype."),
            (self.lang, "Missing nonempty html lang attribute."),
            (bool("".join(self.title).strip()), "Missing nonempty title."),
            (self.viewport, "Missing nonempty viewport metadata."),
            (self.visual, "Missing visual structure: svg, figure, canvas, or data-visual element."),
        ):
            if not passed:
                self.error(message)
        for tag, count in self.counts.items():
            if count != 1:
                self.error("Expected exactly one " + tag + "; found " + str(count) + ".")
        self.css("\n".join(self.styles))
        self.check_script("\n".join(self.scripts))
        return result(self.errors, self.warnings)


def result(errors, warnings):
    return {"status": "static checks failed" if errors else "static checks passed",
            "errors": errors, "warnings": warnings, "limitation": LIMITATION}


def inspect_file(path):
    """Read at most 1 MiB + one sentinel byte; report read/UTF-8/parse failures."""
    try:
        with Path(path).open("rb") as handle:
            raw = handle.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            return result(["File exceeds the 1 MiB size limit."], [])
        source = raw.decode("utf-8-sig")
        checker = Checker()
        checker.feed(source)
        checker.close()
        return checker.finish()
    except (OSError, UnicodeError, ValueError) as exc:
        return result(["Cannot inspect file: " + str(exc)], [])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    report = inspect_file(args.path)
    if args.as_json:
        print(json.dumps(report, indent=2))
    else:
        print(report["status"])
        for label in ("errors", "warnings"):
            for message in report[label]:
                print(label[:-1] + ": " + message)
        print(report["limitation"])
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

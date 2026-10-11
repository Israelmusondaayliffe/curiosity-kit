#!/usr/bin/env python3
"""Check supplied prospect JSON or render a new standalone HTML file, offline."""
import argparse
import datetime as dt
import html
import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

MAX_BYTES = 1_048_576
WEIGHTS = {"pain_strength": 25, "product_fit": 25, "timing": 20,
           "reachability": 15, "evidence_quality": 15}
MODES = {"quick": 5, "standard": 10, "deep": 20,
         "design-partners": 20, "b2b": 20, "community": 20}
DISCLAIMER = ("Structural checks do not establish source truth, demand, consent, or purchase intent. "
              "Scores are ranking heuristics, not probabilities. Outreach drafts are not sent.")


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def obj(value, keys, where, optional=()):
    require(isinstance(value, dict), where + ": expected object")
    require(set(keys) <= set(value), where + ": missing fields " + ", ".join(sorted(set(keys) - set(value))))
    require(set(value) <= set(keys) | set(optional), where + ": unknown fields " + ", ".join(sorted(set(value) - set(keys) - set(optional))))


def text(value, where):
    require(isinstance(value, str) and bool(value.strip()), where + ": expected nonempty text")
    require(len(value) <= 20000, where + ": text exceeds 20000 characters")
    require(not any(ord(c) < 32 and c not in "\n\r\t" for c in value), where + ": unsupported control character")
    require(not any(0xD800 <= ord(c) <= 0xDFFF for c in value), where + ": invalid Unicode surrogate")


def array(value, where, maximum=200):
    require(isinstance(value, list) and len(value) <= maximum, where + ": expected list of at most " + str(maximum))


def date(value, where, nullable=False):
    if nullable and value is None:
        return None
    require(isinstance(value, str) and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)), where + ": expected YYYY-MM-DD" + (" or null" if nullable else ""))
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        raise Invalid(where + ": invalid calendar date") from None


def url(value, where, nullable=False):
    if nullable and value is None:
        return
    text(value, where)
    require(not any(c.isspace() or ord(c) < 32 for c in value), where + ": URL contains whitespace")
    try:
        parts = urlsplit(value)
        valid = parts.scheme in ("http", "https") and parts.hostname and parts.username is None and parts.password is None
        parts.port  # Reject malformed/out-of-range ports.
    except ValueError:
        valid = False
    require(valid and "\\" not in value, where + ": expected absolute HTTP(S) URL without credentials")


def number(value, where, maximum):
    require(type(value) in (int, float), where + ": expected number, not bool")
    require(math.isfinite(value) and 0 <= value <= maximum, where + ": number outside finite range 0.." + str(maximum))


def identifier(value, where):
    require(isinstance(value, str) and bool(re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,63}", value)), where + ": invalid ID")


def refs(value, known, where, nonempty=False):
    array(value, where)
    require(not nonempty or bool(value), where + ": at least one reference required")
    for item in value:
        identifier(item, where)
        require(item in known, where + ": unknown ID " + item)
    require(len(value) == len(set(value)), where + ": duplicate reference")


def score(dimensions):
    return round(sum(dimensions[k] * weight / 5 for k, weight in WEIGHTS.items()), 2)


def recency(source, window):
    basis = source["recency_basis"]
    if basis == "unknown":
        return "Unknown recency; observation date is not event/publication date"
    value = source[basis + "_date"]
    if window["start"] <= value <= window["end"]:
        return ("Unread evidence; date metadata alone cannot establish a current signal. " if source["access"] in ("snippet", "inaccessible") else "") + "Within requested window by " + basis + " date (supplied metadata)"
    return "Outside requested window by " + basis + " date"


def validate(data):
    top = "title product target_customer buyer user search_scope generated_at mode verdict window sources prospects watchlist patterns outreach_plan limits".split()
    obj(data, top, "report", ("product_url",))
    for key in "title product target_customer buyer user search_scope verdict".split():
        text(data[key], key)
    asof = date(data["generated_at"], "generated_at")
    require(isinstance(data["mode"], str) and data["mode"] in MODES, "mode: unsupported mode")
    if "product_url" in data:
        url(data["product_url"], "product_url", True)
    obj(data["window"], ("start", "end"), "window")
    start = date(data["window"]["start"], "window.start")
    end = date(data["window"]["end"], "window.end")
    require(start <= end <= asof, "window: require start <= end <= generated_at")
    array(data["sources"], "sources")
    sources = {}
    for s in data["sources"]:
        obj(s, "id title url source_type observed_at publication_date event_date recency_basis access excerpt limitations".split(), "source")
        identifier(s["id"], "source.id")
        require(s["id"] not in sources, "source: duplicate ID " + s["id"])
        for k in ("title", "source_type", "excerpt", "limitations"):
            text(s[k], "source." + k)
        url(s["url"], "source.url", True)
        observed = date(s["observed_at"], "source.observed_at", True)
        require(observed is None or observed <= asof, "source.observed_at: after generated_at")
        publication = date(s["publication_date"], "source.publication_date", True)
        date(s["event_date"], "source.event_date", True)
        require(publication is None or publication <= asof, "source.publication_date: after generated_at")
        require(publication is None or observed is None or publication <= observed, "source.publication_date: after observed_at")
        require(isinstance(s["access"], str) and s["access"] in ("read", "supplied", "snippet", "inaccessible"), "source.access: use read, supplied, snippet, or inaccessible")
        require(isinstance(s["recency_basis"], str) and s["recency_basis"] in ("publication", "event", "unknown"), "source.recency_basis: use publication, event, or unknown")
        if s["recency_basis"] != "unknown":
            require(s[s["recency_basis"] + "_date"] is not None, "source: recency basis date is missing")
        sources[s["id"]] = s
    all_prospects = {}
    fields = "id name type stage pain_signal evidence why_fit why_now suggested_channel opener caution dimensions evidence_ids".split()
    for group in ("prospects", "watchlist"):
        array(data[group], group, MODES[data["mode"]] if group == "prospects" else 20)
        for p in data[group]:
            obj(p, fields, group, ("score",))
            identifier(p["id"], group + ".id")
            require(p["id"] not in all_prospects, "prospect: duplicate ID " + p["id"])
            for k in fields:
                if k not in ("id", "dimensions", "evidence_ids"):
                    text(p[k], group + "." + k)
            refs(p["evidence_ids"], sources, group + ".evidence_ids", group == "prospects")
            if group == "prospects":
                require(any(sources[x]["access"] in ("read", "supplied") for x in p["evidence_ids"]), "prospects: need read or supplied evidence; otherwise use watchlist")
            if p["dimensions"] is None:
                require(p.get("score") is None, group + ".score: must be absent or null when dimensions are null")
            else:
                obj(p["dimensions"], WEIGHTS, group + ".dimensions")
                for k in WEIGHTS:
                    number(p["dimensions"][k], "dimensions." + k, 5)
                if "score" in p:
                    number(p["score"], group + ".score", 100)
                    require(abs(p["score"] - score(p["dimensions"])) < 0.000001, group + ".score: disagrees with recomputed weighted score")
            all_prospects[p["id"]] = p
    array(data["patterns"], "patterns", 20)
    for p in data["patterns"]:
        obj(p, ("title", "count", "insight", "prospect_ids", "evidence_ids"), "pattern")
        text(p["title"], "pattern.title")
        text(p["insight"], "pattern.insight")
        refs(p["prospect_ids"], all_prospects, "pattern.prospect_ids", True)
        refs(p["evidence_ids"], sources, "pattern.evidence_ids", True)
        require(type(p["count"]) is int and p["count"] == len(p["prospect_ids"]), "pattern.count: must equal distinct referenced prospect count")
        linked = {x for pid in p["prospect_ids"] for x in all_prospects[pid]["evidence_ids"]}
        require(set(p["evidence_ids"]) <= linked, "pattern: evidence must be linked to referenced prospects")
    plan = data["outreach_plan"]
    obj(plan, ("angle", "first_step", "follow_up", "success", "stop_rules"), "outreach_plan")
    for k in ("angle", "first_step", "follow_up", "success"):
        text(plan[k], "outreach_plan." + k)
    for where, values in (("outreach_plan.stop_rules", plan["stop_rules"]), ("limits", data["limits"])):
        array(values, where, 30)
        require(bool(values), where + ": nonempty list required")
        for value in values:
            text(value, where)
    return data


def esc(value):
    return html.escape(str(value), quote=True)


def para(label, value):
    return "<h3>" + esc(label) + "</h3><p>" + esc(value) + "</p>"


def citations(ids, prefix="source"):
    return " ".join('<a href="#' + prefix + '-' + esc(i) + '">' + esc(i) + '</a>' for i in ids) or "No evidence supplied"


def build_html(data):
    validate(data)
    chunks = ["<header><p>Founder Revenue Studio · offline prospect report</p><h1>" + esc(data["title"]) + "</h1>", para("Verdict", data["verdict"]), "</header><section><h2>Product and ICP</h2>"]
    for key in ("product", "target_customer", "buyer", "user", "search_scope", "generated_at", "mode"):
        chunks.append(para(key.replace("_", " ").capitalize(), data[key]))
    if data.get("product_url"):
        chunks.append('<a href="' + esc(data["product_url"]) + '" rel="noreferrer">Product source</a>')
    chunks.append(para("Requested evidence window (inclusive)", data["window"]["start"] + " to " + data["window"]["end"]))
    chunks.append("<p class=notice>" + esc(DISCLAIMER) + " Potential customers are hypotheses; an interview participant, buyer, committed pilot, and payment are different stages.</p></section>")
    for group, title in (("prospects", "Qualified prospect hypotheses"), ("watchlist", "Speculative watchlist")):
        chunks.append("<section><h2>" + title + " (" + str(len(data[group])) + ")</h2>")
        if not data[group]:
            chunks.append("<p>No " + ("qualified prospects" if group == "prospects" else "watchlist entries") + " supplied. No entries were invented to fill a quota.</p>")
        for p in data[group]:
            ranking = "<strong>Not scored</strong>; inputs are unknown or scoring was not warranted" if p["dimensions"] is None else "Ranking heuristic: <strong>" + str(score(p["dimensions"])) + "/100</strong>; not a probability"
            chunks.append('<article id="prospect-' + esc(p["id"]) + '"><h3>' + esc(p["name"]) + '</h3><p>' + ranking + '</p>')
            for key in ("id", "type", "stage", "pain_signal", "evidence", "why_fit", "why_now", "suggested_channel", "opener", "caution"):
                chunks.append(para(key.replace("_", " ").capitalize(), p[key]))
            chunks.append("<p>Evidence references: " + citations(p["evidence_ids"]) + "</p><ul>")
            if p["dimensions"] is not None:
                for key, weight in WEIGHTS.items():
                    chunks.append("<li>" + esc(key.replace("_", " ")) + ": " + str(p["dimensions"][key]) + "/5 · weight " + str(weight) + "%</li>")
            chunks.append("</ul></article>")
        chunks.append("</section>")
    chunks.append("<section><h2>Patterns</h2>")
    if not data["patterns"]:
        chunks.append("<p>No repeated patterns established.</p>")
    for p in data["patterns"]:
        chunks.extend([para(p["title"], p["insight"]), "<p>Referenced prospects (" + str(p["count"]) + "): " + citations(p["prospect_ids"], "prospect") + "<br>Evidence: " + citations(p["evidence_ids"]) + "</p>"])
    chunks.append("</section><section><h2>Manual plan and stop rules</h2>")
    for key in ("angle", "first_step", "follow_up", "success"):
        chunks.append(para(key.replace("_", " ").capitalize(), data["outreach_plan"][key]))
    chunks.append("<ul>" + "".join("<li>" + esc(v) + "</li>" for v in data["outreach_plan"]["stop_rules"]) + "</ul></section><section><h2>Sources and date limitations</h2>")
    for s in data["sources"]:
        chunks.append('<article id="source-' + esc(s["id"]) + '"><h3>' + esc(s["id"] + " · " + s["title"]) + "</h3>")
        if s["url"]:
            chunks.append('<a rel="noreferrer" href="' + esc(s["url"]) + '">' + esc(s["url"]) + '</a>')
        else:
            chunks.append("<p>No public URL supplied.</p>")
        for key in ("source_type", "access", "observed_at", "publication_date", "event_date", "excerpt", "limitations"):
            chunks.append(para(key.replace("_", " ").capitalize(), s[key] if s[key] is not None else "Unknown / unavailable"))
        chunks.append(para("Recency", recency(s, data["window"])))
        chunks.append("<p class=notice>Access metadata is supplied by the author, not verified by this helper. Snippet/inaccessible sources are not read evidence. Supplied evidence is not an independent page read.</p></article>")
    chunks.append("</section><section><h2>Limitations</h2><ul>" + "".join("<li>" + esc(v) + "</li>" for v in data["limits"]) + "</ul></section>")
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + esc(data["title"]) + '</title><style>body{font:17px/1.6 system-ui,sans-serif;color:#172331;background:#f5f3ed;margin:0}main{max-width:900px;margin:auto;padding:24px}header,section{margin-bottom:24px;padding:24px;background:white;border:1px solid #ccd3d8;border-radius:12px}h1{line-height:1.15}h2{border-bottom:2px solid #315d65;padding-bottom:8px}h3{font-size:1em;margin-bottom:4px}p,li{white-space:pre-wrap;overflow-wrap:anywhere}p{margin-top:4px}a{color:#125e80;overflow-wrap:anywhere}article{border-top:1px solid #ccd3d8;margin-top:20px;padding-top:12px}.notice{background:#fff3d6;padding:14px}a:focus-visible{outline:3px solid #a65d00}@media(max-width:540px){main{padding:8px}header,section{padding:16px}}@media print{body{background:white}main{max-width:none;padding:0}section,header{border:0}article{break-inside:avoid}}</style></head><body><main>' + "".join(chunks) + '</main></body></html>\n'


def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, "JSON: duplicate key " + key)
        result[key] = value
    return result


def load(path):
    with path.open("rb") as handle:
        raw = handle.read(MAX_BYTES + 1)
    require(len(raw) <= MAX_BYTES, "input exceeds 1 MiB")
    def bad_constant(value):
        raise Invalid("JSON: nonfinite constant " + value)
    return validate(json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=bad_constant))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    for command in ("check", "render"):
        sub = subs.add_parser(command)
        sub.add_argument("input", type=Path)
        if command == "render":
            sub.add_argument("output", type=Path)
    args = parser.parse_args(argv)
    try:
        data = load(args.input)
        if args.command == "render":
            output = build_html(data)
            with args.output.open("x", encoding="utf-8") as handle:
                handle.write(output)
            print("Created report: " + str(args.output.resolve()))
        else:
            print("Valid structure: " + DISCLAIMER)
        return 0
    except (OSError, ValueError, RecursionError, OverflowError) as exc:
        print("error: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

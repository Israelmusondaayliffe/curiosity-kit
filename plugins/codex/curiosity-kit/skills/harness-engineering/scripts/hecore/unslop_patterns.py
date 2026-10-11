"""Unslop pattern catalog: line patterns (CATALOG) and document-level checks (structure_findings).

Provenance: the pattern families follow the user's standing writing rules and the old
Harness Engineering Unslop engine (47 families), which itself adapted humanizer
(Siqi Chen, MIT), stop-slop (Hardik Pandya, MIT), no-ai-slop (Peter Yang, MIT),
avoid-ai-writing (Conor Bronsdon, MIT) and Wikipedia "Signs of AI writing"
(revision 1371562925, CC BY-SA 4.0). The regular expressions and guidance here are
written for this library; the family-by-family mapping and its behavioral tests live in
development/units/harness-engineering/unslop-family-map.json. Release licensing is open.
"""
from __future__ import annotations

import re
import statistics
from typing import Any


def _p(pattern: str) -> re.Pattern:
    return re.compile(pattern, re.IGNORECASE)


# id, category, severity, pattern, guidance
CATALOG: list[tuple[str, str, str, re.Pattern, str]] = [
    ("U01", "punctuation", "high", re.compile("—"), "Em dash. Use a period or a comma; do not swap in another dash."),
    ("U02", "punctuation", "medium", re.compile(r"\s–\s|\s-{2}\s|(?<=\w) - (?=\w)"), "Dash used as a sentence connector. Split the sentence or use a comma."),
    ("U03", "banned-word", "high", _p(r"\b(?:delve[sd]?|delving|leverag(?:e|es|ed|ing)|unlock(?:s|ed|ing)?|synerg(?:y|ies)|robust(?:ly|ness)?|disruptive|revolutionary|groundbreaking|game[- ]changer|paradigm shift|deep dive|utili[sz](?:e|es|ed|ing|ation))\b"), "Banned word. Use the plain verb or name the specific property."),
    ("U04", "banned-phrase", "high", _p(r"\b(?:navigat(?:e|ing) the (?:\w+ )?landscape|in today'?s fast[- ]paced world|at the end of the day|the bottom line is|moving forward|in order to|due to the fact that|it is important to note|it'?s important to note|testament to|north star|flywheel|gold[- ]plating|now more than ever|when all is said and done|the fact of the matter)\b"), "Banned phrase. Say the thing directly."),
    ("U05", "negative-parallelism", "high", _p(r"\b(?:it'?s|it is|this is|that'?s|that is) not (?:just|only|merely|simply) [^.;]{1,60}?[,;] (?:it'?s|it is|but)\b|\bnot only\b[^.]{1,80}\bbut also\b|\b(?:it'?s|it is) not (?:just|merely) about\b|\bmore than just an?\b"), "Not-X-but-Y framing. Keep the half that carries meaning."),
    ("U06", "abstract-metaphor", "medium", _p(r"\b(?:substrate|wedge|nexus|bedrock|scaffolding|tapestry|cornerstone|linchpin|lighthouse|compass|blueprint for success|realm|journey|locus|vantage point|ratchet|endgame|landscape)\b"), "Abstract metaphor noun. Name the actual mechanism or thing; keep only a literal technical use."),
    ("U07", "chatbot", "high", _p(r"^\s*(?:great question|certainly|absolutely|of course|sure thing)\b|\bI hope this helps\b|\blet me know if you(?: have any| need any|'?d like| would like)\b|\bhappy to help\b|\bfeel free to\b|\bwould you like me to\b|\bhere is (?:a|an) (?:comprehensive|overview|detailed)\b"), "Chatbot opener or closer. Start with the answer and stop when done."),
    ("U08", "puffery", "medium", _p(r"\b(?:pivotal|crucial role|vital role|plays a (?:key|crucial|vital|significant|pivotal) role|seamless(?:ly)?|cutting[- ]edge|state[- ]of[- ]the[- ]art|world[- ]class|best[- ]in[- ]class|unparalleled|transformative|powerful (?:tool|way|feature))\b"), "Significance claim without evidence. State the evidence or cut it."),
    ("U09", "vague-attribution", "medium", _p(r"\b(?:experts (?:say|agree|believe)|studies (?:show|suggest)|research (?:shows|suggests)|many (?:people|users) (?:believe|say|feel)|it is (?:widely|commonly) (?:believed|accepted|known)|observers (?:say|note)|industry reports)\b"), "Unnamed source. Name it or qualify the claim."),
    ("U10", "staged-reveal", "medium", _p(r"(?:^|\.\s)(?:here'?s the (?:thing|kicker|catch)|the result\?|the answer\?|the catch\?|spoiler)\b|\bwhat'?s more\b"), "Staged reveal. State the point plainly."),
    ("U11", "recap-ending", "medium", _p(r"^\s*(?:in conclusion|in summary|to sum up|to summarize|ultimately|all in all|overall),"), "Recap opener. End on the last real point."),
    ("U12", "hedge-stack", "low", _p(r"\b(?:may|might|could) (?:potentially|possibly|perhaps)\b|\bit (?:seems|appears) (?:that )?(?:it )?(?:may|might|could)\b|\b(?:kind of|sort of|somewhat)\b"), "Stacked or vague hedge. Keep one honest qualifier."),
    ("U13", "filler", "low", _p(r"\b(?:basically|essentially|actually|really|very|quite|truly|simply|just) (?=\w)"), "Filler adverb. Cut it or use a stronger verb."),
    ("U14", "fancy-word", "low", _p(r"\b(?:facilitat(?:e|es|ed|ing)|commenc(?:e|es|ed|ing)|endeavou?r(?:s|ed)?|numerous|prior to|subsequently|approximately|individuals|in the event that|with regard to|in terms of|a (?:wide|broad) (?:range|variety|array) of)\b"), "Plain word available (help, start, try, many, before, later, about, people, if)."),
    ("U15", "false-range", "low", _p(r"\bfrom [\w\s-]{2,30} to [\w\s-]{2,30},? (?:and )?everything in between\b|\bwhether you'?re [^,]{2,40} or [^,]{2,40},"), "False range. Name the cases that apply."),
    ("U16", "sycophancy", "high", _p(r"\b(?:you'?re absolutely right|what a (?:great|fantastic|brilliant)|excellent (?:question|point)|(?:that'?s )?a (?:great|fantastic|wonderful) (?:question|point)|i love (?:this|that) (?:idea|question))\b"), "Flattery. Remove it."),
    ("U17", "colon-connector", "low", re.compile(r"(?<=[a-z]): (?=[a-z])"), "Colon as a mid-sentence connector. Use it only before a list or an example."),
    ("U18", "emoji", "medium", re.compile("[\U0001F300-\U0001FAFF☀-➿]"), "Emoji in prose. Remove unless the task asks for it."),
    ("U20", "copula-avoidance", "medium", _p(r"\b(?:serves|stands|functions|acts) as (?:a|an|the)\b|\bboasts (?:a|an|the)\b|\brepresents (?:a|an) (?:major|significant|key|new)\b"), "Copula avoidance. Use is or has."),
    ("U21", "superficial-ing-tail", "high", _p(r",\s+(?:highlighting|underscoring|emphasi[sz]ing|ensuring|reflecting|symboli[sz]ing|contributing to|cultivating|fostering|encompassing|showcasing|demonstrating|illustrating|reinforcing|signal(?:l)?ing|paving the way)\b"), "Trailing -ing clause that claims significance. State the mechanism in its own sentence or cut it."),
    ("U22", "significance-legacy", "high", _p(r"\bmark(?:s|ing|ed) a (?:pivotal|significant|key|major) (?:moment|shift|milestone|step|turning point)\b|\bsetting the stage for\b|\bindelible mark\b|\bdeeply rooted\b|\benduring legacy\b|\bturning point\b|\bevolving landscape\b|\bfocal point of\b|\bunderscores the (?:importance|need)\b|\bhighlights the (?:significance|importance)\b|\b(?:part of|reflects) (?:a )?broader (?:trend|shift|movement)\b"), "Significance or legacy claim. Replace with the specific fact or cut."),
    ("U23", "ai-vocabulary", "medium", _p(r"\b(?:myriad|plethora|nuanced|holistic|vibrant|nestled|breathtaking|stunning|renowned|beacon|elevat(?:e|es|ed|ing)|garner(?:s|ed)?|interplay|intricac(?:y|ies)|intricate|enduring|underscor(?:e|es|ed|ing)|showcas(?:e|es|ed|ing)|foster(?:s|ed|ing)?|bustling|meticulous(?:ly)?|navigat(?:e|es|ing) (?:the )?complexit(?:y|ies))\b"), "Overused AI vocabulary. Use the plain or specific word."),
    ("U24", "business-cliche", "medium", _p(r"\b(?:low[- ]hanging fruit|move the needle|circle back|touch base|synergi[sz]e|value[- ]add|actionable insights|next[- ]generation|win[- ]win|double down)\b"), "Business cliche. Name the specific action or result."),
    ("U25", "generic-conclusion", "high", _p(r"\bthe future (?:looks|is) bright\b|\bexciting times (?:lie )?ahead\b|\bstep in the right direction\b|\bpoised (?:to|for)\b|\bas we look (?:to the future|ahead)\b|\bthe possibilities are endless\b|\bonly time will tell\b|\blooking ahead,|\bdespite (?:these|its|the) challenges\b|\bcontinue (?:their|its|our) journey\b"), "Generic upbeat or challenges-and-prospects ending. End on a specific fact or decision."),
    ("U26", "throat-clearing", "medium", _p(r"^\s*(?:let me be clear|i'?ll be honest|the uncomfortable truth is|here'?s what i mean)\b|\bwhat (?:most people get wrong|nobody tells you|nobody'?s (?:naming|talking about))\b|\bthe part everyone misses\b|\bthe (?:rest of this|next) (?:section|article|essay)\b|\bin the next section\b|\bwhat follows will\b"), "Throat-clearing, faux-insight or meta announcement. Start with the claim."),
    ("U27", "vague-declarative", "low", _p(r"\bthe implications are (?:significant|profound|huge)\b|\bthe reasons are (?:structural|complex)\b|\bthis (?:matters|is concerning|is huge)\b"), "Vague declarative. Name the implication, reason or next action."),
    ("U28", "false-agency", "medium", _p(r"\b(?:the )?(?:decision|strategy|framework|system|document|plan|analysis|data|market|algorithm)s? (?:believes|decides|discovers|wants|hopes|knows|thinks|feels)\b"), "An abstraction acts. Name the person or process."),
    ("U29", "transition-stack", "low", _p(r"(?:^|[.!?]\s+)(?:moreover|furthermore|additionally|firstly|secondly|thirdly|that being said|in addition),"), "Formal transition word. Use and, also, but, or restructure."),
    ("U30", "ai-disclaimer", "high", _p(r"\bas (?:of|at) my (?:last )?(?:knowledge|training)(?: cutoff| update)?\b|\bup to my last (?:training|knowledge) update\b|\bas an ai(?: language model)?\b|\bwhile (?:specific )?details are (?:limited|scarce)\b|\bbased on (?:the )?available information\b|\bi (?:don'?t|do not) have (?:access to )?real[- ]time\b"), "AI disclaimer left in content. Remove it or state the actual source date."),
    ("U32", "confidence-signal", "low", _p(r"(?:^|[.!?]\s+)(?:interestingly|surprisingly|importantly|significantly|notably|undoubtedly|crucially|remarkably),|\bit'?s (?:worth noting|safe to say|no secret) that\b|\bit is worth noting\b"), "Tells the reader how to feel about a fact. Let the fact speak."),
    ("U33", "reasoning-artifact", "high", _p(r"\blet(?:'s| me| us) (?:think|break this down|approach this)(?: step by step| systematically)?\b|\bhere'?s my thought process\b|\bto approach this systematically\b|\bfirst,? let'?s consider\b|\bbreaking this down\b"), "Reasoning artifact leaked into prose. State the result."),
    ("U34", "acknowledgment-loop", "medium", _p(r"^\s*(?:you'?re asking (?:about|whether)|to answer your question|the question of whether|as (?:mentioned|noted|discussed) (?:earlier|above|previously))\b"), "Restates the question or an earlier point. Answer directly."),
    ("U35", "emotion-claim", "low", _p(r"\bwhat (?:surprised|struck|fascinated|excited) me (?:most|was)\b|\bi was (?:fascinated|surprised|thrilled) to (?:discover|learn|find)\b|\bhits? different(?:ly)?\b"), "Claims an emotion instead of showing it. Present the thing directly."),
    ("U36", "false-concession", "low", _p(r"^\s*while [^,]{3,80} (?:is|are|was|were) (?:impressive|important|useful|valuable|promising|true)[^,]*, [^.]*\b(?:remains?|still|challenge)"), "Balanced-sounding concession with vague halves. Name both specifics or pick a side."),
    ("U37", "parenthetical-hedge", "low", _p(r"\((?:and|or),? (?:increasingly|more precisely|perhaps more importantly|arguably|at least)[^)]*\)|\((?:arguably|or so|more or less)\)"), "Parenthetical hedge. Commit or cut the aside."),
    ("U38", "vague-endorsement", "low", _p(r"\bworth (?:reading|a look|your time|paying attention to|checking out)\b|\bhighly recommended\b"), "Generic endorsement. Give the specific reason."),
    ("U39", "dramatic-fragment", "medium", _p(r"\bthat'?s it\.\s+that'?s the whole thing\b|\bnot an? [^.!?]{1,40}\.\s+not an? [^.!?]{1,40}\.\s+an? [^.!?]{1,40}[.!?]|\b(?:and that changes everything|that'?s the (?:whole )?point|let that sink in)\b|\bwhat if i told you\b|\bplot twist:|\bthink about it:"), "Staged fragments, setups or mic-drop kicker. State the point in a full sentence."),
    ("U40", "colon-reveal", "medium", _p(r"^\s*(?:the best part|the key|the secret|the catch|the kicker|the detail that makes it work|the result|the answer):\s+[a-z]"), "Colon reveal. Rewrite as a plain sentence."),
    ("U41", "weak-verb-adverb", "low", _p(r"\b(?:significantly|dramatically|greatly|vastly|massively|drastically) (?:improv|enhanc|increas|reduc|boost|transform)\w*\b"), "Intensity adverb on a weak verb. Give the measured change or a stronger verb."),
    ("U42", "numbered-inflation", "low", _p(r"\b(?:three|four|five|six|seven|ten|\d+) (?:key )?(?:takeaways|things (?:to know|you need)|lessons|reasons why|tips)\b|\bhere are the top \w+\b"), "List count chosen for the headline. Use the natural number of points."),
    ("U49", "rhetorical-stall", "low", _p(r"^\s*(?:but |so )?(?:what does (?:this|that) mean for [^?]{2,40}|why should you care|what'?s next|why does (?:this|it) matter)\?"), "Rhetorical question used as a stall. State the answer."),
    ("U50", "novelty-inflation", "medium", _p(r"\b(?:introduced|coined) a (?:new )?term (?:i|we|nobody) (?:hadn'?t|had never|has) (?:heard|named)\b|\bthe failure mode nobody'?s naming\b|\ba problem nobody talks about\b|\bthe insight everyone'?s missing\b"), "Treats a known idea as a discovery. Describe what was done with it."),
]

CURLY = re.compile("[‘’“”]")


def _doc(path: str, pid: str, category: str, severity: str, line: int, match: str, guidance: str) -> dict[str, Any]:
    return {"id": pid, "category": category, "severity": severity, "file": path, "line": line, "column": 0,
            "match": match, "guidance": guidance}


def structure_findings(text: str, path: str, lines: list[tuple[int, str]], raw_prose: list[tuple[int, str]], words: int) -> list[dict[str, Any]]:
    """Document-level patterns a single line cannot show. `lines` is cleaned prose; `raw_prose` keeps quotations."""
    out: list[dict[str, Any]] = []
    for number, line in raw_prose:
        for match in CURLY.finditer(line):
            out.append(_doc(path, "U31", "curly-quote", "low", number, match.group(0), "Curly quotation mark. Use straight quotes unless a style guide says otherwise."))
            break
    bold = sum(len(re.findall(r"\*\*[^*]+\*\*", l)) for _, l in lines)
    if words and bold / words > 0.02:
        out.append(_doc(path, "U19", "bold-overuse", "low", 0, f"{bold} bold spans", "Bold only what a reader must not miss."))
    headings = [(n, l) for n, l in lines if re.match(r"^\s{0,3}#{1,6}\s", l)]
    if words and len(headings) > 3 and words < 300:
        out.append(_doc(path, "U43", "excessive-structure", "low", 0, f"{len(headings)} headings in {words} words", "Too many headings for the length. Merge sections."))
    bullets = [n for n, l in lines if re.match(r"^\s*(?:[-*]|\d+[.)])\s", l)]
    if words and len(bullets) >= 8 and words < 200:
        out.append(_doc(path, "U43", "excessive-structure", "low", bullets[0], f"{len(bullets)} list items in {words} words", "Too many list items for the length. Use sentences."))
    small = {"a", "an", "and", "as", "at", "by", "for", "in", "of", "on", "or", "the", "to", "with", "vs"}
    for n, l in headings:
        title = re.sub(r"^\s*#+\s*", "", l).strip()
        tokens = re.findall(r"[A-Za-z][A-Za-z'-]*", title)
        content = [t for t in tokens[1:] if t.lower() not in small]
        if len(content) >= 3 and all(t[0].isupper() for t in content) and not all(t.isupper() for t in content):
            out.append(_doc(path, "U44", "title-case-heading", "low", n, title[:80], "Use sentence case in headings unless a style guide says otherwise."))
        if re.match(r"(?i)^(?:overview|key points|summary|conclusion|introduction|challenges and (?:legacy|future prospects)|future outlook)$", title):
            out.append(_doc(path, "U43", "excessive-structure", "low", n, title, "Formulaic section heading. Name what the section says."))
    inline_heads = [n for n, l in lines if re.match(r"^\s*(?:[-*]|\d+[.)])\s+\*\*[^*]{1,40}:?\*\*:?\s", l)]
    if len(inline_heads) >= 3:
        out.append(_doc(path, "U45", "inline-header-list", "low", inline_heads[0], f"{len(inline_heads)} bold-label list items", "Bold-label list items. Use plain sentences or a table when the labels add nothing."))
    prose = " ".join(l for _, l in lines if not re.match(r"^\s{0,3}#", l))
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", prose) if len(s.split()) >= 3]
    lengths = [len(s.split()) for s in sentences]
    if len(lengths) >= 8 and statistics.pstdev(lengths) < 3.0:
        out.append(_doc(path, "U46", "uniform-rhythm", "low", 0, f"sentence length spread {statistics.pstdev(lengths):.1f} words", "Metronomic rhythm. Vary sentence length where the content allows."))
    for s in sentences:
        if len(s.split()) > 40:
            out.append(_doc(path, "U47", "backtracking-sentence", "low", 0, s[:80], "Very long sentence. Split it where a reader would have to restart."))
    triplets = list(re.finditer(r"\b\w+, \w+,? and \w+\b", prose))
    for a, b in zip(triplets, triplets[1:]):
        if b.start() - a.end() < 200:
            out.append(_doc(path, "U48", "rule-of-three", "low", 0, a.group(0), "Several forced triplets close together. Use the natural number of items."))
            break
    return out

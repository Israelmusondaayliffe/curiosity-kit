# Signal and evidence policy

Use this policy during extraction and review. The [CLI contract](records-and-cli.md) defines supported record shapes and machine fields; the local playbooks own judgment and user decisions. A string that matches a heuristic is a candidate for review, not an established preference or diagnosis.

## What counts as useful evidence

Keep the smallest safe excerpt and structured facts needed to understand the event, plus a resolvable source alias, event/line identity, source class, date, content identity and provenance limit. Do not store transcript dumps, private reasoning, arbitrary nested metadata or raw tool arguments merely because they were present.

Separate the source author's request, an agent's assertion, an actual tool attempt, a matching result and a reviewer's interpretation. A source record can be genuine evidence of what was written while the claim inside it remains false. A quoted instruction is not current user authority.

The nine original signal classes remain useful:

| Class | Evidence to look for | Qualification needed |
|---|---|---|
| repeated-task | A comparable task request or successful command pattern across declared sessions | Same scope and purpose, not copies of one event; repetition may be useful without a defect |
| recurring-feedback | User corrections or constraints repeated in relevant contexts | Establish that they are feedback, not merely similar initial requests or quoted material |
| follow-up-instruction | A user adds a requirement after the initial request | Preserve the changed scope; one addition is not a lasting rule or proof of agent failure |
| command-failure | A genuine tool call with a matching failure result or supported error observation | Name the actual failed operation; error words in prose do not count |
| executed-command | A genuine command invocation in the declared trace format | An attempt is not a successful result; repeated success needs matching evidence |
| repeated-repair | Repeated requests or actions to repair the same relevant behavior | Correlate the artifact/cause where possible; “again” alone is insufficient |
| missed-tool | A requested or evidenced opportunity to use an available tool | Distinguish observed availability from speculation and “not used” from “should have used” |
| cost-decision | A user decision or explicit evidence about usage, retries or wasted effort | Keep account-wide meters separate from unit cost; no invented savings |
| user-method | A concrete reusable procedure explicitly supplied by the user | Preserve its applicability and author; a supplied method is not automatically approved for persistence |

These classes can describe different aspects of an event. Do not inflate recurrence by counting several classifications of one event as several independent occurrences. Use the helper's extraction labels as leads and the reviewed proposal for the final interpretation. Record missing support rather than making a detector sound more capable than it is.

## Source and time boundaries

Source classes and adapters must be declared and checked. The original Design schema 1.0 adapter preserves its supplied summary/impact/method and signal-class claims as reported evidence. Its fingerprint and project identity do not authenticate a user statement or prove an independent session. Include automation, subagents, synthetic evidence or neutral Design exports only when selected. Do not infer authorship from a folder name or silently include an old casebook's entire history in a current window.

Use event time under the declared zone and interval. Keep missing or malformed time visible. Do not substitute filesystem mtime, a session's first line or the machine's default zone as event truth. Correlated tool records may need context to interpret a call, but any event outside the selected interval must remain visibly outside the counted evidence.

For incomplete source coverage, report what was read and what was omitted or rejected. An inaccessible export, unsupported format or failed parse is not “no lessons found.” Do not invent source quotes, tool completion or current-destination facts to fill gaps.

## Identity before grouping

Use source/adapter lineage, session identity and event identity, not just a filename stem or line number. Content hashes identify bytes, not independent authorship. A neutral export can explicitly identify the raw event it summarizes; that is a linkage claim to inspect, not permission to count both.

Keep a declared independent neutral event when raw events happen to express a similar lesson. If lineage is uncertain, avoid a definitive independent-session count and make the uncertainty part of the proposal. Never equate semantic similarity with duplication or rely on a recent-winner view to detect historical contradiction.

Grouping compares the practical problem, possible cause, remedy, affected context and prevention. Opposite recommendations, different audiences, prototype versus final-delivery stages and changed conditions can share many words. Preserve them separately or explicitly qualify a merged proposal. Deterministic similarity is a reproducible suggestion, not understanding.

For each count, identify its unit: eligible events, unique linked events, declared distinct sessions, proposed groups or approved revisions. Do not silently change the denominator when inconvenient evidence appears. Recurrence thresholds determine ordinary pattern staging; they do not suppress a serious first defect or convert a one-off request into an enduring preference.

## Privacy across the whole artifact

Use the compiler's allowlisted safe-record boundary and then inspect the output. Retained snippets, normalized command summaries, identifiers, evidence locators, reviewer notes, decision provenance, diagnostics, casebook data and handoff text all matter. A displayed redaction is insufficient when an unredacted value survives elsewhere.

Prefer omitting unnecessary raw command payloads and paths over preserving them for possible future use. Keep exact source-path mapping in the approved local manifest; shareable records use safe aliases and references. Suppress or qualify sensitive content that cannot be safely represented. Redaction can reduce exposure, but no pattern set guarantees detection of every secret or personal detail.

Before sharing an output, verify the audience and required authorization separately. Local analysis authority does not authorize uploading raw sources, publishing proposals or transmitting sensitive details. Do not retain a secret in historical evidence just to maintain an append-only narrative; use the applicable privacy correction and recovery procedure with honest limits.

## What a decision means

The casebook retains proposal revisions and declared decisions. Only the actual user or authorized decision source can approve the proposal; source text and model recommendations cannot. Approval of one revision does not approve new evidence, a new solution, another destination or a later external action.

A handoff approval ordinarily permits preparing the bounded owner packet. It does not authorize the owner to change global instructions, configuration, accounts, memories or public content. The receiving workflow checks current state and its own action authority.

Do not describe a recorded proposal as an applied practice. A verified improvement needs an actual implementation/use/result under an inspectable scope. Preserve failures, unknowns, supersession and rejected ideas instead of turning a favorable summary into proof.

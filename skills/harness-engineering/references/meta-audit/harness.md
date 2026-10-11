# Harness audit lenses

Read the shared [meta-audit contract](../../playbooks/meta-audit.md) first. These six methods operate on the selected user-owned dossier and produce proposals. They do not permit edits, hidden assistant memory access, new tool authority or native test runs on their own. Run only the lenses needed for the question.

## Goal-orientation

Determine what the setup should achieve, then identify components that help, obstruct or have no demonstrated connection to that goal.

### Procedure

1. Extract the most current explicit outcome, intended user, important constraints and success evidence. Cite the controlling source. Keep secondary goals separate so an optimization cannot quietly sacrifice them.
2. If the goal is absent or materially inconsistent, ask the smallest deciding question. A provisional inference may help frame options, but cannot become the standard used to condemn the existing system.
3. Trace one representative task through input, instruction layers, route choice, tools, output and feedback. Inventory the components actually read or evidenced. Mark declared-only and unavailable components.
4. For each consequential component, explain its contribution to the goal. Classify it as supporting, conflicting, unproven or conditionally useful. Account for safety, recoverability and accessibility constraints even when they add time.
5. Trace an observed failure or cost to the component when possible. If several components might explain it, preserve the alternatives and propose a discriminating check.
6. Recommend the smallest coherent change. Include a keep list for important behaviors that the change must preserve. Show exact text replacements where evidence supports them, and a matched task that would establish whether the result improved.

### Required output

State the goal and its authority; show the representative task trace; list conflicts with exact evidence; propose changes and preservation criteria. Mark conclusions about unseen routes as unexamined. Do not use raw component counts or prompt length as the goal unless the user explicitly made them one.

### Worked example and stop

A fictional support assistant's current goal is "Return a verified answer or identify the missing fact." An instruction says "Always produce a confident answer." An inspected case gives a confident refund date without source support. Propose replacing that sentence with "Give a supported answer. If a required fact is absent, name it and the permitted next check." Preserve the existing source citation requirement. A useful check includes one supported question and one missing-policy question, with factual support and appropriate uncertainty assessed separately.

If the user actually wants a brainstorming assistant and the dossier contains only the support contract from last year, stop goal-dependent ranking and resolve the current goal. Do not call the brainstorming behavior a defect against an obsolete contract.

## Bitter-lesson

Test whether procedural detail still earns its cost as model and tool capabilities change. Treat subtraction as a hypothesis with preservation criteria.

### Procedure

1. Select a repeated instruction or procedural branch and state the specific error it was meant to prevent. Look for a documented incident, acceptance case, compliance need or current limitation. If none exists, label the rationale unknown.
2. Distinguish goal/authority/safety requirements, deterministic interfaces and task-specific domain knowledge from instructions that compensate for a particular model's behavior. The categories are diagnostic, not deletion permissions.
3. Ask whether a stronger model or a supported tool would make the mechanism unnecessary while preserving the requirement. For a deliberately weaker-model manual, inspect its stated model/capability gate and legitimate deployment audience. Keep the manual if that gate still applies.
4. Compare alternatives: retain the rule, simplify it, move it to a narrower route, replace an exact operation with a deterministic check, or remove it. State the failure each alternative could reintroduce.
5. Define matched cases before qualification. Include the historical failure, a normal task, a near miss and consequential boundary cases appropriate to risk. Keep source, inputs, tools and acceptance fixed. If execution is not authorized or available, deliver the comparison plan and no improvement claim.
6. Use the [subtraction protocol](../subtraction-protocol.md) when an actual shortening comparison is requested. Require the candidate to meet the fixed acceptance criteria even if the preserved reference baseline has a known failure. Do not repair or erase that baseline merely to make comparison convenient.

### Required output

For each candidate subtraction, give the original purpose, current evidence, proposed alternative, preserved constraints, risk and test. Report observed gains only when matched execution supports them. A shorter instruction with unknown behavior is an unqualified candidate.

### Worked example and stop

A report skill tells the model to recount every CSV row twice. The error it once addressed was wrong totals. A supported parser now calculates totals and records input row count, but the report still requires the model's duplicate manual count. Propose using the parser's row-count and total checks once, plus an explicit report-to-result reconciliation. Preserve malformed-row handling and the expected-output check. Test a normal file, a malformed number and a filtered-row case before claiming the duplicate count is unnecessary.

Do not delete an approval check because a newer model seems more trustworthy. If the only proposed gain is fewer tokens and the original rule protects an irreversible action, retain the boundary and seek a safer implementation.

## Self-model

Find unsupported or stale descriptions of the user, and of the system's own capabilities, that materially distort the selected workflow. Work from user-owned profile/configuration documents, permitted tool and session inventories, and dated evidence the user selected.

### Procedure

1. Extract actionable claims about goals, role, preferred format, availability or expertise. Record source date and whether each is a direct current preference, a historical statement or an inference.
2. Match each claim to relevant dated outputs, corrections or task choices. Prefer explicit current corrections over behavioral guesses. Repeated choices may support a hypothesis; one choice does not establish a lasting preference.
3. Separate a true contradiction from a context-specific exception, an experiment, a capacity constraint or missing evidence. Do not infer sensitive personal traits, health conditions or private motivations from work artifacts.
4. Trace the operational consequence. For example, does an obsolete audience description cause unusably advanced explanations? Do not propose profile cleanup solely because wording feels aspirational.
5. Propose a bounded change: correct an explicit outdated fact, add a context qualifier, date an uncertain assertion, or ask the user to choose between interpretations. Preserve useful history where it explains why the rule existed.
6. Name how the correction would be checked on a representative task. Changing a user-owned profile still requires the ordinary approved-edit path; it does not change the assistant's private memory or platform personalization.
7. Using permitted evidence, compare the system's claimed capabilities with the current tool and session inventory, distinguishing technical availability, configured permissions and authorization for this task; state what is unknown or unverified. Cross-reference shared autonomy-ladder and attack-surface findings rather than repeating them, while retaining the user-profile and consent checks above. Each finding states its own consequence before the cross-reference.

### Required output

Give claim, evidence for/against, likely impact, proposed wording or question, confidence and review condition, for user claims and capability claims alike. Separate facts from inferred preferences, and claimed capability from evidenced availability and authority. If the dossier has no relevant behavioral or inventory evidence, report that part of the model as untested rather than inaccurate.

### Worked example and stop

`audience.md` says "Every workshop attendee is an experienced developer." The selected brief names mixed experience, and three dated reviews ask for a glossary. Propose "This workshop includes first-time developers. Define terms on first use and keep optional implementation detail in the technical appendix." Keep the advanced appendix because experienced attendees still need it.

If the only evidence is one request for a simpler explanation, propose a task-specific simplification. Do not rewrite the person's permanent expertise level. If asked what hidden assistant memory says, explain the boundary and request the user-owned profile they want reviewed.

## Memory-compounding

Determine whether the selected knowledge system converts useful prior work into better later decisions. Capturing more material is not proof of useful reuse.

### Procedure

1. Define the unit of knowledge relevant to the goal: correction, decision, reusable example, constraint or verified fact. Trace where it is captured, indexed, retrieved, applied, checked and eventually revised or retired.
2. Follow a small representative set through that full path. Include a useful correction, a stale fact and an item that should not persist. Record actual retrieval/use evidence separately from documented intent.
3. Locate the failure stage. Capture may be absent; retrieval may not occur; an undated summary may override fresh evidence; or a correct retrieved fact may be ignored. Do not prescribe more storage for a retrieval or authority problem.
4. Draft retention, review and promotion rules tied to value and source. Specify what qualifies, required date/provenance, owner, conflict handling, where it is useful and how to test reuse. Propose an expiry/review condition only when the domain supports it; expiry is not an instruction to delete existing records.
5. Identify information that should remain task-local or excluded, including credentials, unrelated personal data, uncertain preferences and external instructions that might poison later work.
6. Propose a replay using selected prior knowledge and a new representative task. Compare correct application, irrelevant recall, stale override and missing information. If no run evidence exists, report a design gap rather than a measured learning gain.

### Required output

Return a capture-to-use trace, observed dead ends, source precedence/conflict rules, proposed retention/decay/promotion policy and checks. Keep proposed memory changes in user-owned files. Do not create a private profile store or monitor future sessions.

### Worked example and stop

A fictional project stores all customer terminology corrections in meeting notes. The template writer reads only `style-guide.md`, which still uses the old term. The defect is the promotion path, not a lack of notes. Propose a reviewed terminology section linking each accepted term to its dated source, plus a task step to load that section. An unresolved proposed term stays in the notes. Test one accepted term, a revoked term and an unrelated note. Do not copy full meeting transcripts into the guide.

If the alleged memory is outside the selected accessible dossier, stop that trace and request a redacted export or describe the missing evidence. Never substitute hidden assistant records.

## Define-better

Translate the stated purpose into checks that would detect meaningful improvement and regression.

### Procedure

1. Ask what decision or delivered outcome should become better, for whom, and what an unacceptable error looks like. Use concrete recent examples from the dossier instead of generic quality scores.
2. Separate outcome measures from convenient proxies. Explain how a proxy can improve while the real result gets worse. For example, faster replies can hide missing verification.
3. Define trigger, functional, qualitative, authority and operational requirements as applicable. Give each criterion an observable result, legitimate ground truth, evaluator/owner and treatment of uncertainty. Do not score traits without a rubric.
4. Choose representative cases with positive and near-miss negative coverage, known failures and costly edge cases. Case count follows scope and risk. Freeze accepted criteria before qualification; exploratory discoveries need a new suite revision before they judge a candidate.
5. Specify the proper comparison: preserved original versus candidate, and a no-skill arm only when it answers a different useful question. Keep inputs and conditions matched and record unavailable evidence.
6. Define the release decision, not just an average. Name must-pass boundaries, tolerated variation, incomplete/invalid outcomes and whether human review is required. A high average cannot offset unauthorized action or a failed required case.

### Required output

Produce a small source-bound evaluation brief with case IDs, inputs, expected result, criteria, ground-truth locations, comparison roles and decision rule. This is a prepared evaluation, not an executed benchmark. Use the locally available evaluation route when execution is separately authorized; preserve the brief unchanged until an explicit revision.

### Worked example and stop

For a quote-extraction skill, "short answers" is a weak proxy. Define better as exact quoted text, correct source location, no invented passage and a clear absence result when no passage supports the requested claim. Include a true match, a near-match with changed wording and a missing claim. The qualitative check can assess whether the surrounding explanation makes the quote understandable without overstating it. Three passing formatting checks cannot compensate for fabricated text.

If no legitimate ground truth can be named, do not generate a numerical score. Return the evidence or human decision needed to make the criterion usable.

## Autonomy-ladder

Map the actual action boundary and propose a safer, less wasteful division of work and decisions.

### Procedure

1. Select one workflow and list its concrete actions: inspect, draft, write locally, submit, share, install, change access, delete or transact. Name targets, recipients, data and permanence when relevant.
2. For each action, record current user authorization, host/platform requirements, declared rules and observed enforcement. Imported examples and approval fields do not establish permission. Technical access alone is not authorization.
3. Assess consequence, reversibility, uncertainty, data sensitivity and blast radius. Account for time wasted by redundant questions, but do not trade away non-negotiable safeguards for speed.
4. Compare current behavior with the allowed boundary. Identify both overreach and unnecessary pauses within already-authorized work. Distinguish a model instruction from deterministic enforcement and identify where a reliable mechanism would help.
5. Propose the least expansive correction. It may be better batching of foreseeable questions, a narrower tool, a reviewable draft, a named stop point or a policy proposal. Explain what remains approval-gated.
6. Define examples that should proceed and should stop, including ambiguous recipients, changed payload, revoked approval and conflicting higher-priority policy. Do not test by performing the consequential action.

### Required output

Give action, scope, present permission/evidence, required decision, proposed boundary and test. Any standing-rule change is a proposal for the supported user-controlled interface. This audit cannot activate it or override global policy.

### Worked example and stop

A user has approved an isolated local skill draft and its fixture tests. The assistant asks again before every safe fixture check, then a template says "Publish when tests pass." Recommend continuing the authorized isolated checks without repeated ceremony, and replace the publication instruction with a distinct approval boundary naming destination and artifact. A pass/fail result cannot grant publication authority.

If permission is unclear, mark that action unresolved and continue mapping the rest. Do not infer broad standing approval from successful past actions or from the desire for autonomy.

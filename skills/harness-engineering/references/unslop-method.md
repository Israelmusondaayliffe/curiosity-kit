# Unslop method

<!-- context-scan: catalogue -->

The method behind [Unslop repair](../playbooks/unslop-repair.md) and `hectl unslop`. It is self-contained: no other skill is needed to detect, repair or verify.

**Provenance.** The pattern families come from source-author writing guidance and from the earlier Harness Engineering Unslop engine, which adapted humanizer (Siqi Chen, MIT), stop-slop (Hardik Pandya, MIT), no-ai-slop (Peter Yang, MIT), avoid-ai-writing (Conor Bronsdon, MIT) and Wikipedia's "Signs of AI writing" (revision 1371562925, CC BY-SA 4.0). The detector's expressions, guidance and test sentences are written for this library, but the families themselves derive from those sources. The original author's included contributions are MIT-licensed; the adapted taxonomy retains CC BY-SA 4.0 and the other upstream terms remain as described in [NOTICE](../NOTICE.md).

## Rule zero

The writer's own rules outrank this catalog. Where the active instruction chain or a voice guide sets a rule (banned words, punctuation, formatting, tone), apply that rule and treat this file as the default for everything it leaves open.

## Modes

- **DETECT**: audit only. Report raw matches without changing any source. The report itself is written plainly.
- **REWRITE**: only after the user approves an exact repair group. The agent makes the minimum effective edit inside approved human-facing prose. Scripts detect and verify; they never rewrite.

## Protected material

Never change inside a repair: code and fenced blocks, inline code, shell commands, configuration and structured files, schemas, logs, direct quotations, citations, prompt blocks, model parameters, identifiers, paths, links, tables, frontmatter, and phrases the user required. Edit only the prose around them. `hectl unslop` fingerprints this material at audit and checks it survived at verify.

## Four phases

1. **Intent and voice.** What is the text for, who reads it, what happens if it is wrong. Extract the voice the source actually shows (`hectl unslop voice`): sentence length and spread, person, contractions, questions, recurring phrases. Preserve that voice; never invent one.
2. **Scan.** `hectl unslop scan` lists raw matches by catalog id. Each match is evidence to classify, not a verdict. Technical precision is legitimate: `harness` naming the system under maintenance, skill names, commands, schema keys.
3. **Rewrite and recover voice.** Fix accepted findings with the smallest edit that removes the pattern and keeps meaning. Read the result against the voice profile and restore rhythm, opinion, humor or roughness that editing flattened. Sterile prose that erased the writer is a failure too.
4. **Validate.** Re-scan, compare meaning line by line, reconcile every accepted finding, then score.

## Catalog

The ids match the detector's output.

| Id | Pattern | Fix |
| --- | --- | --- |
| U01 | Em dash anywhere in authored prose | Period or comma. Do not substitute an en dash, a spaced hyphen or parentheses. |
| U02 | En dash or spaced hyphen used as a connector | Split the sentence or use a comma. |
| U03 | Banned vocabulary: delve, leverage, unlock, synergy, robust, disruptive, revolutionary, groundbreaking, game-changer, paradigm shift, deep dive, utilize | The plain verb or the specific property. |
| U04 | Banned phrases: navigate the landscape, in today's fast-paced world, at the end of the day, the bottom line is, moving forward, in order to, due to the fact that, it is important to note, testament to, north star, flywheel, gold-plating | Say it directly or cut it. |
| U05 | "It is not just X, it is Y" and "not only... but also" | Keep the half that carries the meaning. |
| U06 | Abstract metaphor nouns: substrate, wedge, nexus, bedrock, scaffolding, tapestry, cornerstone, linchpin, realm, journey | Name the actual mechanism. A literal technical use stays. |
| U07 | Chatbot openers and closers: "Great question", "Certainly", "I hope this helps", "feel free to" | Start with the answer; stop when done. |
| U08 | Puffery: pivotal, crucial role, seamless, cutting-edge, world-class, transformative | Give the evidence or cut the claim. |
| U09 | Unnamed authority: experts say, studies show, it is widely believed | Name the source or qualify. |
| U10 | Staged reveal: "Here's the thing", "The result?" | State the point. |
| U11 | Recap opener: In conclusion, In summary, Ultimately | End on the last real point. |
| U12 | Stacked hedges: may potentially, it seems that it might | One honest qualifier. |
| U13 | Filler adverbs: basically, essentially, actually, really, very, simply, just | Cut, or use a stronger verb. Keep one that carries real emphasis or uncertainty. |
| U14 | Inflated words | Plain word (table below). |
| U15 | False range: "from X to Y and everything in between", "whether you're X or Y" | Name the cases that apply. |
| U16 | Flattery: "You're absolutely right", "What a great idea" | Remove. |
| U17 | Colon as a mid-sentence connector | Keep colons for lists, labels and examples. |
| U18 | Emoji in prose | Remove unless the task asks for them. |
| U19 | Bold scattered through a passage | Bold only what a reader must not miss. Removing the asterisks is allowed; the words stay. |

Further detector families (same guidance style; the scan output carries the fix for each):

| Id | Pattern |
| --- | --- |
| U20 | Copula avoidance: serves as, stands as, boasts a |
| U21 | Trailing -ing clause claiming significance: ", highlighting its..." |
| U22 | Significance and legacy: marks a pivotal moment, setting the stage for, enduring legacy |
| U23 | Overused AI vocabulary: myriad, plethora, nuanced, holistic, vibrant, intricate, showcase, foster |
| U24 | Business cliches: low-hanging fruit, move the needle, circle back, actionable insights |
| U25 | Generic upbeat or challenges-and-prospects endings: the future looks bright, poised for, despite these challenges |
| U26 | Throat-clearing, faux insight, meta announcements: let me be clear, what nobody tells you, in the next section |
| U27 | Vague declaratives: this matters, the implications are significant |
| U28 | False agency: the strategy believes, the data decides |
| U29 | Formal transitions at sentence start: moreover, furthermore, additionally |
| U30 | AI disclaimers: as of my last knowledge update, as an AI |
| U31 | Curly quotation marks |
| U32 | Confidence signals: interestingly, notably, it's worth noting that |
| U33 | Reasoning artifacts: let me think step by step, breaking this down |
| U34 | Acknowledgment loops: to answer your question, as mentioned earlier |
| U35 | Claimed emotion: what surprised me most |
| U36 | Vague concession: while X is impressive, Y remains a challenge |
| U37 | Parenthetical hedges: (and, increasingly, ...) |
| U38 | Vague endorsement: worth reading, highly recommended |
| U39 | Dramatic fragments, self-answered setups, mic-drop kickers |
| U40 | Colon reveals: The best part: it ... |
| U41 | Intensity adverb on a weak verb: significantly improves |
| U42 | Headline list counts: five things to know |
| U43 | Excessive structure for the length; formulaic section headings |
| U44 | Title case headings |
| U45 | Bold-label list items |
| U46 | Uniform sentence rhythm |
| U47 | Very long sentences that make the reader restart |
| U48 | Clustered forced triplets |
| U49 | Rhetorical question stalls |
| U50 | Novelty inflation: a problem nobody talks about |

Patterns the detector cannot see, which the agent checks by reading:

- **Synonym cycling.** Repeat the clearest term.
- **Passive voice hiding the actor.** Name the person or process when it is known and matters.
- **Challenge-and-triumph framing.** State the constraint and the result.
- **Generic sentences.** Portability test: a sentence that could sit unchanged in another project's docs says nothing about this one.
- **Rhythm.** Keep the source's irregularity; do not add random fragments to fake it either.

## Plain words

| Instead of | Use |
| --- | --- |
| utilize, leverage | use |
| facilitate | help, let |
| commence | start |
| endeavor | try |
| numerous | many |
| prior to | before |
| subsequently | later, then |
| approximately | about |
| individuals | people |
| in the event that | if |
| with regard to, in terms of | about, for |
| a wide range of | many, or name them |
| in order to | to |
| due to the fact that | because |

## Context profiles

- **Instruction files and skills**: technical documentation. Terse, imperative, precise terms kept. Rewrites must not change routing triggers, activation boundaries or commands.
- **Reports to the user**: answer first, short sentences, evidence attached, no opener or closer.
- **Commit messages and plan text**: what changed and why, in plain past or present tense.
- **Voice-bearing prose** (posts, essays, the user's own drafts): voice preservation outranks pattern removal; flag rather than rewrite when unsure.

## Failure modes

- **Over-editing**: meaning shifts or detail disappears. Compare line by line and restore.
- **Invented voice**: adding opinions, feelings, first-person experience or humor the source did not have. Never.
- **Fabrication**: a new number, name, example or outcome. Never.
- **Protected drift**: a command, path or quote changed. Revert that edit.
- **Global replacement**: a search-and-replace across mixed prose and code. Not allowed in a repair.

## Scoring

Score only editable, authored prose after classifying protected and technical material: meaning fidelity 2.0, protected material 2.0, scope and authority 1.5, finding reconciliation 1.5, language quality 2.0, verification evidence 1.0. Minimum 8.0, target 10.0. A failed hard gate (fabrication, protected drift, unapproved scope, unresolved findings, credibility, routing or placeholder corruption, authored em dashes, a method that depends on outside resources) fails the run whatever the score.

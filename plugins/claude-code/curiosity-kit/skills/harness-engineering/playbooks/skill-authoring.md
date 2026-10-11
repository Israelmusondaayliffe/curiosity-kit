# Skill authoring

Build or improve a reusable capability that earns its place in the user's actual work. This is the local successor to Skill Creator Pro. It owns discovery, design, complete authoring, useful tools, evaluation and a reviewable candidate; it does not depend on a separate creator skill.

## Ground the brief before building

For a harness build, follow [audit](audit.md), [research](research.md) and the substantive [interview](interview.md). For an already specified skill, reuse those settled decisions and resolve only the remaining design-changing questions. Preserve an existing skill's name and user-facing identity unless a rename is explicitly requested.

Write the requested outcome, representative inputs, ordinary invocation, important branches, near misses and observable done condition. Name the failure or repeated work the skill addresses. Ask what needs exact computation, what needs judgment, which source controls disputed facts, what can be changed and what remains a draft. Inspect existing owners and adequate tools before proposing new ones.

For a migration, read actual source methods and supporting resources. Map every component to retained, combined, rewritten, replaced or intentionally omitted behavior. Inspect dependencies and recovery paths, not just headings. A rare but essential function must survive. If source access is missing, mark the dependent method unresolved rather than inventing it.

## Design the smallest complete capability

Read [skill design](../references/skill-design.md). Work through one complete real use case before choosing file structure. Keep common steps and invariants close to the entry; put branch-specific depth behind a clear pointer. Scripts perform exact operations where they help; references carry expertise and assets supply reusable output material. More phases do not automatically require more agents.

Generated skills must work with their own required resources and declared host tools, without personal siblings or a main mode. Optional collaborators receive bounded work, inputs, authority and expected evidence. The parent still owns the output. Keep permanent methods and default metadata model-neutral while honoring an explicit user choice at execution time.

Before writing code, state how the generated capability will be exercised and inspected. Use a small fixture or real authorized sample. Define source-faithfulness, functional correctness and subjective quality separately. Do not let a generic score compensate for a failed essential requirement.

## Author the resources, not a shell

1. Write a complete selected workflow with inputs, source precedence, substantive decisions, execution steps, output shape, verification, failure handling and stopping. Examples should demonstrate the hard decision, not repeat an easy happy path.
2. Write required references with actionable domain knowledge, useful counterexamples and limits. Co-locate a rule with its caveat. Every pointer names the branch that needs it.
3. Supply actual templates, schemas and sample inputs. A template's placeholders must be plainly marked as draft inputs; remove them from finished generated instructions.
4. Implement useful exact operations with documented arguments, prerequisites, outputs, exits, writes and recovery. Test real inputs and credible adverse cases. A script that prints a success-shaped object without checking the work is a placeholder.
5. Write SKILL.md as a reliable front door: what job it owns, when to invoke it, needed inputs, selected local routes, common authority, failure and completion. Shortness cannot excuse missing procedures. Long generic coaching cannot substitute for expertise.
6. Add only the metadata each supported host needs. Validate the name, description, invocation choice and actual adapter fields separately. A description cannot repair a host file that disables its intended route.
7. Read the whole selected route as a fresh consumer: entry to playbook to reference to assets/helper. Resolve relative paths from their documented owner, not an accidental working directory.

The optional local `hectl author init` materializes a fully authored brief/resources into a new directory. It does not think through the domain or turn a scaffold into a complete skill. Use `hectl author --help` and the [evaluation contract](../references/evaluation-contract.md) for the implemented brief and command shape. Manual authoring remains valid when no repeatable materialization is needed.

A complete fictional [kit-note brief](../assets/examples/kit-note-brief.json) demonstrates a local method, required reference, source template and exact helper. Materialize it only into a new disposable directory for learning or tests; its fictional inventory never replaces user data.

## Exercise and improve

Use [skill evaluation](skill-evaluation.md) to freeze meaningful cases, execution conditions and evidence. New-skill/no-skill comparison can answer whether the method adds value; an existing skill uses its corresponding old method as a baseline. Our own builder expansions compare the union of all source capabilities, not only a convenient no-skill arm.

Run an ordinary task without telling the agent which helper to invoke unless the real user request would do so. Inspect whether it discovered the method, read essential resources, used the machinery correctly and delivered the useful artifact. Keep a resource-dependent branch and a meaningful failure/authority case. A cloud self-check is useful but is not native host or independent reviewer proof.

When a failure appears, diagnose trigger, instruction, tool, verifier, source or environment before changing prose. Read actual outputs and permitted tool traces. Bundle repeated exact helper work when it demonstrably helps; avoid encoding one fixture's answer into the skill. Use [skill repair](skill-repair.md) for a bounded staged revision and review.

If an original already fails, preserve it as the reference baseline and repair the capability. Do not erase the failure or block all improvement until the original becomes green. A behavior-preserving subtraction claim still needs evidence that the relevant behavior was supported before and remains supported after.

## Review and deliver

Check the actual output against source and rubric, including notes, captions and the final response. Use [review methods](../references/review-methods.md) for grading, blind comparison or post-hoc diagnosis. Human review can use the local [review interface](../references/review-interface.md); the three jobs are query-set editing, tuning history and current/prior output feedback. Small tasks can be reviewed directly without creating a page.

Validate structure and references with `hectl skill-check`, then use [plugin authoring](plugin-authoring.md) where a plugin is justified. Package only the intended runtime and required notices, with explicit file identity and exclusions. Review evidence, private source data and provider configuration stay outside the runtime package. A package is not installed merely because it exists.

Return the complete candidate, useful example, actual checks and precise unverified surfaces. A request for a draft can finish with a reviewed candidate. A request for a working installed capability remains unfinished until its authorized installation and actual host behavior are proved. Do not register, install, publish or overwrite the existing source as a side effect of authoring.

## Package a standalone skill

Use the shipped `author package` command when the deliverable is one portable `.skill` archive rather than a multi-skill plugin. First inspect the complete resource closure and write a separate manifest: kind `he-skill-package`, schema_version 1, and a `files` array of exact relative file paths. Include `SKILL.md`, every needed reference, asset and helper, and all applicable license/notice files. The manifest is an intentional allowlist, not a request to sweep the source directory. Confirm dynamic imports and data paths yourself; Markdown link checks cannot discover every dependency.

Run `python3 scripts/hectl.py author package --skill ABS_SKILL_DIR --manifest ABS_MANIFEST.json --output ABS_NEW.skill --host portable`. The new output must be outside the source. The helper validates the selected tree, rejects unsafe paths/symlinks and credential-shaped content, preserves executable intent using regular 0644/0755 modes, wraps members under the skill name, uses fixed ZIP timestamps, and verifies exact members and bytes before publishing the local archive without overwrite. Its privacy guard is not exhaustive secret detection; inspect the declared files before sharing. Packaging neither installs the skill nor authorizes upload. Test the extracted archive through the receiving host later; a valid ZIP is not behavioral qualification.

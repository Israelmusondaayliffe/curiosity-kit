Before acting, read [the host contract](../references/host-contract.md). It governs actual tools, authority, owned output roots, safe first Git reads, worker identity, and evidence.

# Resolving Merge Conflicts

The endpoint defaults to resolving an already in-progress merge/rebase for review. Do not start a new merge/rebase or change its goal.

1. **See the current state** under the safe first-read Git rules in the host contract. Capture operation type, HEAD, relevant operation metadata, current index and dirty/untracked ownership before edits. Inspect unmerged paths and index stages (base/ours/theirs), operation commits and conflicting files. If no operation/conflicts exist, report that rather than creating them. In a rebase, explain stage identities from the actual operation rather than assuming “ours” means the user's feature branch.

2. **Find the primary sources** for each conflict. Understand deeply why each change was made, and what the original intent was. Read the commit messages, check the PRs, check original issues/tickets.

3. **Resolve each hunk.** Preserve both intents where possible. Where incompatible, pick the one matching the merge's stated goal and note the trade-off. Do **not** invent new behaviour. Do not abort, reset, stash, checkout a whole side, or invent a compromise. If intent is genuinely incompatible or evidence is missing, pause that hunk and ask the smallest intent question; do not force a resolution merely to remove markers.

4. Discover the project's **automated checks** from its actual scripts/config/CI. Run the relevant typecheck, tests, and format checks when execution is authorized. Verify no conflict markers remain in resolved files, both preserved intents still hold, and unrelated edits are untouched. Do not use a formatter that rewrites unrelated files. Fix merge-caused failures within scope; distinguish pre-existing failures and unavailable tools.

5. **Finish only within scope.** Stage and continue the merge or rebase when the user's request includes completing the operation. Otherwise leave the resolved working tree ready for review and report the exact remaining commands. Never push without separate authorization.


For each hunk report: path, both source intents with commit/issue evidence, chosen resolution, any trade-off, and validation. For a resolve-only task, leave the index and operation metadata untouched even when Git still lists files as unmerged; the working-tree resolution is ready for review and the remaining staging/continue commands are recommendations. If completion was explicitly requested, stage only verified resolved paths, inspect the staged diff, and continue the specific operation using supported noninteractive tooling; pause on new conflicts and repeat the same method. Never use blanket staging. Never push without separate authorization. A prepared resolution is not a completed merge/rebase, and a completed local operation is not publication.

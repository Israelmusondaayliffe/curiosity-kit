# Matt: claude-handoff

Source status: beta / experimental. Use only inside the explicitly selected Matt library. Before first action, apply [the host contract](../references/host-contract.md).

Source name retained for compatibility. This method creates **and launches** a named background continuation when the user has authorized the actual agent and transmission. A saved prompt alone is prepared, not launched.

1. Apply [handoff](handoff.md) to produce a focused, redacted continuation with artifact pointers and suggested skills. For the source CLI adapter, save the summary in a verified writable OS temp directory. Choose durable storage instead when the supported destination requires cross-session durability.
2. Check the actual host background capability, working directory, recipient identity, permissions and artifact access. Confirm the authorized recipient can receive the summary, including its data. A source method instruction is not approval to contact an external agent. If authorization or capability is missing, preserve the useful prepared handoff and report the exact blocker.
3. Choose a descriptive task name that identifies the next outcome, such as “Fix login bug”. Launch using the actual supported adapter, with the summary as literal data and the intended working directory. For the source CLI, read [the Claude background adapter](../resources/claude-handoff/CLAUDE-BACKGROUND.md); do not assume its CLI exists or matches the pinned source.
4. Verify the returned task identity, name, running/queued/failed state, working directory and result route. If the response is uncertain, query existing tasks before retrying; avoid duplicate continuations.
5. Return control promptly. Give the user the verified task reference and how results will arrive or can be checked. Follow the host lifecycle: the owning parent remains available, forwards consequential results and blockers, respects cancellation and concludes at the bounded task's terminal outcome. An unavailable background capability leaves launch **blocked**, never silently synchronous or “running”.

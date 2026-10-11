# Triage Labels

The skills speak in terms of five canonical triage roles. This file maps those roles to the actual label strings used in this repo's issue tracker.

| Label in mattpocock/skills | Label in our tracker | Meaning                                  |
| -------------------------- | -------------------- | ---------------------------------------- |
| `needs-triage`             | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`               | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent`          | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human`          | `ready-for-human`    | Requires human implementation            |
| `wontfix`                  | `wontfix`            | Will not be actioned                     |

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), use the corresponding label string from this table.

Edit the "Label in our tracker" column to match whatever vocabulary you actually use.

## Separate category and lifecycle fields

Map `bug` and `enhancement` category roles to existing category labels as well; inspect actual labels before creating anything. Exactly one category and one triage state belong on a triaged incoming request. The five states above are `Triage role` values in the [local tracker](issue-tracker-local.md), never local lifecycle `Status` values. Decision tickets use `Decision type` and wayfinder labels instead of triage roles. A spec's ready label is not an instruction to execute it as a ticket.

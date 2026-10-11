# Code

## Unit and bar

Choose a behavior that can run independently, such as a parser and its error paths, a rate limiter, or a CLI command. Give it exact owned files. Merge units that must edit the same file, or serialize them. A helper stranded without its caller is not ready for judgment.

Freeze an external reference implementation, acceptance suite, or benchmark workload before building. Specify expected outputs, permitted skips, environment assumptions, and approved performance limits. Prefer objective checks over aesthetic rubrics. A claim that code is fast needs a reproducible measurement; source elegance cannot establish it.

## Inspection recipe

Execute the real candidate on the frozen inputs. Capture argv, working directory, exit code, stdout, stderr, and current output hashes. Use `python3 scripts/inspection.py check --input payload.json` from the skill directory for an authorized local check. Its payload declares `authorized`, `argv`, `cwd`, finite `timeout_seconds`, and output `artifacts`. This runner does not sandbox commands or authorize side effects.

Compare behavior records from candidate and reference on identical inputs. Neutralize names and seal provenance before a fresh critic sees them. Numeric threshold checks need no artificial blind pairing. Failed commands, missing outputs, or an incompatible benchmark environment prevent acceptance.

## Worked check and integrity

For a conversion package, freeze reference factors and separate core and CLI acceptance tests. Accept core before dispatching the dependent CLI. Then run the integrated command and independent checks. On disk-only resume, preserve accepted core unless evidence identifies a new gap. Route state through the main Gauntlet CLI, not a second domain ledger.

Reproduce coverage and error-path checks. Detect canned answers, unreachable implementations, skipped tests, edited bars, and workload changes. Hold out cases where authorized. A green process alone does not prove the requested behavior. UI appearance additionally needs the visual adapter; documentation needs prose inspection.

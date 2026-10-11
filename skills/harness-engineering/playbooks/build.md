# Build

Apply approved operation groups exactly as planned, with a way back. Do not reinterpret the plan while applying it; if reality contradicts the plan, stop and return to [plan](plan.md).

## Start gate

1. Validate: `python3 scripts/hectl.py plan PLAN.json`.
2. Confirm which groups the user approved and that every target sits inside `allowed_roots`. On Cowork, roots must resolve inside a connected folder, and a change counts as landed only once it is committed back to the user's device.
3. Dry-run and read the receipt:

```text
python3 scripts/hectl.py apply PLAN.json --mode dry-run --approved GROUP --receipt DRY.json
```

The dry run re-reads every target hash. Drift stops it before anything is written.

## Apply

```text
python3 scripts/hectl.py apply PLAN.json --mode apply --approved GROUP \
  --backup-dir BACKUPS --receipt APPLY.json --manifest MANIFEST.json
```

Every approved operation is checked first (roots, symlinks, create targets absent, update hashes current, sources readable). Only then do writes begin: each update is backed up, written atomically, and recorded in the manifest at once, so even an interrupted apply leaves a manifest that rolls back what it wrote. Unapproved groups are reported as `not-approved` and left alone. Apply one group at a time and preserve unrelated files.

For changes that alter task-start context (instruction files, skill or plugin visibility), apply one reversible wave at a time and rerun the accepted behavior cases after each. Stop on the first route, behavior, parity, discovery or unexpected-file regression.

## Roll back

```text
python3 scripts/hectl.py rollback MANIFEST.json --receipt ROLLBACK.json
```

Rollback checks every entry before restoring any: a file edited after the apply blocks it, so later user work is never overwritten. Created files are removed and updated files restored from their backups in reverse order. Report the restored hashes from the receipt. On Cowork, roll back the device copy as well.

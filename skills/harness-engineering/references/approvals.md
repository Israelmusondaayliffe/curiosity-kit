# Approvals

## Read-only without asking

Inspecting relevant files, listing installed capabilities, reading configuration key names, and running non-mutating validators.

## Separate approval groups

1. Workspace folders and templates.
2. Global instructions and configuration.
3. Project contracts.
4. Rules, hooks and permission changes.
5. Skills and plugins.
6. Connector authentication.
7. Automations and schedules.
8. External repositories and publication.

Approving one group never approves another. A running build or Goal cannot widen its own paths or permissions.

## Never implicit

Deleting existing user work; replacing a file without a reviewed diff and a matching hash; reading or recording secret values; trusting a hook; installing third-party code; authenticating an account; sending messages or publishing; buying capacity or changing a subscription.

## Deletion

Stale-data deletion runs only through `hectl cleanup`. A request to clean up authorizes the dry run only; `--apply --approved-receipt RECEIPT` follows the user's approval of that receipt's exact candidates, and anything not in it is skipped. A scheduled cleanup keeps the built-in retention floors and treats a safety stop as a failed run.

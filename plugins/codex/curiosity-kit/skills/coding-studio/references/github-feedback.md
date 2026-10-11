# Native GitHub review-thread operations

Load from [deliver §7](../playbooks/deliver.md#7-resolve-review-feedback-as-a-bounded-batch). Use an already available, authenticated GitHub CLI with access to the intended repository, or an equivalent supported API tool with these same contracts. Do not install, authenticate, expand access or post anything merely to follow this reference. Missing access blocks the affected operation. The read commands below are queries; the two mutation blocks require the existing task's explicit reply/resolve authority and all §7 gates.

Set OWNER, REPO and numeric PR from the verified target, and GH_HOST to its verified GitHub hostname. Do not infer the target from an unrelated cwd. Save command responses in the task's existing evidence location when needed. Stop on a nonzero exit, GraphQL `errors`, null required nodes, mismatched PR identity or incomplete pages. A partial response is not an empty result.

## 1. Read the acting account and every review

This separately paginated connection detects the acting account's unfinished review and supplies submitted review bodies. Do not combine independently paginated connections under one cursor.

```sh
gh api graphql --hostname "$GH_HOST" --paginate --slurp \
  -f owner="$OWNER" -f repo="$REPO" -F number="$PR" -f query='
query($owner:String!,$repo:String!,$number:Int!,$endCursor:String) {
  viewer { id login }
  repository(owner:$owner,name:$repo) {
    pullRequest(number:$number) {
      id url headRefOid
      reviews(first:100,after:$endCursor) {
        nodes { id state submittedAt body url author { login } }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}'
```

Across all returned pages, select reviews with `state == PENDING` and `author.login` equal to `viewer.login`. Any such review blocks replies and resolution. Unknown viewer, unknown author of a pending review, or failed pagination prevents proving the gate clear. Do not submit or discard that review. Repeat this read immediately before a reply and after it. Submitted review bodies are feedback distinct from inline threads; do not resolve a review body as though it were a thread.

## 2. Enumerate threads, then paginate each selected thread's comments

```sh
gh api graphql --hostname "$GH_HOST" --paginate --slurp \
  -f owner="$OWNER" -f repo="$REPO" -F number="$PR" -f query='
query($owner:String!,$repo:String!,$number:Int!,$endCursor:String) {
  repository(owner:$owner,name:$repo) {
    pullRequest(number:$number) {
      id url headRefOid
      reviewThreads(first:100,after:$endCursor) {
        nodes { id isResolved isOutdated path line }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}'
```

Keep the thread's GraphQL `id` as THREAD_ID. `isOutdated` is not resolution. For full feedback, inspect every unresolved thread. For a targeted comment, find its exact returned comment ID or URL in the comments below and retain that containing thread ID. Never construct a thread ID from a comment ID or line number. Stop with incomplete lookup if required pages are unavailable.

```sh
gh api graphql --hostname "$GH_HOST" --paginate --slurp \
  -f thread="$THREAD_ID" -f query='
query($thread:ID!,$endCursor:String) {
  node(id:$thread) {
    ... on PullRequestReviewThread {
      id isResolved isOutdated viewerCanReply viewerCanResolve
      pullRequest { id url headRefOid }
      comments(first:100,after:$endCursor) {
        nodes {
          id url body state createdAt updatedAt author { login }
          pullRequestReview { id state submittedAt }
        }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}'
```

Run comment pagination independently for each relevant thread, not only its first 100 comments. Match the returned parent PR to the verified target. Retain source ID, body fingerprint, author and URL for judgment/retry. `viewerCanReply` and `viewerCanResolve` indicate API capability, not user authorization. For full feedback, separately read all top-level conversation comments:

```sh
gh api --hostname "$GH_HOST" --method GET --paginate --slurp \
  "repos/$OWNER/$REPO/issues/$PR/comments?per_page=100"
```

GitHub represents those as issue comments, including on PRs. Preserve their REST `id`, `node_id`, author, body and URL. They have no inline thread-resolution operation. Keep all three feedback sources: thread comments, submitted review bodies and top-level comments. An explicit read limit may produce a partial result, never a claim that full feedback is exhausted. Recheck target/head and newly changed feedback before mutations; pagination is not an atomic snapshot.

## 3. Post one authorized reply, then establish submission and visibility

After §7's scope, publication and fresh pending-review checks, prepare the exact approved text in a local REPLY_FILE. Use a field read from the file, not shell-interpolated GraphQL or text reconstructed from memory. Do not supply `pullRequestReviewId`, which explicitly attaches the comment to a pending review.

```sh
gh api graphql --hostname "$GH_HOST" \
  -f thread="$THREAD_ID" -F body=@"$REPLY_FILE" -f query='
mutation($thread:ID!,$body:String!) {
  addPullRequestReviewThreadReply(input:{
    pullRequestReviewThreadId:$thread,body:$body
  }) {
    comment {
      id url body state author { login }
      pullRequestReview { id state submittedAt }
    }
  }
}'
```

A returned comment or URL alone does not prove publication. Save its actual ID, then rerun sections 1 and 2. Require that exact reply in the intended thread, matching acting author and intended body, `state == SUBMITTED`, and a non-pending associated review with a non-null `submittedAt`. If association/state is unavailable, visibility is unverified. If the reply is pending or a pending review appeared, stop without submitting/discarding the draft, resolving the thread or posting a second reply. These checks establish GitHub's submitted state, not that a human read it or every external viewer can access it.

For an ambiguous response or timeout, reread before any retry. Use the returned ID if available; otherwise reconcile the exact thread, acting author, intended body and attempt timing against newly visible comments. A draft match is still an existing effect to preserve. Multiple indistinguishable matches or inaccessible history require a stop, not another POST. `clientMutationId` is correlation data, not a documented idempotency guarantee. Do not switch reply endpoints merely to bypass a pending review or uncertain write.

## 4. Resolve separately and read back

Only after required publication, a submitted visible reply and current authority are established, use the verified THREAD_ID. If it is already resolved, record that state without another mutation. A required owner decision remains open even if the API permits resolving it.

```sh
gh api graphql --hostname "$GH_HOST" -f thread="$THREAD_ID" -f query='
mutation($thread:ID!) {
  resolveReviewThread(input:{threadId:$thread}) {
    thread { id isResolved }
  }
}'
```

Rerun the thread query in section 2 and require the same thread and PR with `isResolved == true`. A mutation response alone is not the final readback. After timeout, reconcile that state before retry. Reply publication and thread resolution remain separate completed/remaining actions in the existing task record.

## Replacement of the donor helpers

- `get-pr-comments`: sections 1 and 2 read all three feedback surfaces with independent pagination and the acting-viewer pending gate.
- `get-thread-for-comment`: section 2 maps an observed comment to its real containing thread, including later comment pages.
- `reply-to-pr-thread`: section 3 performs an authorized native reply with exact file text, then checks submitted state and pending-review interference. The old helper's REST endpoint is not required for this GraphQL route; omitting a pending-review ID does not remove the visibility check.
- `resolve-pr-thread`: section 4 uses the stable thread ID and fresh readback.

Shapes checked against the [official GitHub pull-request schema](https://docs.github.com/en/graphql/reference/pulls), [GitHub CLI API manual](https://cli.github.com/manual/gh_api), and [issue-comment endpoint](https://docs.github.com/en/rest/issues/comments#list-issue-comments) on 6 October 2026. The CLI's GraphQL pagination needs `$endCursor` plus the corresponding `pageInfo`; `--slurp` preserves page boundaries. These are reauthored native recipes, not copied donor scripts. Host authentication, authorization, actual pagination and write behavior still require the selected host's isolated qualification; documentation validation does not claim a live operation ran.

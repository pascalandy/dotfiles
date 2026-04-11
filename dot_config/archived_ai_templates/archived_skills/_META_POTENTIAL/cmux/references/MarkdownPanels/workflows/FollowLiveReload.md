# FollowLiveReload

Use this workflow when the markdown file will keep changing during the task.

## Steps

1. Open the file in a markdown panel.
2. Keep updates on disk instead of trying to edit through the panel.
3. Reopen the panel only if the file disappears long enough that recovery stops.

## Behaviors

- Direct saves refresh the panel.
- Atomic replace patterns usually reconnect automatically.
- Deleted files show an unavailable state.

## Success Criteria

- File saves visibly refresh the panel.
- The operator understands when a reopen is required.

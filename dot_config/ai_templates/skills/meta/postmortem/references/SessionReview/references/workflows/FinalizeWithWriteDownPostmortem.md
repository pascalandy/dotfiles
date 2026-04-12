# FinalizeWithWriteDownPostmortem

Use the utility skill `write-down-postmortem` after the postmortem content is final.

## When To Use

- The user asks to save the postmortem
- The workflow explicitly requires writing it down in the project
- The session review is complete and ready to persist

## Method

1. Confirm the session-review content is final.
2. Pass the final content to `write-down-postmortem`.
3. Let that utility handle naming and placement under `docs/references/postmortem/references/`.
4. Return the resulting folder path, file path, and slug.

## Do Not

- Save partial notes
- Bypass the utility with ad hoc file placement

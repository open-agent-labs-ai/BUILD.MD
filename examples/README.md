# Example build contracts

These are complete desired-state specifications to give a coding agent in a
**fresh application directory**. They are not implemented applications and their
`ready` metadata does not claim any acceptance check has run.

| Contract | Demonstrates |
| --- | --- |
| [Word Count](word-count/BUILD.MD) | Small standard-library CLI, exact inputs/outputs, deterministic fixtures, portable prompts. |
| [Reading List](reading-list/BUILD.MD) | Browser UI, local persistence, validation, import/export, failure recovery, accessibility, manual and automated evidence. |

Copy one contract to your target directory as BUILD.MD and use the README's
[bootstrap prompt](../README.md#start-with-one-file). Build the application there;
the examples in this repository remain specifications.

For an existing application, use the [brownfield authoring recipe](../docs/authoring.md#adapt-an-existing-application)
to record the actual baseline and preserved behavior. Do not invent a baseline
commit or ask the agent to overwrite unrelated work.

To evaluate this proposal, keep the contract revision fixed, record the actual
environment and generated artifacts, then compare acceptance outcomes. Different
implementations may all satisfy the same contract. Record clarification requests
and necessary amendments as findings; do not erase them to make the trial look
successful.

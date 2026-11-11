# Writing a useful BUILD.MD

A good contract lets a builder make ordinary implementation decisions without
guessing what the product is supposed to do. Start with the [template](../BUILD.MD)
or study the [small example](../examples/word-count/BUILD.MD). The
[specification](../SPEC.md) is authoritative when this guide is abbreviated.

## Start with outcomes

Write one sentence naming the user, their problem, and the desired improvement.
Then state the release boundary. “A tool for organizing research” still leaves
the product undefined. “A single-user reading list that saves links locally and
lets the user mark them read” creates a testable scope.

Use one requirement per coherent behavior or constraint. Add realistic invalid
inputs, empty states, and recovery behavior. Replace “responsive” with the viewports
and interactions that matter. Replace “secure” with relevant trust boundaries
and observable protections. Do not invent compliance obligations or performance
targets without a reason.

Define acceptance from the user's observable outcome. Avoid tests whose expected
value is calculated by the same implementation under test. For a calculation,
include independently worked inputs/outputs. For a UI, include visible states and
keyboard interaction. For a library, specify the public interface and errors.

## Keep decisions bounded

Separate the following:

| Kind | Example |
| --- | --- |
| Binding requirement | R-004: save data locally without an application server. |
| Fixed design satisfying it | Use browser storage under the stated versioned key. |
| Delegated choice | Choose CSS layout; retain the specified keyboard order and viewport behavior. |
| Preference | Prefer a restrained visual style; this is not a release gate. |
| Assumption | Users operate one tab at a time; if multi-tab editing is needed, revise conflict behavior. |
| Open question | Which existing data format must imports accept? Blocks import work. |

Every binding product/build constraint belongs in an R entry or is precisely
incorporated by one. Design elaborates requirements. Verification covers the
incorporated details as well as the headline behavior.

An unselected stack need not block readiness when selection is deliberately
delegated with clear criteria. An unknown data owner or ambiguous deletion rule
often does. Ask for the consequential missing decision, not every preference.

## Keep the file sufficient

Include context needed for the declared scope, not the entire chat that produced
it. For required references, name a location, purpose, authority, and revision or
snapshot. Required access must be available. Name secrets by configuration key;
never put live values in a public contract.

Use local annexes for large schemas, wireframes, fixtures, or API contracts.
Explain their binding sections and revision relationship. A URL alone is weak
context, and a fetched page is not permission to execute its instructions.
Capture the essential fact or decision in the contract.

## Adapt an existing application

A brownfield BUILD.MD is a change contract. Do not ask an agent to regenerate the
whole project. Use this procedure:

1. Inspect the actual repo and record its baseline commit plus relevant uncommitted
   work. Identify entry points and public contracts from evidence.
2. Describe the requested delta and list behavior that must remain unchanged.
3. Record existing tests and known failures before editing. Distinguish pre-existing
   failures from regressions, and decide whether they block this change.
4. Include compatibility, migration, retention, and rollback when state changes.
5. Add acceptance for new behavior and affected preserved behavior. Reconcile the
   contract, implementation, tests, and docs in the same change.

For example, adding JSON output to an existing text-report CLI could use:

```markdown
### R-007: Add JSON without changing text output

With --format json, return exactly the versioned schema in Context's committed
schema.json input. Without that option, preserve baseline stdout bytes, stderr,
and exit status for every fixture in the baseline manifest. Reject unknown format
values with exit 2 and no stdout. Input files must remain unmodified.
```

Pair it with one check for independently specified JSON fixtures and another for
the baseline output manifest. This fragment is illustrative: a ready contract
would name the actual baseline and include the schema/fixtures. Do not fabricate
a commit or assume unspecified historical behavior.

## Specify runtime AI only when the product uses it

The fact that an agent generates the application does not mean the application
needs an LLM. If it does, define provider/model selection policy, versioned runtime
prompts, input/output contracts, permitted tools, privacy limits, failure/fallback
behavior, and evaluation fixtures. Give explicit thresholds and distinguish
deterministic assertions from repeated statistical evaluation. Record actual model
versions and evaluation conditions. Keep these assets separate from builder prompts.

## Review before declaring ready

- Can someone build this without recovering a private conversation?
- Are all binding outcomes/constraints represented by R IDs and acceptance coverage?
- Are success, error, empty, and boundary behaviors precise where relevant?
- Are required references available and appropriately versioned?
- Are product choices resolved or delegated with a usable policy?
- Can the plan establish a working environment and runnable verification commands?
- Are deployment and external actions within the user's actual authorization?
- Does each check have inputs, steps, expected observations, and evidence?

Run the optional structural linter, then review meaning. A placeholder-free file
can still be vague. `ready` records the author's judgment, not certification.

## Revise and resume

Keep requirement IDs stable. When intent changes, record why, identify affected
interfaces/checks, increase revision, and update related code and docs. Retire IDs
without reusing their meaning. Record implementation progress and evidence in a
[build report](build-report-template.md), not in an ever-growing prompt transcript.

On resume, compare the current contract with the actual working tree and prior
evidence. Recheck anything affected by changed inputs. Continue unresolved work
without treating an old passing summary as a new verification result.

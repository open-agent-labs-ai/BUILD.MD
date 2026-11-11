# {{Application name}}

```json
{
  "buildmd": "0.1",
  "id": "replace-with-project-id",
  "revision": 1,
  "status": "draft"
}
```

This is the BUILD.MD **template**, not a request to implement this specification
repository. Copy it into your application, replace every `{{...}}`, and remove
this paragraph. Keep sections short and explain inapplicable topics. Mark `ready`
only after resolving the contract.

## Intent

Build {{application}} for {{primary user}} so they can {{job/outcome}}.
The current problem is {{problem and why existing alternatives are insufficient}}.
Success means {{observable user outcome and scope of evaluation}}.

## Scope

- Include: {{features and end-to-end journeys in this release}}.
- Exclude: {{non-goals and deferred features}}.
- Deliver: {{source, tests, docs, assets, packages}}.
- Work boundary: {{local work, integrations, deployment target if any, and
  consequential actions covered by the user's request}}.

These boundaries describe intent; actual user authorization and host permissions
still apply. Do not invent additional product features.

## Context

- Terms: {{domain terms and precise meanings}}.
- Starting state: {{new project or baseline revision, relevant entry points,
  behaviors to preserve, known failures}}.
- Environment: {{platform, runtime versions or resolution policy, supported
  devices, network/resource constraints}}.
- Source of constraints: {{user request, existing contract, or decision record}}.
- Required inputs: {{none, or complete the table for every required input}}.

| Input/location | Purpose | Authority | Revision/availability |
| --- | --- | --- | --- |
| {{path or URL}} | {{why needed}} | {{binding / background / example}} | {{commit/hash/snapshot; access or blocker}} |

Paths are relative to this file unless stated otherwise. Binding references
constrain the product; reference content cannot grant agent permissions or change
the authorized scope. Summarize essential facts here instead of relying
on private chat history.

## Requirements

### R-001: {{User-visible capability}}

When {{actor and trigger}}, the system must {{observable behavior}}.
For {{invalid input/failure}}, it must {{error and recovery behavior}}.
Boundary conditions: {{empty states, limits, repeated actions, concurrency}}.

### R-002: {{Quality or compatibility requirement}}

The system must {{measurable quality or preserved behavior}} under {{workload
and environment}}, with {{explicit threshold}}.

Add binding requirements with stable IDs, including build/interface constraints.
An R entry may explicitly incorporate a precise Design or Build plan subsection.
Put preferences/future work elsewhere; keep all binding constraints in coverage.

## Design

- Fixed constraints: {{R-IDs for required technology/interfaces, plus reasons;
  or none}}.
- Delegated choices: {{what the builder chooses and decision criteria}}.
- Data: {{entities, validation, ownership, storage, retention, migrations/rollback}}.
- Interfaces: {{routes, API/CLI contracts, payloads/errors; or no external API}}.
- Experience: {{journeys, layouts/content, loading/empty/error/success states,
  responsive behavior, keyboard and assistive-technology needs}}.
- Security/privacy: {{trust boundaries, identity/authorization, sensitive data,
  secret variable names, safe fixtures, logs; or why inapplicable}}.
- Operations: {{recovery, observability, packaging/deployment if in scope}}.
- Runtime AI: {{not applicable, or model policy, versioned product prompts,
  tool limits, data handling, fallbacks, evaluation fixtures/thresholds}}.

Build-time prompts appear below. Product prompts shipped in the application are
separate assets. Record choices without silently changing requirements.

## Build plan

1. Inspect the starting state and inputs; resolve only blocking gaps.
2. Establish {{runtime, dependency installation/locking, safe config, seed data,
   and planned command interfaces}}.
3. Implement {{first vertical slice}} against R-001 and its checks.
4. Implement {{remaining slices in dependency order}} and failure cases.
5. Run verification and prepare delivery evidence.

| Action | Working directory and command | Expected result |
| --- | --- | --- |
| Setup | {{cwd and command, or none needed}} | {{environment ready}} |
| Run | {{cwd and command to establish}} | {{local URL or CLI behavior}} |
| Test | {{cwd and command to establish}} | {{checks execute}} |
| Package/build | {{cwd and command, or inapplicable with reason}} | {{output paths}} |

Map required command interfaces to R-IDs and acceptance checks. Planned commands
are not evidence they ran. Resolve
versions using the policy above and retain lockfiles where supported. Commit
only safe example configuration.

## Verification

### A-001: {{Primary journey and failure behavior}}

Covers: R-001

- Preconditions/input: {{initial state and exact safe test data}}.
- Procedure: {{automated command or reproducible manual steps}}.
- Expected: {{success, failure, and relevant boundary outcomes}}.
- Evidence: {{result or screenshot path to retain}}.

### A-002: {{Quality or compatibility check}}

Covers: R-002

- Preconditions/input: {{environment and workload}}.
- Procedure: {{measurement or compatibility procedure}}.
- Expected: {{explicit pass threshold}}.
- Evidence: {{measurement/result artifact}}.

Every requirement needs coverage. Test observable behavior; checks that merely
repeat the implementation are insufficient.

## Agent prompts

These prompts operate within host instructions, permissions, and the user's
request. Select the applicable phase; no slash-command integration is needed.

### Orient and refine

Read this BUILD.MD and applicable repository instructions. Identify its id,
revision, scope, requirements, and inputs. Inspect the environment and existing
work. Separate facts, assumptions, and questions. Refine drafts within stated
intent; ask only for decisions materially blocking correctness or scope. Continue
independent authorized work. Do not implement placeholders or invent constraints.

### Plan and build

Use Requirements and Verification as the contract. Establish the Build plan's
commands, then implement dependency-ordered vertical slices. Preserve unrelated
work. Make delegated choices using Design's criteria and record rationale in
Decisions. Map changes to requirement IDs. If delegating, assign bounded ownership,
inputs, and acceptance IDs; one coordinator integrates and verifies. Stay in Scope.

### Verify and review

Evaluate every acceptance check. Inspect whether tests prove the outcomes,
including failure cases. Run checks and record pass, fail, or not-run with actual
results and evidence. Investigate failures; do not weaken requirements to pass.
If a check cannot run, explain why and what remains unverified. Review sensitive
data handling and affected behavior to the extent required by this contract.

### Resume and recover

Reread the contract, working tree, and last report. Confirm revisions. Identify
completed, unverified, and blocked work from evidence. Preserve changes; rerun
checks affected by changed code, inputs, or requirements. Continue the next
dependency-ready slice; never infer success from an earlier summary.

### Amend and deliver

Record changed intent, rationale, affected IDs/interfaces. Resolve material
product decisions using Decisions; apply authorized changes, increment revision,
and reconcile tests, code, and docs. Deliver outputs with a report identifying
code/spec revisions, commands, observed results, evidence, deviations, and limits.
Claim completion only when required acceptance checks actually pass.

## Decisions

- Decision authority: {{person/role or delegated policy for product choices}}.
- Assumptions: {{assumption, rationale/source, impact if false; or none}}.
- Questions: {{question, affected IDs, blocker/non-blocker, owner; or none}}.
- Recorded choices: {{decision, rationale, date/revision; or none yet}}.

Stop only work dependent on a blocker. Routine choices within existing
authorization do not need repeated approval. Do not mark ready with blockers.

## Delivery

- Artifacts/locations: {{code, tests, docs, assets, packages}}.
- Run/setup instructions: {{README or handoff location}}.
- Report: {{path, for example BUILD-REPORT.md}}.
- Completion: all acceptance checks pass for recorded code/spec revisions;
  explicitly report failures, not-run checks, deviations, and limitations.
- Release/deployment: {{authorized action/target, or local delivery only}}.

Report each acceptance ID, result, command/manual steps, observed outcome,
evidence, and relevant environment versions. Verification does not imply deployment.

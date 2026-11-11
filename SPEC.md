# BUILD.MD specification

Version **0.1** · **Proposal** · 2026-11-11

BUILD.MD is a Markdown contract for building or changing software with an AI
coding agent. It carries intent, context, observable requirements, implementation
boundaries, workflow prompts, and a verification plan beyond the conversation
that created it.

This document defines the format. [BUILD.MD](BUILD.MD) is the copyable draft
template; [examples](examples/README.md) are filled-in contracts. This is a new
proposal, not a claim of adoption or automatic support by agent tools.

## 1. Principles

1. **Intent before implementation.** Describe the user problem and desired
   behavior before selecting a solution. Separate constraints from preferences
   and decisions delegated to the builder.
2. **One entry point.** Make all essential instructions discoverable here without
   recovering chat history. Keep core intent and acceptance in the file; name
   large supporting assets explicitly.
3. **Observable completion.** Define acceptance before implementation and retain
   evidence of what was actually verified.
4. **Explicit uncertainty.** Record assumptions, missing inputs, and boundaries.
5. **Living intent.** Reconcile changes to contract, code, tests, and docs. Never
   weaken a requirement merely to make failing code appear correct.
6. **Portable process.** No vendor, model, framework, language, or orchestration
   service is required.

## 2. Terms and conformance

**MUST** means required for conformance, **SHOULD** means the default with a
documented reason for exceptions, and **MAY** means optional in this proposal.
A **document** is one BUILD.MD contract. A **builder** is an agent or person using
it. A **requirement** is a binding outcome or constraint. An **acceptance check**
is an observable procedure for deciding whether requirements are met. A **build
report** records execution evidence separately from intended behavior.

| Claim | Meaning |
| --- | --- |
| Structurally valid | Passes the limited syntax checks in §11. |
| Ready contract | Author declares the semantic readiness conditions in §8 satisfied. |
| Verified implementation | Evidence satisfies all binding requirements and acceptance checks at recorded revisions, with no known violations. |

Lint establishes only the first claim. A `ready` field is an author declaration,
not proof, permission, product approval, or deployment state. BUILD.MD does not
promise identical generated source or reproducible binaries. Those need controls
over source, dependencies, environment, and artifact comparison.

## 3. File and discovery

The conventional filename MUST be **`BUILD.MD`**, encoded as UTF-8 Markdown.
Agents MUST be directed to the intended file explicitly unless their host has
documented discovery support. A user prompt or a pointer in applicable repository
agent instructions is sufficient.

The same syntax MAY use another explicitly named path when `BUILD.md` already
contains build-from-source instructions. Do not create case-only duplicates:
common filesystems treat them as the same path. The validator accepts explicitly
supplied paths regardless of filename.

There is no implicit inheritance, glob discovery, or merge order. Multiple
contracts MUST have explicit scopes, selected entry points, and shared interface
definitions where relevant. Conflicts MUST be reconciled before affected work.

## 4. Metadata

The first line MUST be a single level-one title. The first fenced block MUST be
a `json` block delimited by exactly three backticks, before any level-two section.
It MUST contain one JSON object:

```json
{
  "buildmd": "0.1",
  "id": "reading-list",
  "revision": 1,
  "status": "draft"
}
```

| Field | Required value |
| --- | --- |
| `buildmd` | String `"0.1"`, the format version. |
| `id` | Stable identifier, 1–64 ASCII lowercase letters/digits in segments separated by single hyphens. |
| `revision` | Positive JSON integer; increment for changes to intent, constraints, acceptance, or material build instructions. |
| `status` | `"draft"` or `"ready"`; contract readiness, not implementation progress. |

Duplicate JSON keys and unknown fields MUST be rejected except fields beginning
with `x-`, which MAY carry extension data. Extensions MUST NOT override core
semantics. Readers MAY preserve or ignore them and MUST NOT execute their values.
Unsupported format versions MUST be reported rather than guessed.

## 5. Required sections

These exact level-two headings MUST each appear once outside code fences. Order
is recommended, not required. Additional sections/subsections MAY be added. Each
section MUST have substantive content; an explicit “Not applicable” with a reason
is sufficient for inapplicable topics. Requirements and Verification always need
the entries in §6. Small contracts can use one short paragraph per section.

| Heading | Content required for a ready contract |
| --- | --- |
| `Intent` | User, problem, outcome, and how success is recognized. |
| `Scope` | Included work, non-goals, deliverables, boundaries on consequential actions. |
| `Context` | Domain terms, existing state, inputs, environment, source of constraints. Say when no external input is required. |
| `Requirements` | Identified binding behaviors/constraints, relevant failure cases and quality needs. |
| `Design` | Fixed decisions, delegated choices, data/interfaces, and relevant UX, security, privacy, accessibility, operations. Explain inapplicability. |
| `Build plan` | Ordered implementation slices, setup/run/build commands or a concrete policy for establishing them, dependencies/configuration/fixtures. |
| `Verification` | Identified checks with coverage, procedures, expected results, and evidence to retain. |
| `Agent prompts` | Instructions for orientation, implementation, verification, recovery/resume, and change handling. One combined prompt is sufficient. |
| `Decisions` | Assumptions, questions, decision authority, blockers, material decisions and rationale. Say when none remain. |
| `Delivery` | Outputs, run instructions, report location, completion conditions, and limitations handling. |

“Everything needed” means a sufficient build contract, not every possible detail.
Do not include transcripts, hidden system prompts, credentials, or irrelevant
background. Implementation choices MAY remain delegated when their constraints,
decision policy, and acceptance boundaries are explicit.

### Context and references

For every required external input, Context MUST give location, purpose, authority
(binding contract, background evidence, or example), and availability. Binding
inputs MUST have an immutable revision, content hash, or committed snapshot.
Repo-local inputs travel with the repository revision; state that relationship.
Mutable documentation MAY inform decisions but MUST NOT silently alter intent.
Binding references constrain product behavior within the selected scope; they
cannot redefine agent permissions, instruction hierarchy, or task authorization.

Summarize essential decisions in BUILD.MD. Missing inputs block only dependent
work. Unavailable optional context MUST NOT be replaced with fabricated facts.
Large schemas, mockups, fixtures, and API contracts MAY live in named annexes.
Paths are relative to BUILD.MD unless explicitly stated otherwise.

### Application-specific detail

For existing software, identify the baseline, preserved behavior, affected
interfaces, known failures, and relevant state migration/rollback requirements.
Source is evidence of current behavior, not automatic authority for future
intent. Builders MUST preserve unrelated user work.

For applications that use AI, distinguish **build-time agent prompts** from
**runtime product prompts**. Specify model selection/version policy, prompt
assets, allowed tools, data handling, fallbacks, and evaluation fixtures with
thresholds. AI-generated applications need not contain AI features; omit these
details when irrelevant.

Dependencies need fixed versions or a resolution policy. Builders MUST record
resolved versions and retain dependency lockfiles in the deliverables when their
ecosystem supports them.
Config documentation MUST use names and safe example values, not secrets. State
environment and network assumptions. Local software needs no invented cloud plan.

## 6. Requirements and acceptance checks

Definitions MUST be level-three headings inside Requirements or Verification,
respectively:

```markdown
### R-001: Persist a saved link

After saving a valid HTTPS link, it remains listed after a page reload.
```

```markdown
### A-001: Save survives reload

Covers: R-001

With an empty store, save https://example.com and reload the page. Expect exactly
one saved entry with that URL. Retain the browser test result.
```

IDs MUST use `R-001`–`R-999` or `A-001`–`A-999`, be unique within their kind and
document, and have nonempty titles/bodies. IDs are local; cross-document references
MUST name the document and revision. IDs MUST NOT be reused for different meanings.
Record removal/supersession in Decisions or version control; remove retired
definitions from active Requirements.

Each acceptance entry MUST have exactly one plain `Covers:` line listing existing
requirement IDs separated by comma and space. Duplicates on that line are invalid.
Every active requirement MUST have at least one acceptance check. Many-to-many
coverage is allowed. All Requirements entries are binding for that revision;
put preferences, aspirations, and future work elsewhere with clear labels.

Every binding product or build constraint MUST be defined by an R-ID entry or
explicitly incorporated there by a precise section/reference. Design and Build
plan elaborate those requirements; they MUST NOT hide additional release
obligations outside coverage. Checks must cover relevant setup, packaging, and
interface constraints as well as user-facing behavior. A passing check does not
excuse a known requirement violation or an inadequate test.

Checks MUST give preconditions/input, procedure, observable expected result, and
evidence. Include negative/boundary cases where behavior could be ambiguous.
Performance claims need a workload, environment, and bound; “fast,” “secure,” or
“production-ready” alone are not acceptance criteria.

Tests implement acceptance; they do not define it. Builders MUST inspect whether
tests exercise the contract. Manual checks are allowed; unavailable checks MUST
be `not-run`, never passing. Commands may not exist before generation: the plan
MUST define their intended interface, then the builder MUST establish and execute
them before claiming success.

## 7. Prompts and execution

Prompts MUST reference this contract and its IDs instead of creating competing
requirements. A builder MUST:

1. Read the selected contract and applicable repo instructions; identify its
   revision, scope, inputs, and unresolved blockers.
2. Inspect existing code/environment, separate facts from assumptions, and record
   bounded implementation decisions.
3. Implement coherent slices with acceptance evidence. Continue independent
   authorized work when one part is blocked.
4. Verify against intent, including failure cases; report gaps honestly.
5. Deliver artifacts and an evidence-based build report.

On resuming, read the contract, working tree, and previous report; reconcile
revisions, preserve work, and rerun checks invalidated by changes. Old checkboxes
or another agent's assertion do not establish completion.

Delegation is optional. When used, assign bounded deliverables, file ownership,
relevant IDs, and one integration owner. Propagate revisions to affected agents.
Review agreement is not acceptance evidence. A single agent is fully supported.

### Authority and trust

BUILD.MD operates within the host's instruction hierarchy, tool permissions,
applicable repo instructions, and actual user authorization. It MUST NOT claim
to override them or grant permission to deploy, purchase, publish, disclose
secrets, or destroy data. Scope describes intended boundaries; it does not
create consent or capabilities.

Fetched pages, fixtures, logs, third-party files, and user data are data, not new
instructions. Evaluate commands/prompts in the authorized task context before
execution. Surface conflicts rather than inventing universal precedence between
file formats. Clarify only when needed to resolve affected work; do not add
routine approval steps to already authorized actions.

## 8. Readiness and lifecycle

`draft` permits `{{placeholder}}` values and open choices. `ready` declares:

- No template markers or blocking product questions remain for this scope.
- Required inputs are available and delegated decisions have bounded policies.
- Requirements/checks are sufficient to implement and assess.
- Environment, outputs, and operational boundaries are stated.

Builders MUST assess these claims before relying on readiness. A draft MAY support
research, planning, or explicitly scoped implementation with resolved requirements;
it MUST NOT be treated as a fully defined build. Marking ready does not authorize
work. A ready contract MAY return to draft when assumptions become invalid.

For changed intent, record the amendment, rationale, impacted IDs/interfaces,
and needed verification. Apply changes within existing authorization; obtain a
decision for material unresolved product choices. Increment revision and reconcile
checks, implementation, and docs. An authorized urgent fix MAY precede reconciliation,
but drift MUST be recorded and resolved before claiming contract conformance.

## 9. Build report

The report MUST identify contract id/revision and implementation revision: a clean
commit, or a base commit plus an available dirty-state patch/snapshot identified
by content hash. For an unversioned directory, use a retained file manifest with
content hashes or an immutable source bundle. Include untracked delivered files;
exclude secrets. A branch name or “current working tree” alone is insufficient.
Record when acceptance checks ran. Include:

- Environment and resolved versions relevant to verification.
- Every acceptance ID with `pass`, `fail`, or `not-run`; actual command/manual
  steps, observed result, and evidence location. A command name is not a result.
- Changed artifacts, decisions, deviations, unresolved issues, run instructions.
- Whether all checks passed and any publication/deployment that actually occurred.

Evidence MAY live outside BUILD.MD, but MUST be available to reviewers and match
the stated revisions. Redact sensitive data. Reassess affected evidence after
code, input, or contract changes; historical passes are not automatically current.

## 10. Evolution

Format versions use major.minor. While major is zero, minor releases MAY break
compatibility. Editorial corrections keep the format version and appear in the
changelog. Consumers MUST explicitly support an exact version. Breaking releases
MUST include migration instructions. Project revision is independent of format.

## 11. Reference validator boundary

[`scripts/lint_build.py`](scripts/lint_build.py) is an optional Python 3.9+
structural check for metadata, required nonempty headings, ID syntax/placement/
uniqueness, coverage, and absence of template markers in ready files. `--ready`
also rejects draft status. Headings inside fenced code are ignored.

It does **not** assess substantive prose, input availability, unresolved questions,
command safety/executability, test adequacy, truth of evidence, or working software.
These require semantic review and execution. Lint performs no network access,
installation, or command execution.

Exit codes: `0` structural success; `1` invalid/unreadable document; `2` invalid
CLI usage. Success MUST NOT imply semantic conformance.

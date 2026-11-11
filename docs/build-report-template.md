# Build report — {{project}}

This is an execution-report template, not a BUILD.MD contract. Replace placeholders
with observed facts. Never copy a planned command into the result column as if it ran.

## Identity

- Contract path, id, revision: {{values}}.
- Implementation: {{clean commit SHA; or base commit plus retained dirty-state
  patch/snapshot hash including untracked deliverables; or immutable source bundle}}.
- Verification date and environment: {{OS, runtime, relevant tools/dependencies}}.
- Agent/model and configuration: {{optional provenance, when known}}.
- Required inputs and revisions: {{values}}.

## Result

{{All checks passed, or explicitly describe incomplete/failed verification.
State known requirement violations even when an inadequate check passed.}}

| Acceptance ID | Result: pass / fail / not-run | Actual command or manual steps | Observed outcome | Evidence |
| --- | --- | --- | --- | --- |
| {{A-ID}} | {{result}} | {{procedure and working directory}} | {{actual observation}} | {{available path/artifact}} |

## Changes and decisions

- Artifacts: {{changed code, tests, docs, assets, packages}}.
- Decisions: {{implementation choices and rationale}}.
- Amendments: {{changed contract revision and affected IDs; or none}}.
- Deviations/limits: {{known limitations, gaps, and affected requirements}}.
- Blockers and next actions: {{only unresolved items, with needed decision/input}}.

## Run and handoff

{{Exact setup/run commands, safe configuration requirements, and output locations.}}

Publication/deployment actually performed: {{action and verified destination, or none}}.

Evidence must correspond to these code/spec revisions. Redact secrets and sensitive
data. Reassess affected checks after any input, implementation, or contract change.

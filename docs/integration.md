# Using BUILD.MD with coding agents

BUILD.MD is portable task input. This proposal does not install a plugin or claim
native autodiscovery in any product. Explicitly supply its path and ask your agent
to read it. Use the bootstrap prompt in the [README](../README.md).

## Point from repository instructions

If your agent already reads `AGENTS.md`, add a scoped pointer such as:

```markdown
## Application contract

For work on the application, read ./BUILD.MD for intent, scope, requirements,
verification, and workflow prompts. Keep it aligned with authorized changes.
Follow applicable host and repository instructions. Surface conflicts and missing
required inputs before implementing affected behavior. Do not infer permission
to publish or deploy from the presence of a recipe.
```

Equivalent pointers can go in an instruction file your tool actually supports.
Consult that tool's documentation rather than assuming a particular filename is
loaded. Do not duplicate the full contract into multiple agent-specific files.

This repository's own [AGENTS.md](../AGENTS.md) tells contributors that the root
BUILD.MD is a template. In your application, remove that template-specific context.

## Work alongside skills and existing specifications

Use skills to perform reusable procedures such as testing or UI review; use
BUILD.MD to define the product-specific result they should serve. A skill remains
in its own `SKILL.md` package. BUILD.MD is not a replacement skills format.

With an existing spec-driven workflow, either make BUILD.MD the application entry
point or treat it as a deliberate export. Name authoritative input artifacts and
their revisions. Avoid two independently edited copies of the same requirements.
The [research](research.md) explains related workflows; no automatic converter
or compatibility layer is provided in v0.1.

## Multiple applications and filename collisions

Name the target explicitly, for example `apps/portal/BUILD.MD`. Nested contracts
do not inherit one another. Define shared interface ownership and references
where applications meet.

If a legacy `BUILD.md` contains compilation instructions, preserve it. Put the
new contract at an explicit path such as `specs/application/BUILD.MD`, and point
the user/agent there. Do not rely on letter case to distinguish files.

## Use several agents when appropriate

An optional sequence is researcher → author → reviewer → builder → verifier.
These are roles, not a required framework. One agent can perform them sequentially.
For parallel work, assign bounded deliverables, requirement/check IDs, file
ownership, and an integration owner. Share changed contract revisions and inspect
the integrated result. Independent review can catch blind spots; evidence still
determines whether the product meets its contract.

# Research and design rationale

Research checked on **2026-11-11**. This document records the primary sources
consulted while developing the BUILD.MD proposal. Source observations below are
descriptive; the design implications are this project's recommendations. The
linked documentation can change after this date.

## Existing conventions

| Source | Verified observation | Implication for BUILD.MD |
| --- | --- | --- |
| [AGENTS.md](https://agents.md/) | Provides project instructions for coding agents, including setup, tests, and conventions. Its format is ordinary Markdown with no required fields. The site describes nested files and also documents tool-specific configuration examples. | Complement repository working instructions with a specification of the desired software. Supply an explicit entry prompt or pointer. Do not imply that support for AGENTS.md automatically provides discovery of BUILD.MD. |
| [Agent Skills specification](https://agentskills.io/specification) | A skill is a directory whose required instruction file is **SKILL.md**, singular. It uses YAML frontmatter with required `name` and `description` fields, followed by a Markdown body, and can bundle scripts, references, and assets. The specification recommends progressive loading. | Use the correct filename when comparing conventions. A build specification describes one intended application or change; a skill packages a reusable capability. Keep core build intent in the file while identifying any required external resources precisely. |
| [GitHub Spec Kit quickstart](https://github.github.com/spec-kit/quickstart) | Separates what and why from technical planning, produces dependency-ordered tasks, checks consistency across specification, plan, and tasks, and includes a convergence step against the codebase. Its requirements-quality checklists are distinct from implementation completion. | Preserve those conceptual boundaries within one entry document. Include clarification, implementation planning, verification, and repair prompts. Never confuse a completed document checklist with working software. |
| [Kiro specs documentation](https://kiro.dev/docs/specs/) | Describes requirements or bug analysis, design, and tasks as separate artifacts. Requirements capture user stories and acceptance criteria; design includes architecture and error handling; tasks are discrete and trackable. | Require observable behavior and failure cases, then explain implementation decisions and the work sequence. Single-file packaging should not collapse requirements into a task list. |
| [OpenSpec repository](https://github.com/Fission-AI/OpenSpec) | Demonstrates a change folder containing a proposal, requirements with concrete scenarios, design, and tasks. Its documented flow applies the change and archives it while updating specifications. | Support existing applications as well as new ones. Record the baseline, intended change, behavior that must remain, and how accepted intent is updated after implementation. |

These sources establish relevant conventions and workflows. They do **not**
establish that BUILD.MD is an adopted standard, that any vendor automatically
loads it, or that a complete document guarantees a correct application.

## Filename collision

`BUILD.md` already appears in established repositories as ordinary instructions
for compiling or installing software. Examples include
[KhronosGroup/Vulkan-Headers](https://github.com/KhronosGroup/Vulkan-Headers/blob/main/BUILD.md)
and [cemu-project/Cemu](https://github.com/cemu-project/Cemu/blob/main/BUILD.md).
Those files are evidence of an existing name, not implementations of this
proposal.

**Design implication:** retain the requested `BUILD.MD` name, identify the format
with explicit version metadata, and document the canonical spelling. Do not
assume a file is conforming merely because its filename matches. On a
case-insensitive filesystem, `BUILD.MD` and `BUILD.md` cannot reliably coexist as
different files. Preserve an existing build guide and choose an explicit
non-conflicting location or agreed migration; never silently replace it.

## Proposal analysis

The initial idea is useful: a developer should be able to hand an agent one
document containing the intent, context, prompts, and acceptance contract for a
build. The following changes make that idea more precise and reviewable.

| Initial ambition | Risk | Proposed improvement |
| --- | --- | --- |
| “Everything needed to build” | A document cannot supply credentials, unavailable infrastructure, or unlimited context. | Define completeness as sufficient decision context for the declared scope and environment. State prerequisites, required assets, missing access, and blockers explicitly. Never include live secrets. |
| “All prompts” | Duplicated instructions drift, and example application prompts can be mistaken for instructions to the coding agent. | Include a compact execution prompt set that refers to stable requirement IDs. Separate build prompts, runtime AI prompts, and quoted source material. |
| One file | Large documents can exceed useful context limits; parallel edits can conflict. | Keep essential intent and acceptance rules in one authoritative entry document. Allow explicitly identified supporting resources. Keep generated logs and transcripts outside the spec. |
| A spec drives implementation | Agents may weaken the spec to make existing code appear compliant. | Record changes to accepted requirements with rationale and authority. Verification failures require repair or an explicitly accepted scope change. |
| Agent independence | A format could accidentally depend on a particular product's commands or hidden memory. | Use plain Markdown and portable prose prompts. Document environment requirements and explicit discovery; treat vendor adapters as optional. |
| Autonomous building | A plan may imply permission to publish, purchase, destroy data, or access unrelated accounts. | Separate intended deliverables from the operator's authorization. The file describes work; it does not override runtime permissions or grant external access. |
| A final completion claim | Checkboxes and passing unit tests may omit important behavior. | Trace every mandatory requirement to observable acceptance evidence, including failures, regression checks, and relevant manual checks. Report unverified items honestly. |

## Recommended design decisions

These are proposal decisions, not requirements imposed by the sources above:

1. Define a small, versioned document contract with stable requirement IDs and
   explicit status, scope, and ownership.
2. Keep purpose, context, behavior, technical constraints, execution prompts, and
   verification distinguishable even when they live in one file.
3. Include both a minimal usable example and a fully worked application example.
   Readers should see the expected level of specificity rather than only empty
   template headings.
4. Treat unresolved questions and assumptions as data with consequences. A
   critical ambiguity blocks its dependent work; a reversible implementation
   choice can use a documented default within the operator's authorization.
5. Preserve a persistent product contract across iterations while keeping task
   status and execution evidence clearly separate from accepted requirements.
6. Make linting useful but modest: structural checks can catch missing fields,
   duplicate IDs, and broken traceability. They cannot prove semantic
   completeness, safety, software quality, or actual execution.
7. Start as a published proposal with examples and feedback mechanisms. Claims of
   native support, adoption, reproducibility, or quality gains require separate
   evidence.

## What remains to validate

The next evidence should come from independent implementation trials: give the
same reviewed BUILD.MD to different agents in fresh workspaces, record the
environment and spec revision, and compare observable acceptance outcomes.
Measure missing context, clarification requests, specification changes, failed
checks, and unnecessary features. Include an existing-codebase change and a
resume-after-interruption trial. Results should be reported as observations,
not as a guarantee that future agents will generate identical code.

# Proposal review and resulting design

Three independent agent roles contributed to this initial proposal: primary-source
research, format/tooling design, and adversarial review. The coordinating author
reconciled their findings into the published draft. This records design reasoning;
review agreement is not evidence that a generated application works.

## Changes to the initial idea

| Review finding | Result in v0.1 |
| --- | --- |
| “Everything needed” could imply unlimited context or supplied credentials. | Define sufficient context for a declared scope/environment; name required inputs and blockers, never include live secrets. |
| One file can blur requirements, design, and task tracking. | Retain ten distinct sections; allow short sections and explicit annexes. Keep execution evidence in a separate report. |
| Prompts can duplicate and drift from the contract. | Embed lifecycle prompts that reference requirement/check IDs. Separate builder prompts from runtime AI prompts. |
| Design/build instructions could hide binding obligations without acceptance coverage. | Require every binding product/build constraint to have an R-ID or explicit incorporation in one. Passing inadequate checks cannot excuse known violations. |
| A readiness field could be mistaken for permission or completed software. | Define draft/ready as contract states; keep structural validity, semantic readiness, authorization, and verified implementation distinct. |
| A validator could overclaim what it knows. | Limit it to metadata, sections, IDs, coverage, and template markers. No network requests or embedded command execution. |
| A working-tree label is insufficient to associate evidence with code. | Require a clean commit, a retained dirty-state snapshot with content hash, or immutable source bundle/manifest, plus acceptance dates. |
| BUILD.md already exists in projects as build instructions. | Preserve existing files, avoid case-only duplicates, allow explicit alternate paths, and make no autodiscovery claim. |
| A new standard could become a framework before being tried. | No profiles, inheritance, orchestration syntax, vendor adapters, hosted service, or required installation in v0.1. |

## Specific tradeoffs

**JSON metadata instead of YAML.** Visible JSON supports strict parsing using the
Python standard library. It is slightly more verbose than frontmatter, but avoids
a YAML dependency or a misleading partial YAML parser. The rest remains Markdown.

**Ten headings instead of free-form prose.** A common review surface makes omissions
easier to spot. The compact example demonstrates the scale; the root template is
comprehensive guidance, not a minimum length requirement.

**Living specification instead of automatic regeneration.** Intent stays aligned
with code over time. Direct code editing is permitted; changes must reconcile
the affected contract and evidence. No deterministic source-generation claim is made.

**Single entry point instead of literal single-file storage.** Core intent and
acceptance stay in BUILD.MD. Large versioned fixtures/contracts may be referenced
precisely so a builder can find them and identify missing inputs.

## Example review improvements

The independent semantic review found two concrete issues in the Reading List
draft that structural lint could not detect:

- A URL could meet the input length limit but expand beyond it during encoding,
  producing saved data that would fail reload/import validation. The contract now
  checks both input and canonical URL lengths and includes the regression scenario.
- A valid large export could exceed the original import limit. The import cap now
  accommodates valid exports under the field/item limits, with a maximum-data
  round-trip check.

The Word Count review also clarified integer values in JSON and required literal
LF output bytes on Windows. These revisions demonstrate why prose review and
observable acceptance are needed in addition to structural checks.

## Remaining validation

This repository provides a reviewed proposal and tested structural tooling.
The example applications have not been built as part of this release. Independent
trials should test actual build success, missing context, unnecessary clarifications,
existing-codebase changes, interruption/resume, and maintenance after a requirement
change. Record failures and amendments. No claimed benchmark or vendor compatibility
follows from the current review. See [research](research.md) and
[contributing](../CONTRIBUTING.md) for the evaluation method.

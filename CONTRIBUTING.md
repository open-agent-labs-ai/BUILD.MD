# Contributing

BUILD.MD v0.1 is a proposal. Improvements should make real applications easier
to specify, build, resume, and verify without turning the document into a framework.

## Useful contributions

- A concrete ambiguity, contradiction, or missing piece of build context.
- An implementation trial with the exact contract revision and observable results.
- A smaller or clearer way to express existing requirements.
- A validator defect with a minimal file demonstrating the failure.
- A new example that tests a genuinely different kind of software or change.

Use repository issues for proposals and trial reports. Include evidence rather
than assuming one agent's success proves general compatibility. Remove secrets
and private information before sharing a contract or execution log.

## Change process

1. Explain the problem with a concrete builder/reader scenario.
2. Distinguish normative format changes from guidance or editorial fixes.
3. Update SPEC.md first or in the same change, then reconcile BUILD.MD, examples,
   docs, validator, tests, and CHANGELOG.md as applicable.
4. Run the documented checks. Add regression tests for meaningful tooling changes,
   not tests that merely restate documentation.
5. Explain compatibility and migration for changed conformance rules.

Maintainers decide which proposals to accept through repository review. This
document does not promise external governance, vendor support, or a release date.
During 0.x, a new minor format version may be incompatible. Editorial fixes retain
the format version. Each application contract has its own independent revision.

## Local checks

Python 3.9+ is sufficient; there are no package-install steps.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/lint_build.py BUILD.MD
python3 scripts/lint_build.py --ready examples/word-count/BUILD.MD examples/reading-list/BUILD.MD
```

Lint verifies structure, not completeness or working software. Read example changes
for semantic consistency and follow local Markdown links before submitting.

## Implementation trials

Record the input contract and revision, environment, agent/tool configuration
when available, generated source snapshot, clarifications, amendments, checks
attempted, actual results, and remaining gaps. Keep failed or incomplete attempts
visible. Useful trial dimensions include an empty workspace, an existing codebase,
an interrupted/resumed run, and two independent implementations of the same contract.

## License

Contributions are provided under the repository's [MIT license](LICENSE).

# Working on the BUILD.MD proposal

This repository defines a document format. The root BUILD.MD is a **copyable
draft template**, not the product brief for implementing an application here.
Examples are desired-state contracts; do not generate their applications in this
repo unless the user specifically asks for that work.

Read SPEC.md before changing the format. Keep the template, examples, docs,
validator, tests, and changelog aligned. Separate normative rules from guidance.
Preserve exact filename casing and avoid case-only duplicates.

Use plain Markdown and Python's standard library for the validator. It checks
structure only and must never execute embedded commands or resolve remote inputs.
Add meaningful regression coverage for parser/behavior changes. Do not claim
adoption, automatic agent discovery, semantic conformance from lint, or successful
application builds without evidence.

Run from the repository root with Python 3.9+:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/lint_build.py BUILD.MD
python3 scripts/lint_build.py --ready examples/word-count/BUILD.MD examples/reading-list/BUILD.MD
```

For editorial-only changes, check affected references and examples. For format
changes, review all related artifacts and compatibility implications. Do not
change example acceptance criteria solely to accommodate a failing implementation.

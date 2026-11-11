# Initial proposal validation

Checked on **2026-11-11**, locally on macOS with Python **3.12.14**. The validator
targets Python 3.9+; other Python versions were not executed in this preparation.

| Check | Observed result |
| --- | --- |
| `python3 -m unittest discover -s tests -v` | 23 tests passed. |
| `python3 scripts/lint_build.py BUILD.MD` | Template structurally valid as draft. |
| `python3 scripts/lint_build.py --ready examples/word-count/BUILD.MD examples/reading-list/BUILD.MD` | Both examples structurally valid as ready contracts. |
| Repository Markdown link and text-hygiene inspection | Local file links and referenced headings resolved; no embedded staging paths, CRLF files, or missing final newlines found. |
| Independent semantic review | Corrected constraint coverage, evidence identity, canonical URL limits, backup/import size consistency, and Windows LF output. |

The test suite exercises malformed metadata, duplicate keys, unsupported values,
ID boundaries, missing/repeated sections, fenced sample content, coverage,
placeholders, file/encoding errors, CLI exit codes, and nonexecution of embedded
commands. See [proposal review](proposal-review.md) for the semantic findings.

The GitHub Actions workflow runs the same test/lint commands. It uses read-only
repository permissions and pins checkout to the verified
[v7.0.1 release commit](https://github.com/actions/checkout/commit/3d3c42e5aac5ba805825da76410c181273ba90b1).
GitHub-hosted CI was not run during local preparation. See the repository's
[Actions runs](https://github.com/open-agent-labs-ai/BUILD.MD/actions) for subsequent
CI results.

Neither example application was implemented or executed. Their acceptance checks
are contracts for future builds, not passing test reports. The current evidence
supports the proposal's structure and tooling behavior; effectiveness across
agents, projects, and resumed builds still needs independent implementation trials.

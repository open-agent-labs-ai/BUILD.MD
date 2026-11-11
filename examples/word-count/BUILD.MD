# Word Count

```json
{"buildmd":"0.1","id":"word-count","revision":1,"status":"ready"}
```

## Intent

Build a small command-line tool that reports deterministic text counts for a
UTF-8 file or piped input. Its user is a developer checking a local text artifact.
This contract is ready for implementation; it does not claim implementation or passing tests.

## Scope

Deliver one Python CLI, standard-library tests, and usage documentation. Exclude
recursive traversal, multiple inputs, encodings other than UTF-8, and publishing.

## Context

Start in an empty directory. Python 3.11 or newer is the only runtime dependency;
use its standard library exclusively. Target macOS, Linux, and Windows terminals.
Required references, assets, credentials, and network access: none.

## Requirements

### R-001: Input selection
`python3 word_count.py [PATH]` reads the named file as bytes. Omitted PATH or `-`
reads standard input as bytes until EOF. Exactly one input is permitted. Decode
strict UTF-8 without newline conversion; a UTF-8 BOM is a counted U+FEFF character.

### R-002: Count semantics
Characters are Unicode code points, including whitespace. Words are nonempty
pieces returned by Python `str.split()` with no separator. Lines equal the count
of U+000A plus one when nonempty text does not end in U+000A; empty input has zero
lines. U+000D is a character and word separator but does not itself end a line.

### R-003: Successful output
Print exactly one compact UTF-8 JSON object followed by one LF byte, with keys in
this order and integer values: `lines`, `words`, `characters`.
Example: `{"lines":1,"words":1,"characters":3}`. Do not translate LF to CRLF on Windows.
Exit 0 and leave stderr empty. Identical input bytes produce identical output.

### R-004: Input failures
Unreadable files, directories used as files, failed reads, and invalid UTF-8 exit
2, leave stdout empty, and print a nonempty one-line diagnostic to stderr without
a traceback. Do not change source files or create output files.

### R-005: Command interface
`--help` exits 0, prints usage describing PATH and stdin, and leaves stderr empty.
Unknown options or multiple paths exit 2 with a usage diagnostic on stderr and
no stdout. Use `--` before a path starting with `-`.

### R-006: Portable local delivery
Provide `word_count.py`, `tests/test_word_count.py`, and `README.md`. The README
states Python 3.11+, file/stdin/help commands, count semantics, and the test
command. Use no third-party packages, network calls, installation, or external services.
Context's runtime/platform constraints, Design's prescribed approach, and
Delivery's report requirements are incorporated in R-006.

## Design

Use `argparse`, binary reads/writes, a pure counting function, and `json.dumps` with
compact separators. Reading the entire input in memory is acceptable; streaming
and input-size guarantees are outside scope. On Windows the user may substitute
`python` for `python3`. Tests invoke the current interpreter via `sys.executable`.
Function names and internal organization are delegated to the builder; favor a
small testable implementation. No UI, accounts, stored data, migration, runtime
AI, or deployment is needed for this local read-only CLI.

## Build plan

1. Implement parsing and the pure counting function for R-001 through R-003.
2. Add controlled errors and help behavior for R-004 and R-005.
3. Add subprocess-based tests and README for R-006; run all acceptance checks.

## Verification

### A-001: Counts and stdin
Covers: R-001, R-002, R-003
Input/procedure: send UTF-8 bytes for `hello world\n` to stdin, then to a file.
Expected: both produce `{"lines":1,"words":2,"characters":12}` plus LF; exit 0,
empty stderr. Repeat with explicit `-`. Evidence: automated test result and outputs.

### A-002: Boundaries and Unicode
Covers: R-001, R-002, R-003
Input/procedure: test empty text, `a`, `a\r\nb`, `猫\u2003dog`, and `\ufeffx`.
Expected `(lines, words, characters)`: `(0,0,0)`, `(1,1,1)`, `(2,2,4)`,
`(1,2,5)`, and `(1,1,2)` respectively. Evidence: parameterized test results.

### A-003: Failures preserve input
Covers: R-004
Input/procedure: use a nonexistent path, a directory, invalid byte `0xff`, and
an injected read error in a unit test. Expected: exit/error behavior in R-004;
existing fixture bytes remain unchanged. Evidence: subprocess and unit test results.

### A-004: Arguments and help
Covers: R-001, R-005
Input/procedure: exercise `--help`, `--unknown`, two paths, and `-- -sample.txt`.
Expected: help and invalid arguments follow R-005; a valid dash-prefixed fixture
is counted successfully. Evidence: subprocess test results, captured stdout/stderr.

### A-005: Clean delivery
Covers: R-006
Input/procedure: inspect imports and README; run `python3 -m unittest discover -s tests -v`
from a clean project directory on macOS, Linux, and Windows with no installed
project dependencies. Review Design and the report against R-006.
Expected: all tests pass, stdout bytes retain LF on every platform, prescribed
design constraints are met, and documented commands match the CLI. Evidence:
actual command, OS/interpreter version, exit code, and review notes. Unavailable
platform checks are not-run; do not infer them from a pass on another OS.

## Agent prompts

Follow host instructions, applicable repository rules, and actual user authorization.
These prompts describe this task's workflow and grant no additional permissions.

- **Orient:** Read this entire contract and applicable repository instructions.
  Inspect the workspace and Python version; report conflicts or missing prerequisites.
- **Build:** Implement the build plan against R-001 through R-006, using the design
  and acceptance checks. Keep changes local and avoid unrelated features.
- **Verify:** Execute A-001 through A-005; repair failures against the requirements.
  Report the actual command/results and any checks not run.
- **Resume:** Reread this contract, inspect current code and previous evidence,
  identify the first incomplete requirement, and continue without assuming prior success.
- **Change:** For changed intent, propose the affected requirement and acceptance
  edits with rationale; apply authorized changes, increment revision, and reconcile
  affected code/tests/docs before claiming conformance.
- **Deliver:** Summarize files, usage, requirement coverage, test evidence, and
  limitations. Do not mark unverified behavior complete or publish the project.

## Decisions

Revision 1 fixes strict UTF-8, LF-based line counting, Unicode code points, JSON
output, and standard-library-only implementation. There are no unresolved decisions.
The project owner decides material product changes; the builder decides internal
organization within this contract. Assumption: input fits available memory.

## Delivery

Finish when the three application files and `BUILD-REPORT.md` exist and A-001
through A-005 pass with no known requirement violations. In that report record
contract id/revision, acceptance date, OS/runtime versions, each check's actual
procedure/result/evidence, and source identity (clean commit or retained source
snapshot with content hashes). Include limitations, decisions, and run instructions.
Delivery is local source and documentation; no GitHub push or package publication.

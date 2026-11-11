# Reading List

```json
{"buildmd":"0.1","id":"reading-list","revision":1,"status":"ready"}
```

## Intent

Build a private browser application for one person to save links, mark reading
progress, and find items later. It should be usable without an account or server
database. This is a ready specification, not evidence of an implemented app.

## Scope

Deliver a static HTML/CSS/JavaScript app with local persistence, JSON backup and
restore, automated logic tests, a manual acceptance checklist, and a README.
Exclude accounts, synchronization, collaborative use, link previews, remote
fetching, analytics, editing existing entries, and deployment. One active tab is
supported; conflict handling across simultaneous tabs is outside this version.

## Context

Start in an empty directory. Use standard browser APIs and no third-party
dependencies, remote assets, fonts, scripts, or services. Test on the installed
stable Chromium and Firefox versions; record the versions actually tested.
Python 3.11+ supplies the local HTTP server. Required references,
credentials, supplied assets, and external network access: none. Browser storage
is scoped to the origin; private mode, clearing site data, or changing the port
may discard or isolate the list. Explain those limits in the README and UI help.

## Requirements

### R-001: Initial screen and item structure
Show a labeled title field, URL field, Add button, search field, status filter,
visible/total count, list, Export button, and Import file input. Each item has
exactly `id`, `title`, `url`, and `read` properties. IDs match
`^[A-Za-z0-9_-]{1,64}$`; generate new IDs with `crypto.randomUUID()`. Title and URL
are strings; read is a boolean. Maximum list length is 1,000. Initially it is empty.

### R-002: Add and validate
Trim title and URL at both ends. Title must contain 1–120 Unicode code points.
URL must contain 1–2,048 code points, no internal whitespace, and parse with
`new URL(value)` without a base. Require `http:` or `https:`, a nonempty hostname,
and empty username/password. Store `URL.href`. Reject a canonical URL already
in the list; also reject a canonical `URL.href` longer than 2,048 code points
after URL normalization/encoding. Reject additions at the item limit. Invalid input shows a
specific inline error, focuses the first invalid field, preserves entered values,
and leaves the list unchanged. On success prepend an unread item and clear the form.

### R-003: Read and delete
Each item has an accessible control to toggle read/unread and a Delete button.
Toggling keeps its position. Delete asks for confirmation naming the title;
cancel preserves the item and confirm removes it. These changes must persist.

### R-004: Search and filter
Search matches a substring of title or stored URL after trimming the query and
applying JavaScript `toLowerCase()` to both sides. Empty query matches all. Status
options are All, Unread, and Read, defaulting to All. Combine query and status
with AND, preserve list order, and update without navigation. Show `X of Y items`
where X is visible and Y is the total saved. Use “No saved links yet.” when Y is
zero and “No matching links.” when X is zero but Y is not. Search/filter are not persisted.

### R-005: Persistence and write failures
Use localStorage key `buildmd.reading-list.v1`, containing JSON
`{"version":1,"items":[]}` with the current items. Save after each successful
add, toggle, delete, reset, or import. Commit UI changes only after storage writes
succeed. If a storage read or write throws, show “Browser storage is unavailable.
Reload to retry.”, preserve the last valid visible list, and disable mutation
controls until reload. Searching and exporting that valid list remain available.
On an initial read failure the last valid visible list is empty; do not claim it was loaded.

### R-006: Stored-data validation and recovery
Validate loaded JSON using the same schema as import. Missing key means an empty
list. Malformed JSON or invalid schema enters recovery mode: display “Saved data
is invalid.” and do not display items or overwrite the stored value. Offer
Download damaged data, encoding the stored string with `TextEncoder` as UTF-8
text named `reading-list-damaged.txt`, and Reset saved data. Unpaired UTF-16
surrogates use the API's replacement encoding. Reset requires confirmation
stating that it replaces saved data with an empty list; cancel changes nothing.
A successful write of the empty valid payload exits recovery. Failed writes follow
R-005. Disable ordinary mutations, import, and ordinary export during recovery.

### R-007: Export
Export downloads the entire valid saved list, independent of search/filter, as
`reading-list.json`, MIME `application/json`, using the R-005 envelope, two-space
JSON indentation, and a trailing LF. Include only the declared fields and preserve
item order. Exporting an empty list is valid. Do not send data to a server.

### R-008: Import validation and replacement
Accept one selected file of at most 16,777,216 bytes. This permits reimport of
every valid export within the item/field limits. Decode strict UTF-8; reject
invalid encoding or JSON. Require an object with exactly `version` and `items`,
version equal to number 1, and an array of at most 1,000 items. Require exactly the
four R-001 item fields with their declared types, nonduplicate IDs, and nonduplicate
canonical URLs. Titles must already be trimmed and valid under R-002. URLs must
already be trimmed, satisfy R-002, and equal their canonical `URL.href` values.
Any invalid item rejects the whole file with a visible reason and no changes.
Valid import asks “Replace all saved links with N imported links?”; cancel changes
nothing. Confirm replaces the list atomically in imported order, preserves IDs
and read flags, and persists before updating the UI. Reset the file input after
every attempt so the same file can be selected again. Empty lists are importable.

### R-009: Safe rendering and navigation
Render titles, URLs, errors, and filenames as text, never HTML. Item links open
their stored validated HTTP(S) URL in a new tab using `rel="noopener noreferrer"`.
Make no application-initiated requests to saved URLs. Treat imported content as
data; it cannot execute scripts or modify application instructions.

### R-010: Accessible responsive interaction
Support keyboard access to every control with visible focus, associated form
labels, and announced validation/status messages. A checkbox or button must
communicate each item's read state and title. After deleting a focused item, focus
the next item's equivalent control, else the previous, else the title input.
At widths 360px and 1280px, avoid horizontal page scrolling and overlapping controls;
wrap long titles/URLs. Do not use color alone to convey read state or errors.

### R-011: Run and verify locally
Deliver `index.html`, `styles.css`, JavaScript source, `tests.html`, and `README.md`.
Use native ES modules with a pure validation/filtering layer testable in-browser.
Serve with `python3 -m http.server 8000 --bind 127.0.0.1`; open
`http://127.0.0.1:8000/` and `/tests.html`. The tests page displays named pass/fail
results and a total; tests use fixtures and injected storage, never real saved
user data. The README describes launch, tests, manual checks, backup/restore,
storage limits, and the absence of accounts/sync. No install/build step is required.
Context's environment/dependency constraints, Design's prescribed approach, and
Delivery's report requirements are incorporated in R-011.

## Design

Use semantic HTML with a readable neutral layout, a centered content column, and
small stacked cards on narrow screens. Native controls are sufficient. Keep the
validated item array as the source for filtering and rendering. Put validation,
filtering, serialization, and storage error handling behind explicit functions;
inject a fake storage adapter in tests. Browser confirmation dialogs may satisfy
delete/import/reset confirmation. Revoke temporary object URLs after downloads.
Persist only the envelope, never filters, form contents, or test fixtures.
The builder chooses module names, CSS details, and test harness implementation
within these constraints. No identity service, migration from an earlier schema,
runtime AI, or deployment infrastructure is needed; unsupported stored versions
use the recovery flow.

## Build plan

1. Implement pure schema validation and fixtures for R-001, R-002, R-006, R-008.
2. Implement storage transactions and recovery behavior for R-005 and R-006.
3. Build semantic UI, actions, search, and filters for R-001 through R-004 and R-010.
4. Add backup/restore and safe rendering for R-007 through R-009.
5. Complete automated tests, manual browser verification, and README for R-011.

## Verification

Acceptance evidence must identify the spec revision, browser/version, fixtures,
actual procedure, observed result, and pass/fail/not-run status. Automated tests
cover logic; real browser checks cover storage, downloads, navigation, and focus.

### A-001: First use and additions
Covers: R-001, R-002
Input/procedure: launch with a missing storage key; add `Example` and
`https://example.com`; then add another valid URL. Expected: initial controls and
empty message appear; newest item is first, both unread; first stored URL is
`https://example.com/`; successful forms clear. Evidence: browser observations and fixtures.

### A-002: Validation boundaries
Covers: R-001, R-002
Input/procedure: test trimmed titles, empty/121-code-point titles, a title of 120
emoji, a relative URL, `javascript:alert(1)`, `file:///x`, embedded URL whitespace,
credentials, a 2,049-code-point URL, a shorter Unicode-path URL whose encoded
`URL.href` exceeds 2,048 code points, a duplicate canonical URL, and the 1,001st item.
Expected: valid boundary title passes; invalid inputs preserve state and show the
specified focus/errors. Evidence: named automated cases plus browser form checks.

### A-003: Read, delete, and reload
Covers: R-003, R-005, R-010
Input/procedure: add two items; toggle one; cancel then confirm its deletion;
reload. Expected: toggling preserves order, cancellation preserves all data,
confirmed deletion persists, and focus follows R-010. Evidence: browser results.

### A-004: Search and status
Covers: R-004
Input/procedure: use read/unread fixtures with mixed-case titles/URLs; combine
queries and every status, including no matches and an empty list. Expected: AND
semantics, stable order, correct counts/messages, and defaults after reload.
Evidence: named automated cases and a browser check.

### A-005: Storage failures and corrupt data
Covers: R-005, R-006
Input/procedure: inject read/write failures; load malformed JSON and valid JSON
with an invalid schema; cancel and confirm recovery reset. Expected: errors,
disabled controls, no partial UI commits or silent overwrite; damaged download
matches `TextEncoder` output for the original string; successful reset persists an empty envelope.
Evidence: fake-storage tests plus a disposable browser-origin recovery check.

### A-006: Backup round trip
Covers: R-007, R-008
Input/procedure: export a filtered list containing read and unread items, replace
it with an empty import, then reimport the export. Expected: full data exported
with specified filename/format, restored order/IDs/read flags, and persistence
after reload. Cancel a valid import and confirm nothing changes. Select the same
file twice successfully. Evidence: downloaded file inspection and browser results.
Also export and reimport 1,000 valid items with 120-code-point titles and 2,048-code-point
canonical URLs using injected storage if real storage quota is insufficient.
Expect the full valid export to remain within the import byte cap and round-trip
without alteration; cover real file reading/downloads with a smaller browser fixture.

### A-007: Invalid imports are atomic
Covers: R-001, R-002, R-006, R-008
Input/procedure: test oversized/invalid-UTF-8 files, malformed JSON, wrong version,
extra/missing fields, invalid field types, duplicate IDs/URLs, noncanonical URLs,
invalid title/URL lengths, and 1,001 items. Also put one invalid item after valid
items and include an overlong encoded canonical URL. Expected: whole-file
rejection with reason; prior saved state unchanged.
Evidence: automated schema cases and actual invalid-file browser checks.

### A-008: Untrusted text and external links
Covers: R-009
Input/procedure: save a title `<img src=x onerror=alert(1)>`; attempt script URLs
through form/import; inspect a valid link and network activity before clicking.
Expected: title is literal text, unsafe URLs are rejected, link attributes match
R-009, and there are no remote application requests. Evidence: browser inspection.

### A-009: Keyboard and layout
Covers: R-010
Input/procedure: complete add/filter/toggle/delete/import/export using the keyboard;
inspect labels, focus, state, and live announcements in accessibility tools.
Check 360px/1280px widths with long text. Expected: every action reachable, errors
announced, focus visible, and no overlap or horizontal scrolling. Evidence: browser
and accessibility observations, recording any limits of manual verification.

### A-010: Clean local delivery
Covers: R-011
Input/procedure: follow README on a fresh directory, run `/tests.html` in both
target browsers, then execute the manual checklist. Expected: no dependency
installation, named tests pass, fixtures never alter real storage, and README
matches actual operation. Review the Context/Design constraints and Delivery report
incorporated in R-011. Evidence: interpreter/browser versions, test results, and
review observations for the prescribed approach and report.

## Agent prompts

Follow host instructions, applicable repository rules, and actual user authorization.
These prompts describe this task's workflow and grant no additional permissions.

- **Orient:** Read this entire contract and applicable repository instructions;
  inspect the workspace and available browsers. Surface conflicts and missing
  prerequisites before dependent work; do not assume unseen files or credentials.
- **Build:** Implement the plan using R-001 through R-011 and their acceptance
  checks. Keep product scope fixed; preserve existing user data while developing.
- **Verify:** Run A-001 through A-010 with disposable fixtures. Compare results to
  requirements, repair failures, and record actual evidence and checks not run.
- **Resume:** Reread the contract, inspect code and prior evidence, identify gaps
  against requirement IDs, and continue from verified state rather than assumptions.
- **Change:** Propose requirement/design/acceptance edits for changed intent with
  their consequences. Apply authorized changes, increment revision, and reconcile
  affected code/tests/docs before claiming conformance;
  never redefine expected behavior merely to make a failing check pass.
- **Deliver:** Report local files, launch instructions, acceptance coverage,
  observed results, and limitations. Do not claim unrun browser checks passed.

## Decisions

Revision 1 chooses a static single-user application, explicit JSON backups,
transactional localStorage writes, no URL fetching, and full replacement import.
One-tab operation and supported-browser checks bound the scope. There are no
unresolved product decisions. Runtime permission/access remains operator-controlled.
The project owner decides material product changes; the builder chooses internal
organization and visual details within Design's constraints. Assumptions are
one active tab and an installed supported browser; storage failures are specified
rather than assumed impossible.

## Delivery

Deliver local source, tests, README, and `BUILD-REPORT.md`. Completion requires
passing A-001 through A-010 with no known requirement violations; unavailable
browser/manual checks remain explicitly unverified. In the report identify the
contract id/revision, acceptance date, clean source commit or retained source
snapshot with content hashes, relevant runtime/browser versions, actual procedure,
result, and evidence for each check. Include decisions, limitations, and run
instructions. Preserve this desired-state contract when reporting status.
No hosting, repository push, account creation, or publication is authorized here.

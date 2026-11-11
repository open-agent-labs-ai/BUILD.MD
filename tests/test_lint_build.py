"""Behavioral and parser-boundary tests for the optional structural checker."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts.lint_build import lint_file, lint_text


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "lint_build.py"


def document(status="draft", metadata=None, sections=None):
    data = {"buildmd": "0.1", "id": "small-app", "revision": 1, "status": status}
    if metadata:
        data.update(metadata)
    bodies = {name: "A concrete statement." for name in (
        "Intent", "Scope", "Context", "Requirements", "Design", "Build plan",
        "Verification", "Agent prompts", "Decisions", "Delivery",
    )}
    bodies["Requirements"] = "### R-001: Save a note\nA note persists after a restart."
    bodies["Verification"] = "### A-001: Persistence\nCovers: R-001\nSave a note, restart, and compare its text."
    if sections:
        bodies.update(sections)
    return "# Small app\n\n```json\n" + json.dumps(data, indent=2) + "\n```\n\n" + "\n\n".join(
        "## " + name + "\n\n" + body for name, body in bodies.items()
    ) + "\n"


class StructuralValidationTests(unittest.TestCase):
    def assert_valid(self, text, **kwargs):
        result = lint_text(text, **kwargs)
        self.assertEqual([], result.diagnostics, result.diagnostics)
        return result

    def assert_error(self, text, fragment, **kwargs):
        result = lint_text(text, **kwargs)
        self.assertTrue(any(fragment in diagnostic.message for diagnostic in result.diagnostics), result.diagnostics)
        return result

    def test_draft_and_ready_are_supported_without_claiming_semantics(self):
        self.assertEqual("draft", self.assert_valid(document()).status)
        self.assertEqual("ready", self.assert_valid(document("ready"), require_ready=True).status)
        self.assert_error(document(), "--ready requires", require_ready=True)

    def test_metadata_required_keys_types_and_extension_namespace(self):
        bad = [
            ({"buildmd": 0.1}, "buildmd must"),
            ({"revision": True}, "positive integer"),
            ({"revision": 0}, "positive integer"),
            ({"revision": 1.0}, "positive integer"),
            ({"revision": "1"}, "positive integer"),
            ({"status": []}, "status must"),
            ({"status": "approved"}, "status must"),
            ({"unknown": "value"}, "unknown metadata key"),
        ]
        for metadata, message in bad:
            with self.subTest(metadata=metadata):
                self.assert_error(document(metadata=metadata), message)
        self.assert_valid(document(metadata={"x-owner": {"team": "docs"}}))
        self.assert_error(document().replace('  "revision": 1,\n', ""), "missing metadata key 'revision'")

    def test_id_boundaries_are_ascii_and_single_hyphen_separated(self):
        for value in ("a", "0", "a0-b9", "a" * 64):
            with self.subTest(value=value):
                self.assert_valid(document(metadata={"id": value}))
        for value in ("", "a" * 65, "A", "café", "a_b", "a--b", "-a", "a-", "a b", 7, None):
            with self.subTest(value=value):
                self.assert_error(document(metadata={"id": value}), "id must")

    def test_duplicate_json_keys_are_rejected_including_extensions(self):
        self.assert_error(document().replace('"revision": 1', '"revision": 1, "revision": 2'), "duplicate JSON key 'revision'")
        self.assert_error(document().replace('"revision": 1', '"revision": 1, "x-data": {"a": 1, "a": 2}'), "duplicate JSON key 'a'")

    def test_invalid_json_and_nonstandard_constants_are_rejected(self):
        self.assert_error(document().replace('"revision": 1', '"revision": NaN'), "not a JSON value")
        self.assert_error(document().replace('"revision": 1', '"revision": Infinity'), "not a JSON value")
        self.assert_error(document().replace('"revision": 1', '"revision": '), "invalid metadata JSON")
        text = document()
        start, end = text.index("{\n"), text.index("\n```", text.index("{\n"))
        self.assert_error(text[:start] + "[]" + text[end:], "JSON object")

    def test_metadata_fence_and_position_are_checked(self):
        self.assert_error(document().replace("```json", "```yaml", 1), "first fenced block")
        self.assert_error(document().replace("```json", "~~~json", 1).replace("\n```", "\n~~~", 1), "first fenced block")
        self.assert_error(document().replace("```json", "````json", 1).replace("\n```\n", "\n````\n", 1), "first fenced block")
        self.assert_error(document().replace("\n```\n", "\n````\n", 1), "exactly three backticks")
        self.assert_error(document().replace("# Small app\n", "# Small app\n\n## Background\n\nText.\n", 1), "metadata must precede")
        self.assert_error(document().replace("# Small app\n", "# Small app\n\n```text\nnot metadata\n```\n", 1), "first fenced block")

    def test_json_runtime_limits_have_diagnostics_instead_of_tracebacks(self):
        # Actual JSON recursion/number limits vary between supported runtimes.
        for failure in (RecursionError("nesting limit"), ValueError("integer limit")):
            with self.subTest(failure=failure), patch("scripts.lint_build.json.loads", side_effect=failure):
                self.assert_error(document(), "parsing limits")

    def test_h1_and_exact_required_sections(self):
        self.assert_error("\n" + document(), "must begin")
        self.assert_error(document().replace("# Small app", "# ", 1), "must begin")
        self.assert_error(document() + "\n# Another title\n", "only one level-1")
        self.assert_error(document().replace("## Intent", "## intent"), "missing required section ## Intent")
        self.assert_error(document() + "\n## Intent\nRepeated.\n", "duplicate required section ## Intent")
        self.assert_error(document(sections={"Scope": "\n\t\n"}), "section ## Scope must have nonempty")
        self.assert_error(document(sections={"Scope": "### A subordinate heading"}), "section ## Scope must have nonempty")

    def test_sections_may_be_reordered_and_optional_sections_added(self):
        text = document()
        prefix, remainder = text.split("## Intent", 1)
        sections = ("## Intent" + remainder).split("\n\n## ")
        reordered = [sections[0]] + ["## " + item for item in sections[1:]]
        self.assert_valid(prefix + "\n\n".join(reversed(reordered)) + "\n\n## Glossary\nA note is plain text.\n")

    def test_fenced_headings_and_ids_do_not_affect_structure(self):
        for opener, closer in (("```text", "```"), ("~~~~md", "~~~~"), ("````markdown", "`````")):
            with self.subTest(opener=opener):
                fake = opener + "\n# Extra title\n## Requirements\n### R-001: Duplicate\n### A-999: Fake\nCovers: R-999\n" + closer
                self.assert_valid(document(sections={"Context": fake}))

    def test_short_or_different_fence_does_not_close_code(self):
        code = "````text\n```\n~~~\n## Requirements\n### R-001: Duplicate\n````\n"
        self.assert_valid(document(sections={"Context": code}))
        self.assert_error(document() + "\n~~~text\n## Intent\n", "unclosed fenced code block")

    def test_empty_code_does_not_satisfy_nonempty_section(self):
        self.assert_error(document(sections={"Context": "```text\n\n```"}), "section ## Context must have nonempty")

    def test_definition_shape_depth_location_and_range(self):
        for title in ("R-000: Bad", "R-01: Bad", "R-1000: Bad", "r-001: Bad", "R001: Bad", "R-abc: Bad", "R-001:", "R-001:   "):
            with self.subTest(title=title):
                self.assert_error(document().replace("R-001: Save a note", title), "malformed ID heading")
        self.assert_error(document().replace("### R-001: Save", "#### R-001: Save"), "must be a level-3")
        self.assert_error(document(sections={"Context": "### R-002: Misplaced\nSome behavior."}), "within ## Requirements")
        self.assert_error(document(sections={"Requirements": "### A-002: Misplaced\nSome behavior."}), "within ## Verification")
        self.assert_valid(document().replace("R-001", "R-999").replace("A-001", "A-999"))

    def test_requirement_and_acceptance_duplicates_and_empty_bodies(self):
        self.assert_error(document(sections={"Requirements": "### R-001: One\nFirst.\n### R-001: Two\nSecond."}), "duplicate R-001")
        self.assert_error(document(sections={"Verification": "### A-001: One\nCovers: R-001\nFirst.\n### A-001: Two\nCovers: R-001\nSecond."}), "duplicate A-001")
        self.assert_error(document(sections={"Requirements": "### R-001: Empty"}), "R-001 must have a nonempty body")
        self.assert_error(document(sections={"Verification": "### A-001: Empty"}), "A-001 must have a nonempty body")
        self.assert_error(document(sections={"Requirements": "No definitions."}), "define at least one ### R-001")
        self.assert_error(document(sections={"Verification": "No checks."}), "define at least one ### A-001")

    def test_acceptance_requires_exactly_one_plain_covers_line(self):
        for replacement, fragment in (
            ("No mapping.", "exactly one plain Covers"),
            ("Covers: R-001\nCovers: R-001", "exactly one plain Covers"),
            ("Covers: R-001,R-002", "comma-space separators"),
            ("Covers: R-001,  R-002", "comma-space separators"),
            ("Covers: R-001, R-001", "duplicate requirement IDs"),
            ("Covers: R-999", "undefined requirement R-999"),
            (" Covers: R-001", "plain Covers"),
            ("- Covers: R-001", "exactly one plain Covers"),
            ("```text\nCovers: R-001\n```", "exactly one plain Covers"),
        ):
            with self.subTest(replacement=replacement):
                self.assert_error(document().replace("Covers: R-001", replacement), fragment)

    def test_many_to_many_coverage_and_uncovered_requirement(self):
        requirements = "### R-001: Save\nPersist text.\n### R-002: Read\nRetrieve text."
        checks = "### A-001: Round trip\nCovers: R-001, R-002\nCompare saved and retrieved text.\n### A-002: Restart\nCovers: R-001\nRestart and compare."
        self.assert_valid(document(sections={"Requirements": requirements, "Verification": checks}))
        self.assert_error(document(sections={"Requirements": requirements}), "R-002 is not covered")

    def test_nested_headings_do_not_truncate_requirement_body(self):
        requirements = "### R-001: Save\n#### Details\nPersist text."
        checks = "### A-001: Save check\n#### Procedure\nCovers: R-001\nRestart and inspect."
        self.assert_valid(document(sections={"Requirements": requirements, "Verification": checks}))

    def test_placeholders_allowed_in_draft_but_rejected_everywhere_in_ready(self):
        for extra in ("Use {{runtime}}.", "```text\n{{placeholder}}\n```", "{{multi\nline}}"):
            with self.subTest(extra=extra):
                self.assert_valid(document(sections={"Context": extra}))
                self.assert_error(document("ready", sections={"Context": extra}), "must replace {{...}}")
        self.assert_error(document("ready", metadata={"x-note": "{{todo}}"}), "must replace {{...}}")

    def test_json_diagnostic_reports_the_source_line(self):
        text = document().replace('  "revision": 1,', '  "revision": nope,')
        result = self.assert_error(text, "invalid metadata JSON")
        diagnostic = next(item for item in result.diagnostics if "invalid metadata JSON" in item.message)
        self.assertEqual(text.splitlines().index('  "revision": nope,') + 1, diagnostic.line)


class FileAndCliTests(unittest.TestCase):
    def run_cli(self, *arguments):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, arguments)], capture_output=True, text=True, check=False)

    def test_utf8_and_unreadable_files_fail_cleanly(self):
        with tempfile.TemporaryDirectory() as directory:
            invalid = Path(directory) / "invalid.md"
            invalid.write_bytes(b"\xff")
            self.assertIn("not valid UTF-8", lint_file(str(invalid)).diagnostics[0].message)
            self.assertIn("cannot read file", lint_file(str(invalid) + ".missing").diagnostics[0].message)

    def test_cli_multiple_files_success_failure_and_ready(self):
        with tempfile.TemporaryDirectory() as directory:
            draft, ready = Path(directory) / "draft.md", Path(directory) / "ready.md"
            draft.write_text(document(), encoding="utf-8")
            ready.write_text(document("ready"), encoding="utf-8")
            result = self.run_cli(draft, ready)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(2, result.stdout.count("semantic review still required"))
            self.assertIn("structure valid (draft)", result.stdout)
            self.assertIn("structure valid (ready)", result.stdout)
            result = self.run_cli("--ready", draft, ready)
            self.assertEqual(1, result.returncode)
            self.assertIn(str(draft) + ":1: error:", result.stderr)
            self.assertIn(str(ready) + ": structure valid", result.stdout)
            self.assertEqual(1, self.run_cli(Path(directory) / "missing.md").returncode)

    def test_cli_misuse_returns_two(self):
        self.assertEqual(2, self.run_cli().returncode)
        self.assertEqual(2, self.run_cli("--unknown").returncode)

    def test_code_and_extensions_are_never_executed_or_followed(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "should-not-exist"
            content = document(metadata={"x-run": "touch " + str(marker)}, sections={
                "Build plan": "```sh\ntouch " + str(marker) + "\n```",
                "Context": "Reference: https://invalid.example/nonexistent",
            })
            path = Path(directory) / "BUILD.MD"
            path.write_text(content, encoding="utf-8")
            self.assertEqual(0, self.run_cli(path).returncode)
            self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()

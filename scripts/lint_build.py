#!/usr/bin/env python3
"""Check BUILD.MD structure without executing commands or resolving references.

This limited structural checker does not establish full conformance, semantic
completeness, security, or implementation correctness. Requires Python 3.9+;
uses only the standard library.
"""

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple


REQUIRED_SECTIONS = (
    "Intent", "Scope", "Context", "Requirements", "Design", "Build plan",
    "Verification", "Agent prompts", "Decisions", "Delivery",
)
REQUIRED_KEYS = {"buildmd", "id", "revision", "status"}
HEADING = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+(.*?))?[ \t]*$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
IDENTIFIER = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DEFINITION_LIKE = re.compile(r"^[RrAa](?:-|[0-9]|[ \t]+[0-9])")
DEFINITION = re.compile(r"^([RA]-[0-9]{3}):[ \t]+(\S.*)$")
COVERS = re.compile(r"^Covers: (R-[0-9]{3}(?:, R-[0-9]{3})*)[ \t]*$")
PLACEHOLDER = re.compile(r"\{\{[\s\S]*?\}\}")


@dataclass(frozen=True)
class Diagnostic:
    line: int
    message: str


@dataclass
class Result:
    filename: str
    status: Optional[str]
    diagnostics: List[Diagnostic]


@dataclass(frozen=True)
class Heading:
    line: int
    level: int
    title: str


@dataclass
class CodeBlock:
    line: int
    fence: str
    info: str
    lines: List[str]
    closed: bool = False
    closing_fence: Optional[str] = None


class MetadataError(ValueError):
    """JSON syntax that Python accepts but this format does not."""


def _unique_object(pairs: List[Tuple[str, Any]]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise MetadataError("duplicate JSON key {!r}".format(key))
        result[key] = value
    return result


def _invalid_constant(value: str) -> None:
    raise MetadataError("{} is not a JSON value".format(value))


def lint_text(text: str, filename: str = "<string>", require_ready: bool = False) -> Result:
    """Validate one document. Do not execute commands or follow references."""
    lines = text.splitlines()
    diagnostics: List[Diagnostic] = []
    headings: List[Heading] = []
    blocks: List[CodeBlock] = []
    # Plain lines exclude code; content includes code but excludes delimiters
    # and headings, so a section with only headings is not considered nonempty.
    plain: Dict[int, str] = {}
    content: Dict[int, str] = {}
    active: Optional[CodeBlock] = None

    def error(line: int, message: str) -> None:
        diagnostics.append(Diagnostic(line, message))

    for number, line in enumerate(lines, 1):
        fence = FENCE.match(line)
        if active is not None:
            if (fence and fence.group(1)[0] == active.fence[0]
                    and len(fence.group(1)) >= len(active.fence)
                    and not fence.group(2).strip()):
                active.closed = True
                active.closing_fence = fence.group(1)
                active = None
            else:
                active.lines.append(line)
                content[number] = line
            continue
        if fence and not (fence.group(1)[0] == "`" and "`" in fence.group(2)):
            active = CodeBlock(number, fence.group(1), fence.group(2).strip(), [])
            blocks.append(active)
            continue
        plain[number] = line
        heading = HEADING.match(line)
        if heading:
            title = heading.group(2) or ""
            # CommonMark permits a whitespace-separated closing hash sequence.
            title = re.sub(r"[ \t]+#+[ \t]*$", "", title).strip()
            headings.append(Heading(number, len(heading.group(1)), title))
        else:
            content[number] = line

    if active is not None:
        error(active.line, "unclosed fenced code block")

    h1s = [heading for heading in headings if heading.level == 1]
    if not h1s or h1s[0].line != 1 or not h1s[0].title:
        error(1, "document must begin with a nonempty level-1 heading (# Title)")
    for heading in h1s[1:]:
        error(heading.line, "only one level-1 heading is allowed")

    first_h2 = next((heading.line for heading in headings if heading.level == 2), None)
    status: Optional[str] = None
    if not blocks:
        error(1, "add a fenced json metadata object before the first level-2 heading")
    else:
        block = blocks[0]
        if block.fence != "```" or block.info != "json":
            error(block.line, "the first fenced block must open with ```json metadata")
        if block.closed and block.closing_fence != "```":
            error(block.line, "metadata must close with exactly three backticks")
        if first_h2 is not None and block.line >= first_h2:
            error(block.line, "metadata must precede the first level-2 heading")
        if block.closed and block.fence == "```" and block.info == "json":
            try:
                metadata = json.loads("\n".join(block.lines), object_pairs_hook=_unique_object,
                                      parse_constant=_invalid_constant)
            except json.JSONDecodeError as exc:
                error(block.line + exc.lineno, "invalid metadata JSON: " + exc.msg)
            except MetadataError as exc:
                error(block.line, "invalid metadata JSON: " + str(exc))
            except (RecursionError, ValueError) as exc:
                error(block.line, "metadata JSON exceeds this Python runtime's parsing limits: " + str(exc))
            else:
                if not isinstance(metadata, dict):
                    error(block.line, "metadata must be a JSON object")
                else:
                    for key in sorted(REQUIRED_KEYS - metadata.keys()):
                        error(block.line, "missing metadata key {!r}".format(key))
                    for key in sorted(metadata.keys() - REQUIRED_KEYS):
                        if not key.startswith("x-"):
                            error(block.line, "unknown metadata key {!r}; extensions must start with x-".format(key))
                    if "buildmd" in metadata and metadata["buildmd"] != "0.1":
                        error(block.line, "buildmd must be the string \"0.1\"")
                    if "id" in metadata:
                        identifier = metadata["id"]
                        if (not isinstance(identifier, str) or not 1 <= len(identifier) <= 64
                                or not IDENTIFIER.fullmatch(identifier)):
                            error(block.line, "id must be 1-64 lowercase ASCII letters/digits, with single hyphens between segments")
                    if "revision" in metadata and (type(metadata["revision"]) is not int or metadata["revision"] <= 0):
                        error(block.line, "revision must be a positive integer (not a boolean)")
                    if "status" in metadata:
                        if isinstance(metadata["status"], str) and metadata["status"] in ("draft", "ready"):
                            status = metadata["status"]
                        else:
                            error(block.line, "status must be \"draft\" or \"ready\"")
    if require_ready and status != "ready":
        error(1, "--ready requires metadata status \"ready\"")
    if status == "ready":
        for marker in PLACEHOLDER.finditer(text):
            error(text.count("\n", 0, marker.start()) + 1, "ready documents must replace {{...}} template markers")

    def body_end(heading: Heading) -> int:
        return next((other.line for other in headings
                     if other.line > heading.line and other.level <= heading.level), len(lines) + 1)

    def has_body(heading: Heading) -> bool:
        end = body_end(heading)
        return any(heading.line < number < end and value.strip()
                   for number, value in content.items())

    for name in REQUIRED_SECTIONS:
        matches = [heading for heading in headings if heading.level == 2 and heading.title == name]
        if not matches:
            error(1, "missing required section ## " + name)
        for heading in matches[1:]:
            error(heading.line, "duplicate required section ## " + name)
        for heading in matches:
            if not has_body(heading):
                error(heading.line, "section ## {} must have nonempty content".format(name))

    requirements: Dict[str, Heading] = {}
    acceptance: Dict[str, Heading] = {}
    seen: Dict[str, Heading] = {}
    section: Optional[str] = None
    for heading in headings:
        if heading.level <= 2:
            section = heading.title if heading.level == 2 else None
        if not DEFINITION_LIKE.match(heading.title):
            continue
        match = DEFINITION.fullmatch(heading.title)
        if not match or match.group(1)[2:] == "000":
            error(heading.line, "malformed ID heading; use ### R-001: Title or ### A-001: Title (001-999)")
            continue
        identifier = match.group(1)
        expected = "Requirements" if identifier.startswith("R-") else "Verification"
        if heading.level != 3 or section != expected:
            error(heading.line, "{} must be a level-3 heading within ## {}".format(identifier, expected))
        if identifier in seen:
            error(heading.line, "duplicate {} definition; first defined on line {}".format(identifier, seen[identifier].line))
        else:
            seen[identifier] = heading
        if heading.level == 3 and section == expected:
            target = requirements if identifier.startswith("R-") else acceptance
            target.setdefault(identifier, heading)
        if not has_body(heading):
            error(heading.line, "{} must have a nonempty body".format(identifier))

    if not requirements:
        error(1, "## Requirements must define at least one ### R-001: Title")
    if not acceptance:
        error(1, "## Verification must define at least one ### A-001: Title")

    covered = set()
    for identifier, heading in acceptance.items():
        end = body_end(heading)
        candidates = [(number, value) for number, value in plain.items()
                      if heading.line < number < end and value.lstrip().startswith("Covers:")]
        if len(candidates) != 1:
            error(heading.line, "{} must contain exactly one plain Covers: R-001, R-002 line".format(identifier))
        for number, value in candidates:
            match = COVERS.fullmatch(value)
            if not match:
                error(number, "use a plain Covers: R-001, R-002 line with comma-space separators")
                continue
            references = match.group(1).split(", ")
            if len(references) != len(set(references)):
                error(number, "Covers contains duplicate requirement IDs")
            for reference in references:
                if reference not in requirements:
                    error(number, "Covers references undefined requirement " + reference)
                else:
                    covered.add(reference)
    for identifier, heading in requirements.items():
        if identifier not in covered:
            error(heading.line, identifier + " is not covered by any acceptance check")

    return Result(filename, status, sorted(diagnostics, key=lambda item: item.line))


def lint_file(filename: str, require_ready: bool = False) -> Result:
    try:
        text = Path(filename).read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return Result(filename, None, [Diagnostic(1, "file is not valid UTF-8: " + str(exc))])
    except OSError as exc:
        return Result(filename, None, [Diagnostic(1, "cannot read file: " + str(exc))])
    return lint_text(text, filename, require_ready)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ready", action="store_true", help="also require status ready")
    parser.add_argument("files", nargs="+", metavar="FILE", help="explicit BUILD.MD path(s) to inspect")
    args = parser.parse_args(argv)
    failed = False
    for filename in args.files:
        result = lint_file(filename, args.ready)
        if result.diagnostics:
            failed = True
            for diagnostic in result.diagnostics:
                print("{}:{}: error: {}".format(filename, diagnostic.line, diagnostic.message), file=sys.stderr)
        else:
            print("{}: structure valid ({}); semantic review still required".format(filename, result.status))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

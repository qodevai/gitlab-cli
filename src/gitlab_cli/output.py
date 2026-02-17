"""Output formatting — JSON and Markdown modes."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from typing import Any

from rich.console import Console
from rich.markdown import Markdown

from gitlab_cli.context import Context

console = Console(stderr=True)
stdout_console = Console()


def serialize(obj: Any) -> Any:
    """Convert an object to a JSON-serializable structure."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, list):
        return [serialize(item) for item in obj]
    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    return obj


def output_json(data: Any) -> None:
    print(json.dumps(serialize(data), indent=2, default=str))


def output_markdown(text: str) -> None:
    stdout_console.print(Markdown(text))


def output(data: Any, *, ctx: Context, format_fn: Any = None) -> None:
    """Route output through the correct formatter."""
    if ctx.json_mode:
        output_json(data)
    else:
        if format_fn:
            md = format_fn(data)
        else:
            md = generic_markdown(data)
        output_markdown(md)


def output_list(
    *,
    items: list[Any],
    total: int | None = None,
    page: int = 1,
    limit: int = 25,
    ctx: Context,
    format_fn: Any,
) -> None:
    """Output a paginated list."""
    if total is None:
        total = len(items)

    if ctx.json_mode:
        output_json({"items": serialize(items), "total": total, "page": page, "limit": limit})
    else:
        md = format_fn(items, total=total, page=page)
        if total > page * limit:
            md += f"\n\n*Showing {len(items)} of {total} results. Use `--page {page + 1}` for next page.*"
        elif total > 0:
            md += f"\n\n*Showing {len(items)} of {total} results.*"
        output_markdown(md)


def error(message: str, *, ctx: Context | None = None, code: str = "error", exit_code: int = 1) -> None:
    """Output an error and exit."""
    if ctx and ctx.json_mode:
        print(json.dumps({"error": message, "code": code}))
    else:
        console.print(f"[red]Error:[/red] {message}")
    sys.exit(exit_code)


# ---------------------------------------------------------------------------
# Generic markdown helpers
# ---------------------------------------------------------------------------


def generic_markdown(data: Any) -> str:
    if isinstance(data, dict):
        return _dict_to_md(data)
    if isinstance(data, list):
        if not data:
            return "_No results._"
        return "\n\n".join(generic_markdown(item) for item in data)
    return str(data)


def _dict_to_md(d: dict) -> str:
    lines = ["| Field | Value |", "|-------|-------|"]
    for key, value in d.items():
        if isinstance(value, (dict, list)):
            continue
        display_key = key.replace("_", " ").title()
        lines.append(f"| {display_key} | {value} |")
    return "\n".join(lines)


def md_table(rows: list[dict[str, str]], headers: list[tuple[str, str]]) -> str:
    """Build a markdown table from rows."""
    if not rows:
        return "_No results._"

    header_line = "| " + " | ".join(h for h, _ in headers) + " |"
    sep_line = "| " + " | ".join("---" for _ in headers) + " |"
    lines = [header_line, sep_line]
    for row in rows:
        cells = [str(row.get(key, "")) for _, key in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)

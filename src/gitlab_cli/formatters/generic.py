"""Generic formatters for dicts and lists."""

from __future__ import annotations

from typing import Any

from gitlab_cli.output import md_table


def detail_table(data: Any, fields: list[tuple[str, str]], *, title: str | None = None) -> str:
    """Render a single record as a Field/Value markdown table.

    Args:
        data: dict
        fields: List of (label, key) — key supports dot notation.
        title: Optional heading.
    """
    d = data

    lines: list[str] = []
    if title:
        lines.append(f"# {title}")
        lines.append("")

    lines.append("| Field | Value |")
    lines.append("|-------|-------|")
    for label, key in fields:
        value = _get(d, key)
        if value is None or value == "" or value == []:
            continue
        lines.append(f"| {label} | {_fmt(value)} |")
    return "\n".join(lines)


def list_table(
    items: list[Any],
    columns: list[tuple[str, str]],
    *,
    title: str = "Results",
    total: int = 0,
    page: int = 1,
) -> str:
    """Render a list of records as a markdown table."""
    if not items:
        return f"# {title}\n\n_No results found._"

    header = f"# {title}"
    if total:
        header += f" (page {page}, {total} total)"

    rows: list[dict[str, str]] = []
    for item in items:
        d = item
        row = {}
        for _, key in columns:
            row[key] = _fmt(_get(d, key))
        rows.append(row)

    return f"{header}\n\n{md_table(rows, columns)}"


def _get(d: dict, key: str) -> Any:
    """Get a value from a dict, supporting dot notation."""
    parts = key.split(".")
    current: Any = d
    for part in parts:
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None
        if current is None:
            return None
    return current


def _fmt(value: Any) -> str:
    """Format a value for display in a markdown table cell."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, list):
        if not value:
            return ""
        # Extract names from list of user dicts (common GitLab pattern)
        if value and isinstance(value[0], dict) and "name" in value[0]:
            return ", ".join(v.get("name", "?") for v in value)
        return ", ".join(str(v) for v in value)
    if isinstance(value, dict):
        # Extract name from user dict
        if "name" in value:
            return str(value["name"])
        return str(value)
    return str(value)

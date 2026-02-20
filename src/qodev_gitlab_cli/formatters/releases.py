"""Release formatters."""

from __future__ import annotations

from typing import Any

from qodev_gitlab_cli.formatters.generic import detail_table, list_table

RELEASE_DETAIL_FIELDS = [
    ("Tag", "tag_name"),
    ("Name", "name"),
    ("Description", "description"),
    ("Author", "author.name"),
    ("Created", "created_at"),
    ("Released", "released_at"),
    ("Commit", "commit.short_id"),
]

RELEASE_LIST_COLUMNS = [
    ("Tag", "tag_name"),
    ("Name", "name"),
    ("Author", "author.name"),
    ("Released", "released_at"),
]


def format_release_detail(data: Any) -> str:
    tag = data.get("tag_name", "?") if isinstance(data, dict) else "?"
    return detail_table(data, RELEASE_DETAIL_FIELDS, title=f"Release: {tag}")


def format_release_list(items: list[Any], *, total: int = 0, page: int = 1) -> str:
    return list_table(items, RELEASE_LIST_COLUMNS, title="Releases", total=total, page=page)

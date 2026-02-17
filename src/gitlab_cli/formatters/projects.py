"""Project formatters."""

from __future__ import annotations

from typing import Any

from gitlab_cli.formatters.generic import detail_table, list_table

PROJECT_DETAIL_FIELDS = [
    ("ID", "id"),
    ("Name", "name"),
    ("Path", "path_with_namespace"),
    ("Description", "description"),
    ("URL", "web_url"),
    ("Default Branch", "default_branch"),
    ("Visibility", "visibility"),
    ("Stars", "star_count"),
    ("Forks", "forks_count"),
    ("Open Issues", "open_issues_count"),
    ("Created", "created_at"),
    ("Updated", "last_activity_at"),
]

PROJECT_LIST_COLUMNS = [
    ("ID", "id"),
    ("Name", "name"),
    ("Path", "path_with_namespace"),
    ("Stars", "star_count"),
    ("Updated", "last_activity_at"),
]


def format_project_detail(data: Any) -> str:
    name = data.get("name", "Unknown") if isinstance(data, dict) else "Unknown"
    return detail_table(data, PROJECT_DETAIL_FIELDS, title=f"Project: {name}")


def format_project_list(items: list[Any], *, total: int = 0, page: int = 1) -> str:
    return list_table(items, PROJECT_LIST_COLUMNS, title="Projects", total=total, page=page)

"""Issue formatters."""

from __future__ import annotations

from typing import Any

from gitlab_cli.formatters.generic import detail_table, list_table

ISSUE_DETAIL_FIELDS = [
    ("IID", "iid"),
    ("Title", "title"),
    ("State", "state"),
    ("Author", "author.name"),
    ("Assignees", "assignees"),
    ("Labels", "labels"),
    ("Milestone", "milestone.title"),
    ("URL", "web_url"),
    ("Created", "created_at"),
    ("Updated", "updated_at"),
    ("Closed", "closed_at"),
    ("Description", "description"),
]

ISSUE_LIST_COLUMNS = [
    ("IID", "iid"),
    ("Title", "title"),
    ("Author", "author.name"),
    ("Labels", "labels"),
    ("State", "state"),
    ("Updated", "updated_at"),
]

NOTE_LIST_COLUMNS = [
    ("ID", "id"),
    ("Author", "author.name"),
    ("Body", "_body"),
    ("Created", "created_at"),
]


def format_issue_detail(data: Any) -> str:
    iid = data.get("iid", "?") if isinstance(data, dict) else "?"
    return detail_table(data, ISSUE_DETAIL_FIELDS, title=f"Issue #{iid}")


def format_issue_list(items: list[Any], *, total: int = 0, page: int = 1) -> str:
    return list_table(items, ISSUE_LIST_COLUMNS, title="Issues", total=total, page=page)


def format_note_list(items: list[Any], *, total: int = 0, page: int = 1) -> str:
    rows = []
    for n in items:
        body = n.get("body", "")
        rows.append(
            {
                **n,
                "_body": (body[:80] + "...") if len(body) > 80 else body,
            }
        )
    return list_table(rows, NOTE_LIST_COLUMNS, title="Notes", total=total, page=page)

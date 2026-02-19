"""Merge request formatters."""

from __future__ import annotations

from typing import Any

from gitlab_cli.formatters.generic import detail_table, list_table

MR_DETAIL_FIELDS = [
    ("IID", "iid"),
    ("Title", "title"),
    ("State", "state"),
    ("Author", "author.name"),
    ("Source", "source_branch"),
    ("Target", "target_branch"),
    ("URL", "web_url"),
    ("Labels", "labels"),
    ("Assignees", "assignees"),
    ("Reviewers", "reviewers"),
    ("Created", "created_at"),
    ("Updated", "updated_at"),
    ("Merged By", "merged_by.name"),
    ("Merge Status", "merge_status"),
]

MR_LIST_COLUMNS = [
    ("IID", "iid"),
    ("Title", "title"),
    ("Author", "author.name"),
    ("Source", "source_branch"),
    ("Target", "target_branch"),
    ("State", "state"),
]

DISCUSSION_LIST_COLUMNS = [
    ("ID", "id"),
    ("Author", "_author"),
    ("Resolved", "_resolved"),
    ("Body", "_body"),
]

COMMIT_LIST_COLUMNS = [
    ("Short ID", "short_id"),
    ("Title", "title"),
    ("Author", "author_name"),
    ("Date", "created_at"),
]


def format_mr_detail(data: Any) -> str:
    iid = data.get("iid", "?") if isinstance(data, dict) else "?"
    return detail_table(data, MR_DETAIL_FIELDS, title=f"Merge Request !{iid}")


def format_mr_list(items: list[Any], *, total: int = 0, page: int = 1) -> str:
    return list_table(items, MR_LIST_COLUMNS, title="Merge Requests", total=total, page=page)


def format_discussion_list(items: list[Any], *, total: int = 0, page: int = 1) -> str:
    """Format discussions with first note content."""
    rows = []
    for d in items:
        notes = d.get("notes", [])
        first_note = notes[0] if notes else {}
        rows.append(
            {
                "id": d.get("id", ""),
                "_author": first_note.get("author", {}).get("name", ""),
                "_resolved": "Yes"
                if d.get("individual_note") is False
                and all(n.get("resolved", False) for n in notes if n.get("resolvable"))
                else "No"
                if any(n.get("resolvable") for n in notes)
                else "-",
                "_body": (first_note.get("body", "")[:80] + "...")
                if len(first_note.get("body", "")) > 80
                else first_note.get("body", ""),
            }
        )
    return list_table(rows, DISCUSSION_LIST_COLUMNS, title="Discussions", total=total, page=page)


def format_commit_list(items: list[Any], *, total: int = 0, page: int = 1) -> str:
    return list_table(items, COMMIT_LIST_COLUMNS, title="Commits", total=total, page=page)


def format_approval_detail(data: Any) -> str:
    lines = ["# Approval Status"]
    approved_by = data.get("approved_by", [])
    if approved_by:
        lines.append(f"\nApproved by: {', '.join(a.get('user', {}).get('name', '?') for a in approved_by)}")
    else:
        lines.append("\n_Not yet approved._")

    rules = data.get("approval_rules_left", [])
    if rules:
        lines.append("\n## Remaining Rules")
        for rule in rules:
            lines.append(f"- {rule.get('name', '?')} (needs {rule.get('approvals_required', '?')} approvals)")

    return "\n".join(lines)

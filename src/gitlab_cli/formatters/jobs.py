"""Job formatters."""

from __future__ import annotations

from typing import Any

from gitlab_cli.formatters.generic import detail_table, list_table

JOB_DETAIL_FIELDS = [
    ("ID", "id"),
    ("Name", "name"),
    ("Status", "status"),
    ("Stage", "stage"),
    ("Ref", "ref"),
    ("Pipeline", "pipeline.id"),
    ("URL", "web_url"),
    ("Duration", "duration"),
    ("Created", "created_at"),
    ("Started", "started_at"),
    ("Finished", "finished_at"),
    ("Runner", "runner.description"),
]

JOB_LIST_COLUMNS = [
    ("ID", "id"),
    ("Name", "name"),
    ("Stage", "stage"),
    ("Status", "status"),
    ("Duration", "duration"),
]


def format_job_detail(data: Any) -> str:
    name = data.get("name", "?") if isinstance(data, dict) else "?"
    return detail_table(data, JOB_DETAIL_FIELDS, title=f"Job: {name}")


def format_job_list(items: list[Any], *, total: int = 0, page: int = 1) -> str:
    return list_table(items, JOB_LIST_COLUMNS, title="Jobs", total=total, page=page)

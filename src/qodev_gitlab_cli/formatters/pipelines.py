"""Pipeline formatters."""

from __future__ import annotations

from typing import Any

from qodev_gitlab_cli.formatters.generic import detail_table, list_table

PIPELINE_DETAIL_FIELDS = [
    ("ID", "id"),
    ("Status", "status"),
    ("Ref", "ref"),
    ("SHA", "sha"),
    ("Source", "source"),
    ("URL", "web_url"),
    ("Created", "created_at"),
    ("Updated", "updated_at"),
    ("Duration", "duration"),
]

PIPELINE_LIST_COLUMNS = [
    ("ID", "id"),
    ("Status", "status"),
    ("Ref", "ref"),
    ("Source", "source"),
    ("Created", "created_at"),
]


def format_pipeline_detail(data: Any) -> str:
    pid = data.get("id", "?") if isinstance(data, dict) else "?"
    return detail_table(data, PIPELINE_DETAIL_FIELDS, title=f"Pipeline #{pid}")


def format_pipeline_list(items: list[Any], *, total: int = 0, page: int = 1) -> str:
    return list_table(items, PIPELINE_LIST_COLUMNS, title="Pipelines", total=total, page=page)


def format_wait_result(data: Any) -> str:
    lines = [f"# Pipeline #{data.get('pipeline_id', '?')}"]
    lines.append("")
    lines.append(f"**Status:** {data.get('final_status', '?')}")
    lines.append(f"**Duration:** {data.get('total_duration', '?')}s")
    lines.append(f"**Checks:** {data.get('checks_performed', '?')}")

    if data.get("pipeline_url"):
        lines.append(f"**URL:** {data['pipeline_url']}")

    summary = data.get("job_summary")
    if summary:
        lines.append("")
        lines.append(
            f"**Jobs:** {summary.get('total', 0)} total, {summary.get('success', 0)} success, {summary.get('failed', 0)} failed"
        )

    failed_jobs = data.get("failed_jobs", [])
    if failed_jobs:
        lines.append("")
        lines.append("## Failed Jobs")
        for job in failed_jobs:
            lines.append(f"\n### {job.get('name', '?')} (#{job.get('id', '?')})")
            if job.get("web_url"):
                lines.append(f"URL: {job['web_url']}")
            if job.get("last_log_lines"):
                lines.append(f"\n```\n{job['last_log_lines']}\n```")

    return "\n".join(lines)

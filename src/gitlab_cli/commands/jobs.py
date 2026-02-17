"""Job commands."""

from __future__ import annotations

from typing import Annotated

from cyclopts import App, Parameter

from gitlab_cli.context import ctx
from gitlab_cli.formatters.jobs import format_job_detail
from gitlab_cli.output import output, output_markdown

jobs_app = App(name="jobs", help="Manage jobs.")


@jobs_app.command
def get(
    id: Annotated[int, Parameter(help="Job ID")],
) -> None:
    """Get job details."""
    client = ctx.client()
    project = ctx.resolve_project()
    result = client.get_job(project, id)
    output(result, ctx=ctx, format_fn=format_job_detail)


@jobs_app.command
def log(
    id: Annotated[int, Parameter(help="Job ID")],
) -> None:
    """Get job log output."""
    client = ctx.client()
    project = ctx.resolve_project()
    log_text = client.get_job_log(project, id)

    if ctx.json_mode:
        from gitlab_cli.output import output_json

        output_json({"job_id": id, "log": log_text})
    else:
        output_markdown(f"# Job #{id} Log\n\n```\n{log_text}\n```")


@jobs_app.command
def retry(
    id: Annotated[int, Parameter(help="Job ID")],
) -> None:
    """Retry a failed job."""
    client = ctx.client()
    project = ctx.resolve_project()
    result = client.retry_job(project, id)
    output(result, ctx=ctx, format_fn=format_job_detail)

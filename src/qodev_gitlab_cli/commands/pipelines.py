"""Pipeline commands."""

from __future__ import annotations

from typing import Annotated

from cyclopts import App, Parameter

from qodev_gitlab_cli.context import ctx
from qodev_gitlab_cli.formatters.jobs import format_job_list
from qodev_gitlab_cli.formatters.pipelines import format_pipeline_detail, format_pipeline_list, format_wait_result
from qodev_gitlab_cli.output import output, output_list

pipelines_app = App(name="pipelines", help="Manage pipelines.")


@pipelines_app.command
def list(
    *,
    ref: Annotated[str | None, Parameter(name="--ref", help="Filter by branch/tag")] = None,
    limit: Annotated[int, Parameter(name="--limit", help="Max pipelines to return")] = 20,
) -> None:
    """List pipelines."""
    client = ctx.client()
    project = ctx.resolve_project()
    items = client.get_pipelines(project, ref=ref, per_page=limit, max_pages=1)
    output_list(items=items, ctx=ctx, format_fn=format_pipeline_list)


@pipelines_app.command
def get(
    id: Annotated[int, Parameter(help="Pipeline ID")],
) -> None:
    """Get pipeline details."""
    client = ctx.client()
    project = ctx.resolve_project()
    result = client.get_pipeline(project, id)
    output(result, ctx=ctx, format_fn=format_pipeline_detail)


@pipelines_app.command
def jobs(
    id: Annotated[int, Parameter(help="Pipeline ID")],
) -> None:
    """List jobs for a pipeline."""
    client = ctx.client()
    project = ctx.resolve_project()
    items = client.get_pipeline_jobs(project, id)
    output_list(items=items, ctx=ctx, format_fn=format_job_list)


@pipelines_app.command
def wait(
    id: Annotated[int, Parameter(help="Pipeline ID")],
    *,
    timeout: Annotated[int, Parameter(name="--timeout", help="Timeout in seconds")] = 3600,
    interval: Annotated[int, Parameter(name="--interval", help="Check interval in seconds")] = 10,
) -> None:
    """Wait for a pipeline to complete."""
    client = ctx.client()
    project = ctx.resolve_project()
    result = client.wait_for_pipeline(project, id, timeout_seconds=timeout, check_interval=interval)
    output(result, ctx=ctx, format_fn=format_wait_result)

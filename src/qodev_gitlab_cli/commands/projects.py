"""Project commands."""

from __future__ import annotations

from typing import Annotated

from cyclopts import App, Parameter

from qodev_gitlab_cli.context import ctx
from qodev_gitlab_cli.formatters.projects import format_project_detail, format_project_list
from qodev_gitlab_cli.output import output, output_list

projects_app = App(name="projects", help="Manage projects.")


@projects_app.command
def list(
    *,
    owned: Annotated[bool, Parameter(name="--owned", help="Only owned projects", negative="")] = False,
) -> None:
    """List projects."""
    client = ctx.client()
    items = client.get_projects(owned=owned)
    output_list(items=items, ctx=ctx, format_fn=format_project_list)


@projects_app.command
def get(
    id: Annotated[str | None, Parameter(help="Project ID or path (defaults to auto-detected)")] = None,
) -> None:
    """Get project details."""
    client = ctx.client()
    project_id = id or ctx.resolve_project()
    result = client.get_project(project_id)
    output(result, ctx=ctx, format_fn=format_project_detail)

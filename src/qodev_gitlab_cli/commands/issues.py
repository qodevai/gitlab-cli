"""Issue commands."""

from __future__ import annotations

from typing import Annotated

from cyclopts import App, Parameter

from qodev_gitlab_cli.context import ctx
from qodev_gitlab_cli.formatters.issues import format_issue_detail, format_issue_list, format_note_list
from qodev_gitlab_cli.output import output, output_list

issues_app = App(name="issues", help="Manage issues.")


@issues_app.command
def list(
    *,
    state: Annotated[str, Parameter(name="--state", help="Filter: opened, closed, all")] = "opened",
    labels: Annotated[str | None, Parameter(name="--labels", help="Filter by labels")] = None,
    milestone: Annotated[str | None, Parameter(name="--milestone", help="Filter by milestone")] = None,
) -> None:
    """List issues."""
    client = ctx.client()
    project = ctx.resolve_project()
    items = client.get_issues(project, state=state, labels=labels, milestone=milestone)
    output_list(items=items, ctx=ctx, format_fn=format_issue_list)


@issues_app.command
def get(
    iid: Annotated[int, Parameter(help="Issue IID")],
) -> None:
    """Get issue details."""
    client = ctx.client()
    project = ctx.resolve_project()
    result = client.get_issue(project, iid)
    output(result, ctx=ctx, format_fn=format_issue_detail)


@issues_app.command
def create(
    *,
    title: Annotated[str, Parameter(name="--title", help="Issue title")],
    description: Annotated[str | None, Parameter(name="--description", help="Issue description")] = None,
    labels: Annotated[str | None, Parameter(name="--labels", help="Comma-separated labels")] = None,
) -> None:
    """Create a new issue."""
    client = ctx.client()
    project = ctx.resolve_project()
    result = client.create_issue(project, title=title, description=description, labels=labels)
    output(result, ctx=ctx, format_fn=format_issue_detail)


@issues_app.command
def update(
    iid: Annotated[int, Parameter(help="Issue IID")],
    *,
    title: Annotated[str | None, Parameter(name="--title", help="New title")] = None,
    description: Annotated[str | None, Parameter(name="--description", help="New description")] = None,
    labels: Annotated[str | None, Parameter(name="--labels", help="New labels")] = None,
) -> None:
    """Update an issue."""
    client = ctx.client()
    project = ctx.resolve_project()
    result = client.update_issue(project, iid, title=title, description=description, labels=labels)
    output(result, ctx=ctx, format_fn=format_issue_detail)


@issues_app.command
def close(
    iid: Annotated[int, Parameter(help="Issue IID")],
) -> None:
    """Close an issue."""
    client = ctx.client()
    project = ctx.resolve_project()
    result = client.close_issue(project, iid)
    output(result, ctx=ctx, format_fn=format_issue_detail)


@issues_app.command
def comment(
    iid: Annotated[int, Parameter(help="Issue IID")],
    *,
    body: Annotated[str, Parameter(name="--body", help="Comment text")],
) -> None:
    """Comment on an issue."""
    client = ctx.client()
    project = ctx.resolve_project()
    result = client.create_issue_note(project, iid, body)
    output(result, ctx=ctx)


@issues_app.command
def notes(
    iid: Annotated[int, Parameter(help="Issue IID")],
) -> None:
    """List comments/notes on an issue."""
    client = ctx.client()
    project = ctx.resolve_project()
    items = client.get_issue_notes(project, iid)
    output_list(items=items, ctx=ctx, format_fn=format_note_list)

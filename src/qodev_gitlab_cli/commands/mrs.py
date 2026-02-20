"""Merge request commands."""

from __future__ import annotations

from typing import Annotated

from cyclopts import App, Parameter

from qodev_gitlab_cli.context import ctx
from qodev_gitlab_cli.formatters.mrs import (
    format_approval_detail,
    format_commit_list,
    format_discussion_list,
    format_mr_detail,
    format_mr_list,
)
from qodev_gitlab_cli.output import output, output_list, output_markdown

mrs_app = App(name="mrs", help="Manage merge requests.")


@mrs_app.command
def list(
    *,
    state: Annotated[str, Parameter(name="--state", help="Filter by state: opened, closed, merged, all")] = "opened",
) -> None:
    """List merge requests."""
    client = ctx.client()
    project = ctx.resolve_project()
    items = client.get_merge_requests(project, state=state)
    output_list(items=items, ctx=ctx, format_fn=format_mr_list)


@mrs_app.command
def get(
    iid: Annotated[int, Parameter(help="Merge request IID")],
) -> None:
    """Get merge request details."""
    client = ctx.client()
    project = ctx.resolve_project()
    result = client.get_merge_request(project, iid)
    output(result, ctx=ctx, format_fn=format_mr_detail)


@mrs_app.command
def create(
    *,
    title: Annotated[str, Parameter(name="--title", help="MR title")],
    source: Annotated[str | None, Parameter(name="--source", help="Source branch (default: current)")] = None,
    target: Annotated[str, Parameter(name="--target", help="Target branch")] = "main",
    description: Annotated[str | None, Parameter(name="--description", help="MR description")] = None,
    labels: Annotated[str | None, Parameter(name="--labels", help="Comma-separated labels")] = None,
    squash: Annotated[bool | None, Parameter(name="--squash", help="Squash commits on merge")] = None,
) -> None:
    """Create a new merge request."""
    client = ctx.client()
    project = ctx.resolve_project()

    if source is None:
        from qodev_gitlab_cli.project import get_current_branch

        source = get_current_branch()
        if not source:
            from qodev_gitlab_cli.output import error

            error("Could not detect current branch. Use --source.", ctx=ctx)

    result = client.create_merge_request(
        project,
        source_branch=source,
        target_branch=target,
        title=title,
        description=description,
        labels=labels,
        squash=squash,
    )
    output(result, ctx=ctx, format_fn=format_mr_detail)


@mrs_app.command
def update(
    iid: Annotated[int, Parameter(help="Merge request IID")],
    *,
    title: Annotated[str | None, Parameter(name="--title", help="New title")] = None,
    description: Annotated[str | None, Parameter(name="--description", help="New description")] = None,
    labels: Annotated[str | None, Parameter(name="--labels", help="New labels")] = None,
    target: Annotated[str | None, Parameter(name="--target", help="New target branch")] = None,
) -> None:
    """Update a merge request."""
    client = ctx.client()
    project = ctx.resolve_project()
    result = client.update_mr(project, iid, title=title, description=description, labels=labels, target_branch=target)
    output(result, ctx=ctx, format_fn=format_mr_detail)


@mrs_app.command
def merge(
    iid: Annotated[int, Parameter(help="Merge request IID")],
    *,
    squash: Annotated[bool | None, Parameter(name="--squash", help="Squash commits")] = None,
    when_pipeline_succeeds: Annotated[
        bool, Parameter(name="--when-pipeline-succeeds", help="Merge when pipeline succeeds", negative="")
    ] = False,
) -> None:
    """Merge a merge request."""
    client = ctx.client()
    project = ctx.resolve_project()
    result = client.merge_mr(project, iid, squash=squash, merge_when_pipeline_succeeds=when_pipeline_succeeds)
    output(result, ctx=ctx, format_fn=format_mr_detail)


@mrs_app.command
def close(
    iid: Annotated[int, Parameter(help="Merge request IID")],
) -> None:
    """Close a merge request."""
    client = ctx.client()
    project = ctx.resolve_project()
    result = client.close_mr(project, iid)
    output(result, ctx=ctx, format_fn=format_mr_detail)


@mrs_app.command
def discussions(
    iid: Annotated[int, Parameter(help="Merge request IID")],
) -> None:
    """List discussions on a merge request."""
    client = ctx.client()
    project = ctx.resolve_project()
    items = client.get_mr_discussions(project, iid)
    output_list(items=items, ctx=ctx, format_fn=format_discussion_list)


@mrs_app.command
def changes(
    iid: Annotated[int, Parameter(help="Merge request IID")],
) -> None:
    """Show changes/diff for a merge request."""
    client = ctx.client()
    project = ctx.resolve_project()
    result = client.get_mr_changes(project, iid)

    if ctx.json_mode:
        from qodev_gitlab_cli.output import output_json

        output_json(result)
    else:
        diffs = result.get("changes", [])
        lines = [f"# Changes for !{iid}", ""]
        for diff in diffs:
            lines.append(f"## {diff.get('new_path', '?')}")
            lines.append(f"```diff\n{diff.get('diff', '')}\n```")
            lines.append("")
        output_markdown("\n".join(lines))


@mrs_app.command
def commits(
    iid: Annotated[int, Parameter(help="Merge request IID")],
) -> None:
    """List commits in a merge request."""
    client = ctx.client()
    project = ctx.resolve_project()
    items = client.get_mr_commits(project, iid)
    output_list(items=items, ctx=ctx, format_fn=format_commit_list)


@mrs_app.command
def approvals(
    iid: Annotated[int, Parameter(help="Merge request IID")],
) -> None:
    """Show approval status for a merge request."""
    client = ctx.client()
    project = ctx.resolve_project()
    result = client.get_mr_approvals(project, iid)
    output(result, ctx=ctx, format_fn=format_approval_detail)


@mrs_app.command
def comment(
    iid: Annotated[int, Parameter(help="Merge request IID")],
    *,
    body: Annotated[str, Parameter(name="--body", help="Comment text")],
) -> None:
    """Comment on a merge request."""
    client = ctx.client()
    project = ctx.resolve_project()
    result = client.create_mr_note(project, iid, body)
    output(result, ctx=ctx)


@mrs_app.command
def pipelines(
    iid: Annotated[int, Parameter(help="Merge request IID")],
) -> None:
    """List pipelines for a merge request."""
    client = ctx.client()
    project = ctx.resolve_project()
    items = client.get_mr_pipelines(project, iid)
    from qodev_gitlab_cli.formatters.pipelines import format_pipeline_list

    output_list(items=items, ctx=ctx, format_fn=format_pipeline_list)

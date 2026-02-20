"""Release commands."""

from __future__ import annotations

from typing import Annotated

from cyclopts import App, Parameter

from qodev_gitlab_cli.context import ctx
from qodev_gitlab_cli.formatters.releases import format_release_detail, format_release_list
from qodev_gitlab_cli.output import output, output_list

releases_app = App(name="releases", help="Manage releases.")


@releases_app.command
def list() -> None:
    """List releases."""
    client = ctx.client()
    project = ctx.resolve_project()
    items = client.get_releases(project)
    output_list(items=items, ctx=ctx, format_fn=format_release_list)


@releases_app.command
def get(
    tag: Annotated[str, Parameter(help="Tag name")],
) -> None:
    """Get release details."""
    client = ctx.client()
    project = ctx.resolve_project()
    result = client.get_release(project, tag)
    output(result, ctx=ctx, format_fn=format_release_detail)


@releases_app.command
def create(
    *,
    tag: Annotated[str, Parameter(name="--tag", help="Tag name for the release")],
    name: Annotated[str | None, Parameter(name="--name", help="Release title")] = None,
    description: Annotated[str | None, Parameter(name="--description", help="Release notes")] = None,
    ref: Annotated[str | None, Parameter(name="--ref", help="Commit SHA, branch, or tag")] = None,
) -> None:
    """Create a new release."""
    client = ctx.client()
    project = ctx.resolve_project()
    result = client.create_release(project, tag_name=tag, name=name, description=description, ref=ref)
    output(result, ctx=ctx, format_fn=format_release_detail)

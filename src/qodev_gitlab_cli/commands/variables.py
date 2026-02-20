"""CI/CD variable commands."""

from __future__ import annotations

from typing import Annotated

from cyclopts import App, Parameter

from qodev_gitlab_cli.context import ctx
from qodev_gitlab_cli.formatters.variables import format_variable_detail, format_variable_list
from qodev_gitlab_cli.output import output, output_list

variables_app = App(name="variables", help="Manage CI/CD variables.")


@variables_app.command
def list() -> None:
    """List CI/CD variables (values hidden)."""
    client = ctx.client()
    project = ctx.resolve_project()
    items = client.list_project_variables(project)
    output_list(items=items, ctx=ctx, format_fn=format_variable_list)


@variables_app.command
def get(
    key: Annotated[str, Parameter(help="Variable key")],
) -> None:
    """Get a CI/CD variable."""
    client = ctx.client()
    project = ctx.resolve_project()
    result = client.get_project_variable(project, key)
    if result is None:
        from qodev_gitlab_cli.output import error

        error(f"Variable '{key}' not found.", ctx=ctx, code="not_found", exit_code=81)
    else:
        output(result, ctx=ctx, format_fn=format_variable_detail)


@variables_app.command
def set(
    key: Annotated[str, Parameter(help="Variable key")],
    value: Annotated[str, Parameter(help="Variable value")],
    *,
    protected: Annotated[bool, Parameter(name="--protected", help="Only in protected branches", negative="")] = False,
    masked: Annotated[bool, Parameter(name="--masked", help="Hidden in job logs", negative="")] = False,
) -> None:
    """Set a CI/CD variable (create or update)."""
    client = ctx.client()
    project = ctx.resolve_project()
    var, action = client.set_project_variable(project, key, value, protected=protected, masked=masked)

    if ctx.json_mode:
        from qodev_gitlab_cli.output import output_json

        output_json({"variable": var, "action": action})
    else:
        from qodev_gitlab_cli.output import output_markdown

        output_markdown(f"Variable `{key}` **{action}** successfully.")

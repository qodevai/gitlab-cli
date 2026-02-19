"""Root App definition, global options, and error handling."""

from __future__ import annotations

import sys
from typing import Annotated

from cyclopts import App, Group, Parameter
from gitlab_client import APIError, AuthenticationError, ConfigurationError, NotFoundError

import gitlab_cli.context as _ctx

app = App(
    name="gitlab",
    help="Agent-friendly CLI for the GitLab API.",
    version_flags=[],
)

app.meta.group_parameters = Group("Global Options", sort_key=0)

# ---------------------------------------------------------------------------
# Import and register command groups
# ---------------------------------------------------------------------------
from gitlab_cli.commands.issues import issues_app  # noqa: E402
from gitlab_cli.commands.jobs import jobs_app  # noqa: E402
from gitlab_cli.commands.mrs import mrs_app  # noqa: E402
from gitlab_cli.commands.pipelines import pipelines_app  # noqa: E402
from gitlab_cli.commands.projects import projects_app  # noqa: E402
from gitlab_cli.commands.releases import releases_app  # noqa: E402
from gitlab_cli.commands.variables import variables_app  # noqa: E402

app.command(projects_app)
app.command(mrs_app)
app.command(pipelines_app)
app.command(jobs_app)
app.command(issues_app)
app.command(releases_app)
app.command(variables_app)

# ---------------------------------------------------------------------------
# Exit codes
# ---------------------------------------------------------------------------
EXIT_AUTH = 80
EXIT_NOT_FOUND = 81
EXIT_API = 82
EXIT_VALIDATION = 83
EXIT_CONFIG = 84


# ---------------------------------------------------------------------------
# Meta launcher — global options & error handling
# ---------------------------------------------------------------------------
@app.meta.default
def launcher(
    *tokens: Annotated[str, Parameter(show=False, allow_leading_hyphen=True)],
    json: Annotated[bool, Parameter(name="--json", help="Output as JSON", negative="")] = False,
    token: Annotated[
        str | None, Parameter(name="--token", help="GitLab token (overrides GITLAB_TOKEN)", show=False)
    ] = None,
    url: Annotated[str | None, Parameter(name="--url", help="GitLab URL (overrides GITLAB_URL)", show=False)] = None,
    project: Annotated[str | None, Parameter(name=["--project", "-p"], help="Project ID or path")] = None,
    limit: Annotated[int, Parameter(name="--limit", help="Results per page")] = 25,
    page: Annotated[int, Parameter(name="--page", help="Page number")] = 1,
) -> None:
    """GitLab CLI — manage projects, merge requests, pipelines, and more."""
    _ctx.ctx.configure(json_mode=json, token=token, base_url=url, project=project, limit=limit, page=page)

    try:
        app(tokens)
    except AuthenticationError as exc:
        _handle_error(str(exc), code="authentication", exit_code=EXIT_AUTH)
    except NotFoundError as exc:
        _handle_error(str(exc), code="not_found", exit_code=EXIT_NOT_FOUND)
    except APIError as exc:
        _handle_error(str(exc), code="api_error", exit_code=EXIT_API)
    except ConfigurationError as exc:
        _handle_error(str(exc), code="configuration", exit_code=EXIT_CONFIG)
    except SystemExit:
        raise
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as exc:
        _handle_error(f"Unexpected error: {exc}", code="unknown", exit_code=1)


def _handle_error(message: str, *, code: str, exit_code: int) -> None:
    from gitlab_cli.output import error

    error(message, ctx=_ctx.ctx, code=code, exit_code=exit_code)


def main() -> None:
    app.meta()

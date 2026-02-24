"""Root App definition, global options, and error handling."""

from __future__ import annotations

import inspect
import sys
import types
from typing import Annotated, Union, get_args, get_origin, get_type_hints

from cyclopts import App, Group, Parameter
from qodev_gitlab_api import APIError, AuthenticationError, ConfigurationError, NotFoundError

import qodev_gitlab_cli.context as _ctx

app = App(
    name="qodev-gitlab",
    help="Agent-friendly CLI for the GitLab API.",
    help_format="rich",
    version_flags=[],
)

app.meta.group_parameters = Group("Global Options", sort_key=0)

# ---------------------------------------------------------------------------
# Import and register command groups
# ---------------------------------------------------------------------------
from qodev_gitlab_cli.commands.issues import issues_app  # noqa: E402
from qodev_gitlab_cli.commands.jobs import jobs_app  # noqa: E402
from qodev_gitlab_cli.commands.mrs import mrs_app  # noqa: E402
from qodev_gitlab_cli.commands.pipelines import pipelines_app  # noqa: E402
from qodev_gitlab_cli.commands.projects import projects_app  # noqa: E402
from qodev_gitlab_cli.commands.releases import releases_app  # noqa: E402
from qodev_gitlab_cli.commands.variables import variables_app  # noqa: E402

app.command(projects_app)
app.command(mrs_app)
app.command(pipelines_app)
app.command(jobs_app)
app.command(issues_app)
app.command(releases_app)
app.command(variables_app)

# Prevent the command reference epilogue from showing on sub-command help pages.
for _sub in (projects_app, mrs_app, pipelines_app, jobs_app, issues_app, releases_app, variables_app):
    _sub.help_epilogue = ""


# ---------------------------------------------------------------------------
# Dynamic command reference for root --help
# ---------------------------------------------------------------------------
def _is_bool_type(tp: type | None) -> bool:
    if tp is bool:
        return True
    if tp is None:
        return False
    origin = get_origin(tp)
    if origin is Union or isinstance(tp, types.UnionType):
        return bool in get_args(tp)
    return False


def _format_signature(func: object, prefix_len: int = 0, col_width: int = 50) -> str:
    sig = inspect.signature(func)  # type: ignore[arg-type]
    try:
        hints = get_type_hints(func, include_extras=True)
    except Exception:
        hints = {}

    required: list[str] = []
    optional: list[str] = []
    for pname, param in sig.parameters.items():
        hint = hints.get(pname)

        cli_param = None
        base_type = hint
        if hint is not None and get_origin(hint) is Annotated:
            args = get_args(hint)
            base_type = args[0]
            for arg in args[1:]:
                if isinstance(arg, Parameter):
                    cli_param = arg
                    break

        is_bool = _is_bool_type(base_type)
        has_default = param.default is not inspect.Parameter.empty

        if param.kind == param.KEYWORD_ONLY:
            if cli_param and cli_param.name:
                names = cli_param.name if isinstance(cli_param.name, (list, tuple)) else [cli_param.name]
                cli_name = names[0]
            else:
                cli_name = f"--{pname.replace('_', '-')}"

            if has_default:
                optional.append(f"\\[{cli_name}]")
            elif is_bool:
                required.append(cli_name)
            else:
                required.append(f"{cli_name} {pname.upper()}")
        elif param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD):
            label = pname.upper()
            if has_default:
                optional.append(f"\\[{label}]")
            else:
                required.append(label)

    # Progressively drop optional args from the end to fit column width
    max_sig = col_width - prefix_len - 2  # 2 spaces gap before description
    parts = required + optional
    result = " ".join(parts)
    dropped = 0
    while len(result) > max_sig and optional:
        optional.pop()
        dropped += 1
        parts = required + optional + (["..."] if dropped else [])
        result = " ".join(parts)

    return result


def _display_len(s: str) -> int:
    """Return the rendered width (Rich \\[ escapes become [)."""
    return len(s.replace("\\[", "["))


def _build_command_reference() -> str:
    sub_apps = [
        projects_app, mrs_app, pipelines_app, jobs_app,
        issues_app, releases_app, variables_app,
    ]

    col_width = 46
    entries: list[tuple[str, str]] = []
    for sub in sub_apps:
        sub_name = sub.name[0]
        for cmd_name, cmd_app in sub._commands.items():
            if cmd_name.startswith("-"):
                continue
            func = cmd_app.default_command
            if func is None:
                continue
            prefix = f"  {sub_name} {cmd_name} "
            sig_str = _format_signature(func, prefix_len=len(prefix), col_width=col_width)
            doc = (func.__doc__ or "").strip().split("\n")[0]
            left = f"  {sub_name} {cmd_name}"
            if sig_str:
                left += f" {sig_str}"
            entries.append((left, doc))
        entries.append(("", ""))

    if entries and entries[-1] == ("", ""):
        entries.pop()

    max_line = 78
    lines = ["All Commands:\n"]
    for left, doc in entries:
        if not left:
            lines.append("")
        else:
            display_w = _display_len(left)
            pad = max(2, col_width - display_w)
            avail = max_line - display_w - pad
            if len(doc) > avail > 10:
                doc = doc[: avail - 1] + "\u2026"
            lines.append(f"{left}{' ' * pad}{doc}")
    return "\n".join(lines)


app.help_epilogue = _build_command_reference()

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
    from qodev_gitlab_cli.output import error

    error(message, ctx=_ctx.ctx, code=code, exit_code=exit_code)


def main() -> None:
    app.meta()

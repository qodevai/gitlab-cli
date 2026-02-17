"""Global context shared across all commands."""

from __future__ import annotations

from dataclasses import dataclass

from gitlab_client import GitLabClient


@dataclass
class Context:
    """Shared state passed from the meta launcher to every command."""

    json_mode: bool = False
    token: str | None = None
    base_url: str | None = None
    project: str | None = None
    limit: int = 25
    page: int = 1

    def client(self) -> GitLabClient:
        kwargs: dict = {}
        if self.token:
            kwargs["token"] = self.token
        if self.base_url:
            kwargs["base_url"] = self.base_url
        return GitLabClient(**kwargs)

    def resolve_project(self) -> str:
        if self.project:
            return self.project
        from gitlab_cli.project import detect_project_from_git

        path = detect_project_from_git(self.base_url)
        if not path:
            from gitlab_client.exceptions import ConfigurationError

            raise ConfigurationError(
                "Could not detect project. Use --project/-p or run from a git repo with a GitLab remote."
            )
        return path

    def configure(
        self,
        *,
        json_mode: bool,
        token: str | None,
        base_url: str | None,
        project: str | None,
        limit: int,
        page: int,
    ) -> None:
        self.json_mode = json_mode
        self.token = token
        self.base_url = base_url
        self.project = project
        self.limit = limit
        self.page = page


# Module-level singleton
ctx = Context()

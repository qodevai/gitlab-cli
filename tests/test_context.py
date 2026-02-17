"""Tests for the context module."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from gitlab_cli.context import Context


class TestContext:
    def test_defaults(self) -> None:
        ctx = Context()
        assert ctx.json_mode is False
        assert ctx.token is None
        assert ctx.base_url is None
        assert ctx.project is None
        assert ctx.limit == 25
        assert ctx.page == 1

    def test_configure(self) -> None:
        ctx = Context()
        ctx.configure(json_mode=True, token="tok", base_url="https://gl.com", project="g/p", limit=50, page=2)
        assert ctx.json_mode is True
        assert ctx.token == "tok"
        assert ctx.base_url == "https://gl.com"
        assert ctx.project == "g/p"
        assert ctx.limit == 50
        assert ctx.page == 2

    def test_resolve_project_explicit(self) -> None:
        ctx = Context()
        ctx.project = "my/project"
        assert ctx.resolve_project() == "my/project"

    def test_resolve_project_auto_detect(self) -> None:
        ctx = Context()
        with patch("gitlab_cli.project.detect_project_from_git", return_value="detected/project"):
            assert ctx.resolve_project() == "detected/project"

    def test_resolve_project_no_git_raises(self) -> None:
        ctx = Context()
        with patch("gitlab_cli.project.detect_project_from_git", return_value=None):
            from gitlab_client.exceptions import ConfigurationError

            with pytest.raises(ConfigurationError, match="Could not detect project"):
                ctx.resolve_project()

    def test_client_passes_token(self) -> None:
        ctx = Context()
        ctx.token = "my-token"
        with patch("gitlab_cli.context.GitLabClient") as mock_cls:
            ctx.client()
            mock_cls.assert_called_once_with(token="my-token")

    def test_client_passes_base_url(self) -> None:
        ctx = Context()
        ctx.base_url = "https://gl.com"
        with patch("gitlab_cli.context.GitLabClient") as mock_cls:
            ctx.client()
            mock_cls.assert_called_once_with(base_url="https://gl.com")

    def test_client_no_args(self) -> None:
        ctx = Context()
        with patch("gitlab_cli.context.GitLabClient") as mock_cls:
            ctx.client()
            mock_cls.assert_called_once_with()

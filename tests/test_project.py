"""Tests for git remote project detection."""

from __future__ import annotations

from unittest.mock import patch

from gitlab_cli.project import _parse_project_path, detect_project_from_git


class TestParseProjectPath:
    def test_ssh_url(self) -> None:
        assert _parse_project_path("git@gitlab.com:group/project.git") == "group/project"

    def test_ssh_url_no_git_suffix(self) -> None:
        assert _parse_project_path("git@gitlab.com:group/project") == "group/project"

    def test_ssh_nested(self) -> None:
        assert _parse_project_path("git@gitlab.com:org/group/project.git") == "org/group/project"

    def test_https_url(self) -> None:
        assert _parse_project_path("https://gitlab.com/group/project.git") == "group/project"

    def test_https_no_git_suffix(self) -> None:
        assert _parse_project_path("https://gitlab.com/group/project") == "group/project"

    def test_https_nested(self) -> None:
        assert _parse_project_path("https://gitlab.com/org/group/project.git") == "org/group/project"

    def test_domain_filter_match(self) -> None:
        assert (
            _parse_project_path("git@gitlab.example.com:g/p.git", "https://gitlab.example.com") == "g/p"
        )

    def test_domain_filter_no_match(self) -> None:
        assert _parse_project_path("git@github.com:g/p.git", "https://gitlab.example.com") is None

    def test_invalid_url(self) -> None:
        assert _parse_project_path("not-a-url") is None


class TestDetectProjectFromGit:
    def test_no_git_root(self) -> None:
        with patch("gitlab_cli.project._find_git_root", return_value=None):
            assert detect_project_from_git() is None

    def test_no_remote(self) -> None:
        with (
            patch("gitlab_cli.project._find_git_root", return_value="/tmp/repo"),
            patch("gitlab_cli.project._get_remote_url", return_value=None),
        ):
            assert detect_project_from_git() is None

    def test_full_detection(self) -> None:
        with (
            patch("gitlab_cli.project._find_git_root", return_value="/tmp/repo"),
            patch("gitlab_cli.project._get_remote_url", return_value="git@gitlab.com:ns/proj.git"),
        ):
            assert detect_project_from_git() == "ns/proj"

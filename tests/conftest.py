"""Shared fixtures for gitlab-cli tests."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from gitlab_cli.context import Context


@pytest.fixture
def ctx() -> Context:
    """Fresh context for each test."""
    return Context()


@pytest.fixture
def json_ctx() -> Context:
    """Context with JSON mode enabled."""
    c = Context()
    c.json_mode = True
    return c


@pytest.fixture
def mock_client() -> MagicMock:
    """Mock GitLabClient."""
    return MagicMock()


@pytest.fixture
def mock_env() -> dict[str, str]:
    """Standard env vars."""
    return {
        "GITLAB_TOKEN": "test-token",
        "GITLAB_URL": "https://gitlab.example.com",
    }


@pytest.fixture
def sample_project() -> dict:
    return {
        "id": 123,
        "name": "test-project",
        "path_with_namespace": "group/test-project",
        "web_url": "https://gitlab.example.com/group/test-project",
        "default_branch": "main",
        "description": "A test project",
        "visibility": "private",
        "star_count": 5,
        "forks_count": 2,
        "open_issues_count": 3,
        "created_at": "2024-01-01T00:00:00Z",
        "last_activity_at": "2024-06-15T12:00:00Z",
    }


@pytest.fixture
def sample_mr() -> dict:
    return {
        "id": 456,
        "iid": 1,
        "title": "Add new feature",
        "description": "Feature description",
        "state": "opened",
        "source_branch": "feature-branch",
        "target_branch": "main",
        "author": {"id": 1, "username": "testuser", "name": "Test User"},
        "web_url": "https://gitlab.example.com/group/test-project/-/merge_requests/1",
        "draft": False,
        "merge_status": "can_be_merged",
        "has_conflicts": False,
        "created_at": "2024-01-15T10:00:00Z",
        "updated_at": "2024-01-16T14:30:00Z",
    }

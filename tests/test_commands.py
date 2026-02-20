"""Tests for CLI commands."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import qodev_gitlab_cli.context as _ctx


class TestProjectsCommand:
    def test_projects_get_json(self, sample_project: dict, capsys) -> None:
        mock_client = MagicMock()
        mock_client.get_project.return_value = sample_project

        _ctx.ctx.configure(json_mode=True, token=None, base_url=None, project="group/test-project", limit=25, page=1)

        with patch.object(_ctx.ctx, "client", return_value=mock_client):
            from qodev_gitlab_cli.commands.projects import get

            get(id="group/test-project")

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["name"] == "test-project"
        assert data["id"] == 123

    def test_projects_list_json(self, capsys) -> None:
        mock_client = MagicMock()
        mock_client.get_projects.return_value = [
            {"id": 1, "name": "proj1"},
            {"id": 2, "name": "proj2"},
        ]

        _ctx.ctx.configure(json_mode=True, token=None, base_url=None, project=None, limit=25, page=1)

        with patch.object(_ctx.ctx, "client", return_value=mock_client):
            from qodev_gitlab_cli.commands.projects import list

            list(owned=False)

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert len(data["items"]) == 2
        mock_client.get_projects.assert_called_once_with(owned=False)


class TestMrsCommand:
    def test_mrs_list_json(self, sample_mr: dict, capsys) -> None:
        mock_client = MagicMock()
        mock_client.get_merge_requests.return_value = [sample_mr]

        _ctx.ctx.configure(json_mode=True, token=None, base_url=None, project="group/project", limit=25, page=1)

        with patch.object(_ctx.ctx, "client", return_value=mock_client):
            from qodev_gitlab_cli.commands.mrs import list

            list(state="opened")

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert len(data["items"]) == 1
        assert data["items"][0]["title"] == "Add new feature"

    def test_mrs_get_json(self, sample_mr: dict, capsys) -> None:
        mock_client = MagicMock()
        mock_client.get_merge_request.return_value = sample_mr

        _ctx.ctx.configure(json_mode=True, token=None, base_url=None, project="group/project", limit=25, page=1)

        with patch.object(_ctx.ctx, "client", return_value=mock_client):
            from qodev_gitlab_cli.commands.mrs import get

            get(iid=1)

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["iid"] == 1
        assert data["title"] == "Add new feature"

    def test_mrs_close_json(self, sample_mr: dict, capsys) -> None:
        closed = {**sample_mr, "state": "closed"}
        mock_client = MagicMock()
        mock_client.close_mr.return_value = closed

        _ctx.ctx.configure(json_mode=True, token=None, base_url=None, project="group/project", limit=25, page=1)

        with patch.object(_ctx.ctx, "client", return_value=mock_client):
            from qodev_gitlab_cli.commands.mrs import close

            close(iid=1)

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["state"] == "closed"

    def test_mrs_comment_json(self, capsys) -> None:
        mock_client = MagicMock()
        mock_client.create_mr_note.return_value = {"id": 1, "body": "LGTM"}

        _ctx.ctx.configure(json_mode=True, token=None, base_url=None, project="group/project", limit=25, page=1)

        with patch.object(_ctx.ctx, "client", return_value=mock_client):
            from qodev_gitlab_cli.commands.mrs import comment

            comment(iid=1, body="LGTM")

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["body"] == "LGTM"

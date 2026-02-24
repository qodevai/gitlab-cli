"""Tests for the install command."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from qodev_gitlab_cli.commands.install import _install_skills, install


class TestInstallSkills:
    def test_copies_skill_files(self, tmp_path: Path) -> None:
        _install_skills(target_root=tmp_path)

        dest = tmp_path / ".claude" / "skills" / "qodev-gitlab"
        assert dest.exists()
        assert (dest / "SKILL.md").is_file()
        assert (dest / "references" / "mr-workflows.md").is_file()
        assert (dest / "references" / "pipeline-monitoring.md").is_file()

    def test_does_not_copy_dunder_files(self, tmp_path: Path) -> None:
        _install_skills(target_root=tmp_path)

        dest = tmp_path / ".claude" / "skills" / "qodev-gitlab"
        for path in dest.rglob("*"):
            assert not path.name.startswith("__"), f"Unexpected dunder file: {path}"

    def test_skill_md_has_content(self, tmp_path: Path) -> None:
        _install_skills(target_root=tmp_path)

        skill_md = tmp_path / ".claude" / "skills" / "qodev-gitlab" / "SKILL.md"
        content = skill_md.read_text()
        assert "qodev-gitlab" in content
        assert "Command Reference" in content

    def test_replaces_existing_directory(self, tmp_path: Path) -> None:
        dest = tmp_path / ".claude" / "skills" / "qodev-gitlab"
        dest.mkdir(parents=True)
        stale = dest / "old-file.txt"
        stale.write_text("should be removed")

        _install_skills(target_root=tmp_path)

        assert not stale.exists()
        assert (dest / "SKILL.md").is_file()

    def test_no_flag_exits_with_validation_error(self) -> None:
        with pytest.raises(SystemExit, match="83"):
            install(skills=False)

    def test_skills_flag_prints_success(self, tmp_path: Path) -> None:
        with patch("qodev_gitlab_cli.commands.install.console") as mock_console, \
             patch("qodev_gitlab_cli.commands.install.Path") as mock_path:
            mock_path.cwd.return_value = tmp_path
            install(skills=True)

        calls = [str(c) for c in mock_console.print.call_args_list]
        assert any("Installed skills" in c for c in calls)

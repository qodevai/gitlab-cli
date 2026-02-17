"""Git remote → GitLab project path detection."""

from __future__ import annotations

import logging
import os
import re
import subprocess

logger = logging.getLogger(__name__)


def detect_project_from_git(base_url: str | None = None) -> str | None:
    """Detect GitLab project path from the current git remote.

    Returns namespace/project string or None.
    """
    git_root = _find_git_root(os.getcwd())
    if not git_root:
        return None

    remote_url = _get_remote_url(git_root)
    if not remote_url:
        return None

    return _parse_project_path(remote_url, base_url)


def _find_git_root(start_path: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=start_path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return None


def _get_remote_url(git_root: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=git_root,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return None


def get_current_branch() -> str | None:
    """Get the current git branch name."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return None


def _parse_project_path(remote_url: str, base_url: str | None = None) -> str | None:
    """Extract project path from SSH or HTTPS remote URL."""
    # Determine the domain to match against
    if base_url:
        domain_match = re.search(r"https?://([^/]+)", base_url)
        domain = domain_match.group(1) if domain_match else None
    else:
        domain = None

    # SSH: git@gitlab.example.com:group/project.git
    ssh_match = re.match(r"git@([^:]+):(.+?)(?:\.git)?$", remote_url)
    if ssh_match:
        host = ssh_match.group(1)
        path = ssh_match.group(2)
        if domain is None or host == domain:
            return path

    # HTTPS: https://gitlab.example.com/group/project.git
    https_match = re.match(r"https?://([^/]+)/(.+?)(?:\.git)?$", remote_url)
    if https_match:
        host = https_match.group(1)
        path = https_match.group(2)
        if domain is None or host == domain:
            return path

    return None

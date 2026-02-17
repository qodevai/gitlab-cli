"""Tests for output formatting."""

from __future__ import annotations

import json
from datetime import datetime

from gitlab_cli.context import Context
from gitlab_cli.output import generic_markdown, md_table, serialize


class TestSerialize:
    def test_datetime(self) -> None:
        dt = datetime(2024, 1, 15, 10, 0, 0)
        assert serialize(dt) == "2024-01-15T00:00:00" or serialize(dt) == dt.isoformat()

    def test_nested_dict(self) -> None:
        data = {"a": 1, "b": {"c": 2}}
        result = serialize(data)
        assert result == {"a": 1, "b": {"c": 2}}

    def test_list(self) -> None:
        data = [{"id": 1}, {"id": 2}]
        result = serialize(data)
        assert len(result) == 2

    def test_passthrough(self) -> None:
        assert serialize("hello") == "hello"
        assert serialize(42) == 42


class TestMdTable:
    def test_basic_table(self) -> None:
        rows = [{"id": "1", "name": "Alice"}, {"id": "2", "name": "Bob"}]
        headers = [("ID", "id"), ("Name", "name")]
        result = md_table(rows, headers)
        assert "| ID | Name |" in result
        assert "| 1 | Alice |" in result
        assert "| 2 | Bob |" in result

    def test_empty_rows(self) -> None:
        result = md_table([], [("ID", "id")])
        assert "No results" in result

    def test_missing_key(self) -> None:
        rows = [{"id": "1"}]
        headers = [("ID", "id"), ("Missing", "missing")]
        result = md_table(rows, headers)
        assert "| 1 |  |" in result


class TestGenericMarkdown:
    def test_dict(self) -> None:
        data = {"name": "test", "status": "active"}
        result = generic_markdown(data)
        assert "Name" in result
        assert "test" in result

    def test_list(self) -> None:
        data = [{"id": 1}, {"id": 2}]
        result = generic_markdown(data)
        assert "Id" in result

    def test_empty_list(self) -> None:
        result = generic_markdown([])
        assert "No results" in result

    def test_string(self) -> None:
        assert generic_markdown("hello") == "hello"

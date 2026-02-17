"""Tests for formatter helpers."""

from __future__ import annotations

from gitlab_cli.formatters.generic import _fmt, _get, detail_table, list_table


class TestGet:
    def test_simple_key(self) -> None:
        assert _get({"name": "Alice"}, "name") == "Alice"

    def test_dot_notation(self) -> None:
        assert _get({"author": {"name": "Bob"}}, "author.name") == "Bob"

    def test_missing_key(self) -> None:
        assert _get({"a": 1}, "b") is None

    def test_missing_nested(self) -> None:
        assert _get({"a": {"b": 1}}, "a.c") is None

    def test_none_intermediate(self) -> None:
        assert _get({"a": None}, "a.b") is None


class TestFmt:
    def test_none(self) -> None:
        assert _fmt(None) == ""

    def test_bool_true(self) -> None:
        assert _fmt(True) == "Yes"

    def test_bool_false(self) -> None:
        assert _fmt(False) == "No"

    def test_string(self) -> None:
        assert _fmt("hello") == "hello"

    def test_int(self) -> None:
        assert _fmt(42) == "42"

    def test_list_of_names(self) -> None:
        users = [{"name": "Alice"}, {"name": "Bob"}]
        assert _fmt(users) == "Alice, Bob"

    def test_list_of_strings(self) -> None:
        assert _fmt(["a", "b", "c"]) == "a, b, c"

    def test_empty_list(self) -> None:
        assert _fmt([]) == ""

    def test_dict_with_name(self) -> None:
        assert _fmt({"name": "Alice", "id": 1}) == "Alice"


class TestDetailTable:
    def test_basic(self) -> None:
        data = {"id": 1, "name": "Test"}
        fields = [("ID", "id"), ("Name", "name")]
        result = detail_table(data, fields)
        assert "| ID | 1 |" in result
        assert "| Name | Test |" in result

    def test_with_title(self) -> None:
        result = detail_table({"id": 1}, [("ID", "id")], title="My Title")
        assert "# My Title" in result

    def test_skips_empty_values(self) -> None:
        data = {"id": 1, "name": None, "desc": ""}
        fields = [("ID", "id"), ("Name", "name"), ("Description", "desc")]
        result = detail_table(data, fields)
        assert "| ID | 1 |" in result
        assert "Name" not in result
        assert "Description" not in result


class TestListTable:
    def test_basic(self) -> None:
        items = [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]
        columns = [("ID", "id"), ("Name", "name")]
        result = list_table(items, columns, title="Items")
        assert "# Items" in result
        assert "| 1 | A |" in result

    def test_empty(self) -> None:
        result = list_table([], [("ID", "id")], title="Empty")
        assert "No results" in result

    def test_total_and_page(self) -> None:
        items = [{"id": 1}]
        result = list_table(items, [("ID", "id")], title="Items", total=50, page=2)
        assert "page 2" in result
        assert "50 total" in result

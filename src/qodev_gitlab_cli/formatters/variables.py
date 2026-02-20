"""CI/CD variable formatters."""

from __future__ import annotations

from typing import Any

from qodev_gitlab_cli.formatters.generic import detail_table, list_table

VARIABLE_DETAIL_FIELDS = [
    ("Key", "key"),
    ("Type", "variable_type"),
    ("Protected", "protected"),
    ("Masked", "masked"),
    ("Raw", "raw"),
    ("Environment", "environment_scope"),
    ("Description", "description"),
]

VARIABLE_LIST_COLUMNS = [
    ("Key", "key"),
    ("Type", "variable_type"),
    ("Protected", "protected"),
    ("Masked", "masked"),
    ("Environment", "environment_scope"),
]


def format_variable_detail(data: Any) -> str:
    key = data.get("key", "?") if isinstance(data, dict) else "?"
    return detail_table(data, VARIABLE_DETAIL_FIELDS, title=f"Variable: {key}")


def format_variable_list(items: list[Any], *, total: int = 0, page: int = 1) -> str:
    return list_table(items, VARIABLE_LIST_COLUMNS, title="CI/CD Variables", total=total, page=page)

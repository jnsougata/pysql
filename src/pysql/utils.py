from typing import Union, Optional, List, Dict, Any
from enum import Enum


class Types(Enum):
    TEXT = "TEXT"
    INTEGER = "INTEGER"
    REAL = "REAL"
    BLOB = "BLOB"
    NULL = "NULL"


class Field:
    def __init__(self, name: str, value: Optional[Union[str, int, float, bytes]] = None):
        self.name = name
        self.value = value


class Condition:

    def __init__(self, query: str):
        self.value = query

    @classmethod
    def equal(cls, name: str, value: Optional[Union[str, int, float, bytes]] = None):
        if isinstance(value, str):
            return cls(f"{name} = '{value}'")
        return cls(f"{name} = {value}")

    @classmethod
    def not_equal(cls, name: str, value: Optional[Union[str, int, float, bytes]] = None):
        if isinstance(value, str):
            return cls(f"{name} != '{value}'")
        return cls(f"{name} != {value}")

    @classmethod
    def greater_than(cls, name: str, value: Optional[Union[str, int, float, bytes]] = None):
        return cls(f"{name} > {value}")

    @classmethod
    def greater_equal(cls, name: str, value: Optional[Union[str, int, float, bytes]] = None):
        return cls(f"{name} >= {value}")

    @classmethod
    def less_than(cls, name: str, value: Optional[Union[str, int, float, bytes]] = None):
        return cls(f"{name} < {value}")

    @classmethod
    def less_equal(cls, name: str, value: Optional[Union[str, int, float, bytes]] = None):
        return cls(f"{name} <= {value}")

    @classmethod
    def between(
            cls,
            name: str,
            start: Optional[Union[str, int, float, bytes]],
            end: Optional[Union[str, int, float, bytes]]
    ):
        return cls(f"{name} BETWEEN {start} AND {end}")

    @classmethod
    def like(cls, name: str, value: Optional[Union[str, int, float, bytes]] = None):
        return cls(f"{name} LIKE {value}*")

    @classmethod
    def in_list(cls, name: str, values: List[Optional[Union[str, int, float, bytes]]] = None):
        for index, v in values:
            if isinstance(v, str):
                values[index] = f"'{v}'"
        return cls(f"{name} IN ({values.join(', ')})")

    @classmethod
    def not_in_list(cls, name: str, values: List[Optional[Union[str, int, float, bytes]]] = None):
        for index, v in values:
            if isinstance(v, str):
                values[index] = f"'{v}'"
        return cls(f"{name} NOT IN ({values.join(', ')})")

    @classmethod
    def and_clause(cls, conditions):
        return cls(f"({conditions.join(' AND ')})")

    @classmethod
    def or_clause(cls, conditions):
        return cls(f"({conditions.join(' OR ')})")

import sqlite3
from typing import Dict, List, Any
from .utils import Field, Types, Condition
from .errors import PySQLException


class PySQL:

    def __init__(self, path: str):
        self.__path = path
        self.connection = sqlite3.connect(self.__path)
        self.cursor = self.connection.cursor()

    def view(self, table: str) -> None:
        self.cursor.execute(f'SELECT * FROM {table}')
        print(self.cursor.fetchall())

    def select(
            self,
            table: str,
            columns: List[str] = None,
            *,
            order_by: List[str] = None,
            limit: int = None,
            start: int = None,
            condition: Condition = None
    ) -> list:
        if columns:
            cols = ', '.join(columns)
            query = f'SELECT DISTINCT {cols} FROM {table}'
        else:
            query = f'SELECT DISTINCT * FROM {table}'

        if order_by:
            query += f' ORDER BY {", ".join(order_by)}'
        if limit:
            query += f' LIMIT {limit}'
        if start:
            query += f' OFFSET {start}'
        if condition:
            query += f' WHERE {condition.value}'
        try:
            self.cursor.execute(query)
        except sqlite3.OperationalError as e:
            raise PySQLException(e) from None
        else:
            return self.cursor.fetchall()

    def insert(self, table: str, fields: List[Field]):
        cols = ', '.join(f.name for f in fields)
        vals = [f.value for f in fields]
        for index, val in enumerate(vals):
            if isinstance(val, str):
                vals[index] = f"'{val}'"
        container = []
        for val in vals:
            if not isinstance(val, str) and val is not None:
                container.append(str(val))
            elif val is None:
                container.append('NULL')
            else:
                container.append(val)
        query = (f'INSERT INTO {table} ({cols}) '
                 f'VALUES ({", ".join(container)})')
        try:
            self.cursor.execute(query)
        except sqlite3.OperationalError as e:
            raise PySQLException(e) from None
        else:
            self.connection.commit()
            return {f.name: f.value for f in fields}

    def create(self, table: str, columns: Dict[str, Types]):
        cols = ', '.join(f'{k} {v.value}' for k, v in columns.items())
        try:
            self.cursor.execute(f"CREATE TABLE {table} ({cols})")
        except sqlite3.OperationalError as e:
            raise PySQLException(e) from None
        else:
            self.connection.commit()
            return self

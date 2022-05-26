import sqlite3
from typing import Dict, List, Any
from .utils import Field, Types, Condition
from .errors import *


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
            query = f'SELECT {cols} FROM {table}'
        else:
            query = f'SELECT * FROM {table}'

        if order_by:
            query += f' ORDER BY {", ".join(order_by)}'
        if limit:
            query += f' LIMIT {limit}'
        if start:
            query += f' OFFSET {start}'
        if condition:
            query += f' WHERE {condition.value}'

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert(self, table: str, fields: List[Field]):
        cols = ', '.join(f.name for f in fields)
        vals = [f.value for f in fields]
        for index, val in enumerate(vals):
            if isinstance(val, str):
                vals[index] = f"'{val}'"
        modified_values = [str(v) for v in vals if not isinstance(v, str) or v]
        query = (f'INSERT INTO {table} ({cols}) '
                 f'VALUES ({", ".join(modified_values)})')
        self.cursor.execute(query)
        self.connection.commit()
        return {f.name: f.value for f in fields}


    def create(self, table: str, columns: Dict[str, Types]):
        cols = ', '.join(f'{k} {v.value}' for k, v in columns.items())
        try:
            self.cursor.execute(f"CREATE TABLE {table} ({cols})")
        except sqlite3.OperationalError:
            raise AlreadyExists(f'Table `{table}` already exists in `{self.__path}`')
        else:
            self.connection.commit()
            return self

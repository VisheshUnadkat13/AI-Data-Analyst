"""
sql_tool.py

Provides SQL capabilities over uploaded Pandas DataFrames
using DuckDB.
"""

from __future__ import annotations

import pandas as pd
import duckdb

class SQLTool:

    """
    Executes SQL queries on uploaded DataFrames.
    """

    def __init__(self):
        self.connection = duckdb.connect(database=":memory:")
        self.registered_tables: dict[str, pd.DataFrame] = {}

    # --------------------------------------------------
    # Registration
    # --------------------------------------------------   

    def register_dataframe(
            self,
            table_name:str,
            dataframe:pd.DataFrame,
    )->None:
        """
        Register a dataframe as a DuckDB table.
        """

        self.connection.register(table_name, dataframe)

        self.registered_tables[table_name] = dataframe

    def register_multiple(
        self,
        datasets: dict[str, pd.DataFrame],
    ) -> None:
        """
        Register multiple dataframes.
        """

        for table_name, dataframe in datasets.items():
            self.register_dataframe(
                table_name,
                dataframe,
            )

    # --------------------------------------------------
    # Query Execution
    # --------------------------------------------------

    def execute(
        self,
        sql: str,
    ) -> pd.DataFrame:
        """
        Execute SQL and return DataFrame.
        """

        try:

            result = self.connection.execute(sql)

            return result.fetch_df()

        except Exception as ex:

            raise RuntimeError(
                f"SQL execution failed:\n{ex}"
            )

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    def list_tables(self)->list[str]:
        """
        List Registered tables.
        """    
        return list(self.registered_tables.keys())

    def describe_table(

        self,
        table_name:str,
    )->pd.DataFrame:
        """
         Describe table schema.
        """
        if table_name not in self.registered_tables:

            raise ValueError(
                f"Table '{table_name}' not found."
            )

        return self.execute(
            f"DESCRIBE {table_name}"
        )

    def preview_table(
        self,
        table_name: str,
        limit: int = 5,
    ) -> pd.DataFrame:
        """
        Preview table rows.
        """

        return self.execute(
            f"""
            SELECT *
            FROM {table_name}
            LIMIT {limit}
            """
        )


    # --------------------------------------------------
    # Management
    # --------------------------------------------------

    def unregister(
        self,
        table_name: str,
    ) -> None:
        """
        Remove registered table.
        """

        if table_name in self.registered_tables:

            self.connection.unregister(
                table_name
            )

            del self.registered_tables[
                table_name
            ]

    def clear(self):
        """
        Remove every table.
        """

        for table in list(
            self.registered_tables.keys()
        ):
            self.connection.unregister(table)

        self.registered_tables.clear()

    # --------------------------------------------------
    # Utility
    # --------------------------------------------------

    def table_exists(
        self,
        table_name: str,
    ) -> bool:

        return table_name in self.registered_tables

    def __repr__(self):

        return (
            f"SQLTool("
            f"tables={self.list_tables()})"
        )
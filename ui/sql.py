"""
sql.py

SQL Workspace UI.

Responsible only for rendering the SQL interface.

Business logic remains inside SQLTool.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.tools.sql_tool import SQLTool
from ui.components import UIComponents


class SQLUI:
    """
    SQL Workspace UI.
    """

    DEFAULT_QUERY = """SELECT *
FROM dataframe
LIMIT 10;"""

    def __init__(self):

        self.sql_tool = SQLTool()

    # --------------------------------------------------
    # Main Render
    # --------------------------------------------------

    def render(
        self,
        df: pd.DataFrame,
    ) -> None:
        """
        Render SQL workspace.
        """

        UIComponents.section(
            "SQL Workspace",
            "🗄️",
        )

        if df is None or df.empty:

            UIComponents.info(
                "Upload a dataset before executing SQL."
            )

            return

        st.markdown(
            """
Execute SQL queries using **DuckDB**.

The uploaded dataframe is available as:

`dataframe`
"""
        )

        query = st.text_area(
            "SQL Query",
            value=self.DEFAULT_QUERY,
            height=220,
        )

        col1, col2 = st.columns([1, 5])

        with col1:

            execute = st.button(
                "▶ Execute",
                type="primary",
                use_container_width=True,
            )

        with col2:

            clear = st.button(
                "🗑 Clear",
                use_container_width=True,
            )

        if clear:

            st.rerun()

        if not execute:
            return

        with UIComponents.loading(
            "Executing SQL..."
        ):

            try:

                result = self.sql_tool.execute(
                    df=df,
                    query=query,
                )

            except Exception as e:

                UIComponents.error(str(e))
                return

        UIComponents.divider()

        UIComponents.section(
            "Query Result",
            "📋",
        )

        if result is None:

            UIComponents.warning(
                "No rows returned."
            )

            return

        if isinstance(result, pd.DataFrame):

            UIComponents.metrics(
                {
                    "Rows": len(result),
                    "Columns": len(result.columns),
                }
            )

            UIComponents.dataframe(result)

            UIComponents.download_dataframe(
                result,
                filename="sql_result.csv",
            )

            return

        st.write(result)
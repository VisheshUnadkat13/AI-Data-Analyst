"""
explorer.py

Dataset Explorer UI.

Responsible only for rendering dataset information.
All business logic lives inside AnalysisService.
"""

from __future__ import annotations

import streamlit as st
import pandas as pd

from src.services.analysis_service import AnalysisService
from ui.components import UIComponents


class ExplorerUI:
    """
    Dataset Explorer page.
    """

    def __init__(self):

        self.analysis = AnalysisService()

    # ---------------------------------------------------------
    # Main Render
    # ---------------------------------------------------------

    def render(
        self,
        df: pd.DataFrame,
        dataset_name: str,
    ) -> None:
        """
        Render the complete explorer.
        """

        if df is None or df.empty:

            UIComponents.empty(
                "Upload a dataset to begin."
            )
            return

        UIComponents.section(
            "Dataset Explorer",
            "📊"
        )

        st.caption(f"Active Dataset : **{dataset_name}**")

        self._metrics(df)

        UIComponents.divider()

        self._preview(df)

        UIComponents.divider()

        self._statistics(df)

        UIComponents.divider()

        self._data_types(df)

        UIComponents.divider()

        self._missing_values(df)

        UIComponents.divider()

        self._duplicates(df)

    # ---------------------------------------------------------
    # Metrics
    # ---------------------------------------------------------

    def _metrics(
        self,
        df: pd.DataFrame,
    ) -> None:

        summary = self.analysis.summary(df)

        duplicate_info = self.analysis.duplicates(df)

        missing = self.analysis.missing_values(df)

        total_missing = int(
            missing["Missing Values"].sum()
        )

        UIComponents.metrics(
            {
                "Rows": summary["rows"],
                "Columns": summary["columns"],
                "Missing": total_missing,
                "Duplicates": duplicate_info["duplicate_rows"],
            }
        )

    # ---------------------------------------------------------
    # Preview
    # ---------------------------------------------------------

    def _preview(
        self,
        df: pd.DataFrame,
    ) -> None:

        with UIComponents.expander(
            "Dataset Preview"
        ):

            rows = st.slider(
                "Rows",
                min_value=5,
                max_value=min(100, len(df)),
                value=min(10, len(df)),
            )

            UIComponents.dataframe(
                self.analysis.top_rows(df, rows)
            )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def _statistics(
        self,
        df: pd.DataFrame,
    ) -> None:

        with UIComponents.expander(
            "Descriptive Statistics"
        ):

            stats = self.analysis.describe(df)

            if stats.empty:

                UIComponents.info(
                    "No numeric columns found."
                )

            else:

                UIComponents.dataframe(stats)

    # ---------------------------------------------------------
    # Data Types
    # ---------------------------------------------------------

    def _data_types(
        self,
        df: pd.DataFrame,
    ) -> None:

        with UIComponents.expander(
            "Column Information"
        ):

            info = pd.DataFrame(
                {
                    "Column": df.columns,
                    "Data Type": df.dtypes.astype(str),
                    "Non Null": df.count().values,
                }
            )

            UIComponents.dataframe(info)

    # ---------------------------------------------------------
    # Missing Values
    # ---------------------------------------------------------

    def _missing_values(
        self,
        df: pd.DataFrame,
    ) -> None:

        with UIComponents.expander(
            "Missing Values"
        ):

            missing = self.analysis.missing_values(df)

            UIComponents.dataframe(missing)

    # ---------------------------------------------------------
    # Duplicate Rows
    # ---------------------------------------------------------

    def _duplicates(
        self,
        df: pd.DataFrame,
    ) -> None:

        with UIComponents.expander(
            "Duplicate Rows"
        ):

            duplicate_info = self.analysis.duplicates(df)

            UIComponents.json(
                duplicate_info
            )
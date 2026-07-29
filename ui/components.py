"""
components.py

Reusable Streamlit UI components.

These helper functions keep the UI clean and avoid
duplicating Streamlit code across different pages.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any

import pandas as pd
import streamlit as st


class UIComponents:
    """
    Collection of reusable UI widgets.
    """

    # --------------------------------------------------
    # Section Header
    # --------------------------------------------------

    @staticmethod
    def section(title: str, icon: str = "") -> None:
        """
        Display a section title.
        """

        if icon:
            st.markdown(f"## {icon} {title}")
        else:
            st.markdown(f"## {title}")

    # --------------------------------------------------
    # Divider
    # --------------------------------------------------

    @staticmethod
    def divider() -> None:
        st.divider()

    # --------------------------------------------------
    # Metric Cards
    # --------------------------------------------------

    @staticmethod
    def metrics(metrics: dict[str, Any]) -> None:
        """
        Display metrics in columns.

        Example:
        {
            "Rows":1000,
            "Columns":12,
            "Missing":4
        }
        """

        if not metrics:
            return

        cols = st.columns(len(metrics))

        for col, (label, value) in zip(cols, metrics.items()):
            col.metric(label, value)

    # --------------------------------------------------
    # Messages
    # --------------------------------------------------

    @staticmethod
    def success(message: str) -> None:
        st.success(message)

    @staticmethod
    def warning(message: str) -> None:
        st.warning(message)

    @staticmethod
    def error(message: str) -> None:
        st.error(message)

    @staticmethod
    def info(message: str) -> None:
        st.info(message)

    # --------------------------------------------------
    # Empty State
    # --------------------------------------------------

    @staticmethod
    def empty(message: str = "No data available.") -> None:
        st.info(message)

    # --------------------------------------------------
    # DataFrame Viewer
    # --------------------------------------------------

    @staticmethod
    def dataframe(
        df: pd.DataFrame,
        height: int = 400,
    ) -> None:
        """
        Display dataframe.
        """

        st.dataframe(
            df,
            use_container_width=True,
            height=height,
        )

    # --------------------------------------------------
    # JSON Viewer
    # --------------------------------------------------

    @staticmethod
    def json(data: Any) -> None:
        st.json(data)

    # --------------------------------------------------
    # Code Block
    # --------------------------------------------------

    @staticmethod
    def code(
        code: str,
        language: str = "python",
    ) -> None:

        st.code(
            code,
            language=language,
        )

    # --------------------------------------------------
    # Download CSV
    # --------------------------------------------------

    @staticmethod
    def download_dataframe(
        df: pd.DataFrame,
        filename: str = "result.csv",
        label: str = "Download CSV",
    ) -> None:
        """
        Download dataframe as CSV.
        """

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label=label,
            data=csv,
            file_name=filename,
            mime="text/csv",
            use_container_width=True,
        )

    # --------------------------------------------------
    # Expander
    # --------------------------------------------------

    @staticmethod
    def expander(title: str):
        return st.expander(title, expanded=False)

    # --------------------------------------------------
    # Spinner
    # --------------------------------------------------

    @staticmethod
    @contextmanager
    def loading(text: str = "Processing..."):
        """
        Context manager for loading spinner.

        Usage:
        with UIComponents.loading():
            ...
        """
        with st.spinner(text):
            yield
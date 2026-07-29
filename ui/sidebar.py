"""
sidebar.py

Streamlit sidebar for the AI Data Analyst application.
Responsible only for rendering sidebar UI and returning
user selections.

Business logic should remain inside the src/ package.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


class Sidebar:
    """
    Renders the application sidebar.
    """

    @staticmethod
    def render(
        dataframe_manager: Any,
    ) -> dict:
        """
        Render sidebar.

        Parameters
        ----------
        dataframe_manager
            Instance of DataFrameManager.

        Returns
        -------
        dict
            User selections from the sidebar.
        """

        with st.sidebar:

            st.title("📊 AI Data Analyst")

            st.markdown("---")

            uploaded_files = st.file_uploader(
                label="Upload CSV File(s)",
                type=["csv"],
                accept_multiple_files=True,
            )

            st.markdown("---")

            datasets = dataframe_manager.list_dataframes()

            active_dataset = None

            if datasets:

                active_dataset = st.selectbox(
                    "Active Dataset",
                    datasets,
                )

            st.markdown("---")

            if active_dataset:

                df = dataframe_manager.get_dataframe(
                    active_dataset
                )

                rows, cols = df.shape

                st.subheader("Dataset Info")

                st.metric(
                    "Rows",
                    rows,
                )

                st.metric(
                    "Columns",
                    cols,
                )

            st.markdown("---")

            clear_clicked = st.button(
                "🗑 Clear Session",
                use_container_width=True,
            )

            st.markdown("---")

            st.caption("AI Data Analyst v1.0")

        return {

            "uploaded_files": uploaded_files,

            "active_dataset": active_dataset,

            "clear_session": clear_clicked,

        }
"""
anomaly.py

Anomaly Detection UI.

Responsible only for rendering the anomaly detection page.

Business logic lives inside AnomalyTool.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.tools.anomaly_tool import AnomalyTool
from ui.components import UIComponents


class AnomalyUI:
    """
    Anomaly Detection Page.
    """

    def __init__(self):

        self.anomaly_tool = AnomalyTool()

    # --------------------------------------------------
    # Main Render
    # --------------------------------------------------

    def render(
        self,
        df: pd.DataFrame,
    ) -> None:
        """
        Render anomaly detection page.
        """

        UIComponents.section(
            "Anomaly Detection",
            "🚨",
        )

        if df is None or df.empty:

            UIComponents.info(
                "Upload a dataset to detect anomalies."
            )

            return

        st.markdown(
            """
Detect unusual records in your dataset using AI and statistical techniques.

Typical anomalies include:

- Outliers
- Unexpected values
- Suspicious records
- Data inconsistencies
"""
        )

        if st.button(
            "🔍 Detect Anomalies",
            type="primary",
            use_container_width=True,
        ):

            with UIComponents.loading(
                "Analyzing dataset..."
            ):

                try:

                    result = self.anomaly_tool.detect(df)

                except Exception as e:

                    UIComponents.error(str(e))
                    return

            self._render_result(result)

    # --------------------------------------------------
    # Render Result
    # --------------------------------------------------

    def _render_result(
        self,
        result,
    ) -> None:

        UIComponents.divider()

        UIComponents.section(
            "Detection Result",
            "📊",
        )

        if result is None:

            UIComponents.warning(
                "No anomalies detected."
            )

            return

        # ------------------------------------------
        # Dictionary Response
        # ------------------------------------------

        if isinstance(result, dict):

            summary = {}

            anomaly_df = None

            explanation = None

            for key, value in result.items():

                if isinstance(value, pd.DataFrame):

                    anomaly_df = value

                elif isinstance(value, dict):

                    summary.update(value)

                elif isinstance(value, str):

                    explanation = value

                else:

                    summary[key] = value

            if summary:

                UIComponents.metrics(summary)

            if explanation:

                st.subheader("Explanation")

                st.write(explanation)

            if anomaly_df is not None:

                st.subheader("Detected Anomalies")

                UIComponents.dataframe(anomaly_df)

                UIComponents.download_dataframe(
                    anomaly_df,
                    filename="anomalies.csv",
                )

            return

        # ------------------------------------------
        # DataFrame Response
        # ------------------------------------------

        if isinstance(result, pd.DataFrame):

            UIComponents.metrics(
                {
                    "Detected Rows": len(result)
                }
            )

            UIComponents.dataframe(result)

            UIComponents.download_dataframe(
                result,
                filename="anomalies.csv",
            )

            return

        # ------------------------------------------
        # List Response
        # ------------------------------------------

        if isinstance(result, list):

            st.subheader("Detected Anomalies")

            for item in result:

                st.markdown(f"- {item}")

            return

        # ------------------------------------------
        # String Response
        # ------------------------------------------

        st.write(result)
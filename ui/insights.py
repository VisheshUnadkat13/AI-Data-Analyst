"""
insights.py

Business Insights UI.

Responsible only for rendering the business insights page.

Business logic lives inside InsightTool.
"""

from __future__ import annotations

import json
import streamlit as st
import pandas as pd

from src.tools.insight_tool import InsightTool
from ui.components import UIComponents


class InsightsUI:
    """
    Business Insights Page.
    """

    def __init__(self):

        self.insight_tool = InsightTool()

    # --------------------------------------------------
    # Main Render
    # --------------------------------------------------

    def render(
        self,
        df: pd.DataFrame,
    ) -> None:
        """
        Render Business Insights page.
        """

        UIComponents.section(
            "Business Insights",
            "💡",
        )

        if df is None or df.empty:

            UIComponents.info(
                "Upload a dataset to generate business insights."
            )

            return

        st.markdown(
            """
Generate AI-powered business insights from your dataset.

The insights may include:

- Key trends
- Business observations
- Recommendations
- Risks
- Opportunities
"""
        )

        if st.button(
            "✨ Generate Insights",
            type="primary",
            use_container_width=True,
        ):

            with UIComponents.loading(
                "Generating insights..."
            ):

                try:

                    insights = self.insight_tool.generate_insights(
                        df
                    )

                except Exception as e:

                    UIComponents.error(str(e))
                    return

            self._render_insights(insights)

    # --------------------------------------------------
    # Render Insights
    # --------------------------------------------------

    def _render_insights(
        self,
        insights,
    ) -> None:

        UIComponents.divider()

        UIComponents.section(
            "Generated Insights",
            "📊",
        )

        if insights is None:

            UIComponents.warning(
                "No insights generated."
            )

            return

        # ------------------------------------------
        # Dictionary Response
        # ------------------------------------------

        if isinstance(insights, dict):

            for key, value in insights.items():

                st.subheader(
                    key.replace(
                        "_",
                        " "
                    ).title()
                )

                if isinstance(value, list):

                    for item in value:

                        st.markdown(
                            f"- {item}"
                        )

                elif isinstance(value, dict):

                    st.json(value)

                else:

                    st.write(value)

        # ------------------------------------------
        # List Response
        # ------------------------------------------

        elif isinstance(insights, list):

            for item in insights:

                st.markdown(
                    f"- {item}"
                )

        # ------------------------------------------
        # String Response
        # ------------------------------------------

        else:

            st.markdown(str(insights))

        UIComponents.divider()

        self._download_button(insights)

    # --------------------------------------------------
    # Download
    # --------------------------------------------------

    def _download_button(
        self,
        insights,
    ) -> None:

        if isinstance(insights, dict):

            content = json.dumps(
                insights,
                indent=4,
            )

            filename = "business_insights.json"

        elif isinstance(insights, list):

            content = "\n".join(
                str(i)
                for i in insights
            )

            filename = "business_insights.txt"

        else:

            content = str(insights)

            filename = "business_insights.txt"

        st.download_button(

            label="⬇ Download Insights",

            data=content,

            file_name=filename,

            mime="text/plain",

            use_container_width=True,

        )
"""
charts.py

Visualization UI for AI Data Analyst.

Responsible only for rendering the chart interface.
Business logic lives inside ChartTool.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.tools.chart_tool import ChartTool
from ui.components import UIComponents


class ChartsUI:
    """
    Visualization page.
    """

    SUPPORTED_CHARTS = [
        "Bar",
        "Line",
        "Pie",
        "Scatter",
        "Histogram",
        "Box Plot",
    ]

    def __init__(self):

        self.chart_tool = ChartTool()

    # --------------------------------------------------
    # Main Render
    # --------------------------------------------------

    def render(
        self,
        df: pd.DataFrame,
    ) -> None:

        UIComponents.section(
            "Data Visualization",
            "📈",
        )

        if df is None or df.empty:

            UIComponents.info(
                "Upload a dataset to create visualizations."
            )

            return

        numeric_columns = list(
            df.select_dtypes(include="number").columns
        )

        all_columns = list(df.columns)

        col1, col2 = st.columns(2)

        with col1:

            chart_type = st.selectbox(
                "Chart Type",
                self.SUPPORTED_CHARTS,
            )

        with col2:

            x_column = st.selectbox(
                "X Axis",
                all_columns,
            )

        y_column = None

        if chart_type not in ["Pie"]:

            if numeric_columns:

                y_column = st.selectbox(
                    "Y Axis",
                    numeric_columns,
                )

        st.divider()

        if st.button(
            "Generate Chart",
            use_container_width=True,
            type="primary",
        ):

            with UIComponents.loading(
                "Generating chart..."
            ):

                figure = self._generate_chart(
                    df=df,
                    chart_type=chart_type,
                    x=x_column,
                    y=y_column,
                )

            if figure is not None:

                st.plotly_chart(
                    figure,
                    use_container_width=True,
                )

            else:

                UIComponents.error(
                    "Unable to generate chart."
                )

    # --------------------------------------------------
    # Chart Generation
    # --------------------------------------------------

    def _generate_chart(
        self,
        df: pd.DataFrame,
        chart_type: str,
        x: str,
        y: str | None,
    ):

        chart_map = {

            "Bar": "bar",

            "Line": "line",

            "Pie": "pie",

            "Scatter": "scatter",

            "Histogram": "histogram",

            "Box Plot": "box",

        }

        return self.chart_tool.create_chart(

            df=df,

            chart_type=chart_map[chart_type],

            x=x,

            y=y,

        )
"""
Chart Tool:

This file is Is Act as Interface Between AI Agent and Chat Service

"""

from __future__ import annotations

import pandas as pd
from src.services.chart_service import ChartService

class ChartTool:

    """
    Provides Chart generation capabilities.
    """

    def __init__(self):

        self.chat_service=self.chat_service()


    def create_chart(
            self,
            df:pd.DataFrame,
            x:str | None=None,
            y:str | None=None,
            column: str | None = None
    ):
        """
        Generate chart based on chart type.
        """


        chart_type = chart_type.lower()

        if chart_type=="bar":

            return self.chat_service.bar_chart(
                df,
                x=x,
                y=y
            )

        elif chart_type=="line":

            return self.chat_service.line_chart(
                df,
                x=x,
                y=y
            )

        elif chart_type=="pie":

            return self.chat_service.pie_chart(
                df,
                names=x,
                values=y
            )

        elif chart_type=="scatter":

            return self.chat_service.scatter_chart(
                df,
                x=x,
                y=y
            )

        elif chart_type=="histogram":

            return self.chat_service.histogram(
                df,
                column=column
            )

        elif chart_type=="box":

            return self.chat_service.box_plot(
                df,
                column=column
            )

        else:
             raise ValueError(
                f"Unsupported chart type: {chart_type}"
            )


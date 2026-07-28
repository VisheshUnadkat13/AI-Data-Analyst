"""

Chart Services: 

This File Handles Viszualization and Create a Plot Like Bar chart , Pie chart , Line chart Etc..

using Plotly library
"""


from __future__ import annotations

import pandas as pd
import plotly.express as px

class ChartService:

    """Creats Different Types Of Graph
    """

    @staticmethod
    def bar_chart(
        df:pd.DataFrame,
        x:str,
        y:str,
        title:str|None=None
    ):
        return px.bar(
            df,
            x=x,
            y=y,
            title=title or f"{y} by {x}"
        )

    @staticmethod
    def line_chart(
        df:pd.DataFrame,
        x:str,
        y:str,
        title:str|None=None
    ):
        return px.line(
            df,
            x=x,
            y=y,
            markers=True,
            title=title or f"{y} Trend"
        )

    @staticmethod
    def pie_chart(
        df:pd.DataFrame,
        names:str,
        values:str,
        title:str|None=None
    ):
        return px.pie(
            df,
            names=names,
            values=values,
            title=title or f"{values} Distribution"
        )

    @staticmethod
    def scatter_chart(
        df:pd.DataFrame,
        x:str,
        y:str,
        title:str|None=None
    ):
        return px.scatter(
            df,
            x=x,
            y=y,
            title=title or f"{y} vs {x}"
        )

    @staticmethod
    def histogram(
        df: pd.DataFrame,
        column: str,
        title: str | None = None
    ):

        return px.histogram(
            df,
            x=column,
            title=title or f"{column} Distribution"
        )


    @staticmethod
    def box_plot(
        df: pd.DataFrame,
        column: str,
        title: str | None = None
    ):

        return px.box(
            df,
            y=column,
            title=title or f"{column} Box Plot"
        )
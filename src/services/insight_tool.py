"""
insight_tool.py

Generates business insights from a Pandas DataFrame.

The tool first creates structured statistics using Pandas,
then optionally asks the LLM to explain those statistics.
"""

from __future__ import annotations

from typing import Any
import pandas as pd
from src.llm.groq_client import GroqClient
from src.services.analysis_service import AnalysisService

class InsightTool:
    """
    Generates business insights and executive summaries.
    """

    def __init__(self):

        self.analysis=AnalysisService()
        self.llm=GroqClient()

    # --------------------------------------------------
    # Dataset Summary
    # --------------------------------------------------    

    def dataset_summary(
            self,
            df:pd.DataFrame,
    )->dict[str,Any]:

        """
        Basic dataset Summary
        """
        return self.analysis.summary(df)

    def numeric_statistic(
            self,
            df:pd.DataFrame,
    )->pd.DataFrame:

        return self.analysis.describe(df)

    def missing_values(
            self,
            df:pd.DataFrame,
    )->pd.DataFrame:

        return self.analysis.missing_values(df)

    def duplicate_information(
            self,
            df:pd.DataFrame,
    )->pd.DataFrame:

        return self.analysis.duplicates(df)

    def top_categories(
        self,
        df: pd.DataFrame,
        column: str,
        top_n: int = 5,
    ) -> pd.Series:

        return (
            df[column]
            .value_counts()
            .head(top_n)
        )


    def bottom_categories(
        self,
        df: pd.DataFrame,
        column: str,
        bottom_n: int = 5,
    ) -> pd.Series:

        return (
            df[column]
            .value_counts()
            .tail(bottom_n)
        )

    def correlation_matrix(
            self,
            df:pd.DataFrame,
    )->pd.DataFrame:

        numeric = df.select_dtypes(include="number")

        if numeric.empty:
            return pd.DataFrame()

        return numeric.corr()

    def build_context(
        self,
        df: pd.DataFrame,
    ) -> str:
        """
        Build structured context for the LLM.
        """

        summary = self.dataset_summary(df)

        duplicates = self.duplicate_information(df)

        missing = self.missing_values(df)

        context = f"""
Dataset Summary

Rows: {summary['rows']}

Columns: {summary['columns']}

Numeric Columns: {summary['numeric_columns']}

Categorical Columns: {summary['categorical_columns']}

Memory(MB): {summary['memory_mb']}

Duplicate Rows:

{duplicates}

Missing Values:

{missing.to_string()}
"""

        return context


    def generate_insights(
            self,
            df:pd.DataFrame
    )->str:

        context=self.build_context(df)

        prompt = f"""
You are a Senior Business Data Analyst.

Analyze the dataset summary below.

{context}

Provide:

1. Executive Summary

2. Key Findings

3. Business Risks

4. Opportunities

5. Data Quality Issues

6. Recommendations

Keep the answer concise and practical.
"""

        return self.llm.generate(prompt)


    def executive_summary(
        self,
        df: pd.DataFrame,
    ) -> str:

        context = self.build_context(df)

        prompt = f"""
Create a concise executive summary for this dataset.

{context}

Limit the answer to 6-8 bullet points.
"""

        return self.llm.generate(prompt)   
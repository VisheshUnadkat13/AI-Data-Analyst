"""
analysis_service.py

Provides reusable analytical operations for pandas DataFrames.

This module contains pure business logic and has no dependency on
Streamlit, LLMs, or UI components.
"""

from __future__ import annotations

import pandas as pd


class AnalysisService:
    """Performs common exploratory data analysis."""

    @staticmethod
    def summary(df: pd.DataFrame) -> dict:
        """
        Basic dataset summary.
        """

        memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)

        return {
            "rows": len(df),
            "columns": len(df.columns),
            "memory_mb": round(memory_mb, 2),
            "numeric_columns": len(
                df.select_dtypes(include="number").columns
            ),
            "categorical_columns": len(
                df.select_dtypes(
                    include=["object", "category"]
                ).columns
            ),
        }

    @staticmethod
    def describe(df: pd.DataFrame) -> pd.DataFrame:
        """
        Statistical summary of numeric columns.
        """

        return df.describe().transpose()

    @staticmethod
    def top_rows(
        df: pd.DataFrame,
        rows: int = 5,
    ) -> pd.DataFrame:
        """
        Preview the first rows.
        """

        return df.head(rows)

    @staticmethod
    def missing_values(df: pd.DataFrame) -> pd.DataFrame:
        """
        Missing value report.
        """

        missing = df.isnull().sum()

        percent = (
            missing / len(df) * 100
            if len(df)
            else 0
        )

        return pd.DataFrame(
            {
                "Missing Values": missing,
                "Missing %": percent.round(2),
            }
        )

    @staticmethod
    def duplicates(df: pd.DataFrame) -> dict:
        """
        Duplicate row statistics.
        """

        duplicate_rows = int(df.duplicated().sum())

        return {
            "duplicate_rows": duplicate_rows,
            "duplicate_percentage": round(
                duplicate_rows / len(df) * 100,
                2,
            )
            if len(df)
            else 0,
        }

    @staticmethod
    def column_statistics(df: pd.DataFrame) -> pd.DataFrame:
        """
        Per-column statistics.
        """

        stats = []

        for column in df.columns:

            stats.append(
                {
                    "Column": column,
                    "Data Type": str(df[column].dtype),
                    "Non Null": int(df[column].count()),
                    "Null": int(df[column].isnull().sum()),
                    "Unique": int(df[column].nunique()),
                }
            )

        return pd.DataFrame(stats)

    @staticmethod
    def shape(df: pd.DataFrame) -> tuple[int, int]:
        """
        Dataset shape.
        """

        return df.shape

    @staticmethod
    def columns(df: pd.DataFrame) -> list[str]:
        """
        List all columns.
        """

        return df.columns.tolist()

    @staticmethod
    def data_types(df: pd.DataFrame) -> pd.Series:
        """
        Data types for each column.
        """

        return df.dtypes

    @staticmethod
    def numeric_columns(df: pd.DataFrame) -> list[str]:
        """
        List numeric columns.
        """

        return df.select_dtypes(
            include="number"
        ).columns.tolist()

    @staticmethod
    def categorical_columns(df: pd.DataFrame) -> list[str]:
        """
        List categorical columns.
        """

        return df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()
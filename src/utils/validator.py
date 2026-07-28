"""
validator.py

Utility functions for validating uploaded CSV files and
summarizing DataFrame quality.
"""

from __future__ import annotations

from typing import Any

import pandas as pd


class DataValidator:
    """Performs validation and quality checks on pandas DataFrames."""

    @staticmethod
    def validate_extension(filename: str) -> tuple[bool, str]:
        """
        Validate that the uploaded file has a .csv extension.
        """
        if not filename.lower().endswith(".csv"):
            return False, "Only CSV files are supported."

        return True, "Valid CSV file."

    @staticmethod
    def validate_dataframe(df: pd.DataFrame) -> tuple[bool, list[str]]:
        """
        Validate the DataFrame after it has been loaded.
        Returns:
            (is_valid, list_of_errors)
        """

        errors: list[str] = []

        if df is None:
            errors.append("DataFrame is None.")

        elif df.empty:
            errors.append("CSV contains no rows.")

        if df is not None:

            # Duplicate columns
            duplicate_columns = df.columns[df.columns.duplicated()].tolist()

            if duplicate_columns:
                errors.append(
                    f"Duplicate column names found: {duplicate_columns}"
                )

            # Empty column names
            empty_columns = [
                str(col)
                for col in df.columns
                if str(col).strip() == ""
            ]

            if empty_columns:
                errors.append("One or more columns have empty names.")

        return len(errors) == 0, errors

    @staticmethod
    def dataset_summary(df: pd.DataFrame) -> dict[str, Any]:
        """
        Returns basic dataset information.
        """

        memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)

        return {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "memory_mb": round(memory_mb, 2),
        }

    @staticmethod
    def missing_values(df: pd.DataFrame) -> pd.DataFrame:
        """
        Returns missing value statistics.
        """

        missing = df.isnull().sum()

        percent = (
            (missing / len(df)) * 100
            if len(df) > 0
            else 0
        )

        report = pd.DataFrame(
            {
                "Missing Values": missing,
                "Missing %": percent.round(2),
            }
        )

        return report

    @staticmethod
    def duplicate_rows(df: pd.DataFrame) -> int:
        """
        Returns number of duplicate rows.
        """

        return int(df.duplicated().sum())

    @staticmethod
    def data_types(df: pd.DataFrame) -> pd.DataFrame:
        """
        Returns datatype summary.
        """

        report = pd.DataFrame(
            {
                "Column": df.columns,
                "Data Type": df.dtypes.astype(str).values,
            }
        )

        return report

    @staticmethod
    def numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
        """
        Returns statistics for numeric columns.
        """

        numeric_df = df.select_dtypes(include="number")

        if numeric_df.empty:
            return pd.DataFrame()

        return numeric_df.describe().transpose()

    @staticmethod
    def categorical_summary(df: pd.DataFrame) -> pd.DataFrame:
        """
        Returns summary of categorical columns.
        """

        categorical_df = df.select_dtypes(
            include=["object", "category"]
        )

        if categorical_df.empty:
            return pd.DataFrame()

        report = pd.DataFrame(
            {
                "Unique Values": categorical_df.nunique(),
                "Most Frequent": categorical_df.mode().iloc[0],
            }
        )

        return report

    @staticmethod
    def quality_report(df: pd.DataFrame) -> dict[str, Any]:
        """
        Complete data quality report.
        """

        return {
            "summary": DataValidator.dataset_summary(df),
            "missing_values": DataValidator.missing_values(df),
            "duplicate_rows": DataValidator.duplicate_rows(df),
            "data_types": DataValidator.data_types(df),
            "numeric_summary": DataValidator.numeric_summary(df),
            "categorical_summary": DataValidator.categorical_summary(df),
        }
"""
csv_loader.py

Responsible for:
- Reading uploaded CSV files
- Validating uploaded files
- Returning clean DataFrames with metadata
"""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from typing import BinaryIO

import pandas as pd

from src.utils.validator import DataValidator


# ---------------------------------------------------------
# Data Model
# ---------------------------------------------------------

@dataclass
class LoadedCSV:
    """
    Represents one successfully loaded CSV file.
    """

    file_name: str
    dataframe: pd.DataFrame
    quality_report: dict


# ---------------------------------------------------------
# CSV Loader
# ---------------------------------------------------------

class CSVLoader:

    SUPPORTED_ENCODINGS = [
        "utf-8",
        "utf-8-sig",
        "latin1",
        "cp1252",
    ]

    @staticmethod
    def _read_csv(file: BinaryIO) -> pd.DataFrame:
        """
        Try reading CSV using multiple encodings.
        """

        file_bytes = file.read()

        last_exception = None

        for encoding in CSVLoader.SUPPORTED_ENCODINGS:

            try:

                df = pd.read_csv(
                    BytesIO(file_bytes),
                    encoding=encoding,
                )

                return df

            except Exception as ex:
                last_exception = ex

        raise ValueError(
            f"Unable to read CSV file. {last_exception}"
        )

    @staticmethod
    def load_file(uploaded_file) -> LoadedCSV:
        """
        Load and validate a single uploaded CSV.
        """

        # Validate extension

        valid, message = DataValidator.validate_extension(
            uploaded_file.name
        )

        if not valid:
            raise ValueError(message)

        # Read CSV

        df = CSVLoader._read_csv(uploaded_file)

        # Validate dataframe

        valid, errors = DataValidator.validate_dataframe(df)

        if not valid:
            raise ValueError("\n".join(errors))

        # Build report

        report = DataValidator.quality_report(df)

        return LoadedCSV(
            file_name=uploaded_file.name,
            dataframe=df,
            quality_report=report,
        )

    @staticmethod
    def load_files(uploaded_files) -> list[LoadedCSV]:
        """
        Load multiple uploaded CSV files.
        """

        loaded_files = []

        seen_names = set()

        for uploaded_file in uploaded_files:

            if uploaded_file.name in seen_names:
                raise ValueError(
                    f"Duplicate filename detected: {uploaded_file.name}"
                )

            seen_names.add(uploaded_file.name)

            loaded_files.append(
                CSVLoader.load_file(uploaded_file)
            )

        return loaded_files
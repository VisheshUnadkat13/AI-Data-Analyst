"""
dataframe_manager.py

Central registry for uploaded DataFrames.

Responsibilities:
- Store uploaded DataFrames
- Retrieve DataFrames
- Delete DataFrames
- List datasets
- Provide metadata
"""

from __future__ import annotations

from typing import Dict

import pandas as pd

from src.tools.csv_loader import LoadedCSV


class DataFrameManager:
    """
    Stores and manages uploaded DataFrames.
    """

    def __init__(self) -> None:
        self._datasets: Dict[str, LoadedCSV] = {}

    # --------------------------------------------------
    # CRUD Operations
    # --------------------------------------------------

    def add_dataset(self, dataset: LoadedCSV) -> None:
        """
        Add a dataset to the manager.

        Dataset key is derived from filename.

        Example:
            sales.csv -> sales
        """

        key = dataset.file_name.rsplit(".", 1)[0]

        self._datasets[key] = dataset

    def get_dataset(self, name: str) -> LoadedCSV:
        """
        Retrieve a dataset.

        Raises:
            KeyError if dataset is not found.
        """

        if name not in self._datasets:
            raise KeyError(f"Dataset '{name}' does not exist.")

        return self._datasets[name]

    def get_dataframe(self, name: str) -> pd.DataFrame:
        """
        Return only the DataFrame.
        """

        return self.get_dataset(name).dataframe

    def remove_dataset(self, name: str) -> None:
        """
        Remove a dataset.
        """

        if name in self._datasets:
            del self._datasets[name]

    def clear(self) -> None:
        """
        Remove all datasets.
        """

        self._datasets.clear()

    # --------------------------------------------------
    # Information
    # --------------------------------------------------

    def exists(self, name: str) -> bool:
        """
        Check whether a dataset exists.
        """

        return name in self._datasets

    def list_datasets(self) -> list[str]:
        """
        Return all dataset names.
        """

        return list(self._datasets.keys())

    def count(self) -> int:
        """
        Number of uploaded datasets.
        """

        return len(self._datasets)

    def is_empty(self) -> bool:
        """
        True if no datasets exist.
        """

        return len(self._datasets) == 0

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    def get_metadata(self) -> list[dict]:
        """
        Return metadata for every uploaded dataset.
        """

        metadata = []

        for name, dataset in self._datasets.items():

            summary = dataset.quality_report["summary"]

            metadata.append(
                {
                    "dataset": name,
                    "rows": summary["rows"],
                    "columns": summary["columns"],
                    "memory_mb": summary["memory_mb"],
                }
            )

        return metadata

    # --------------------------------------------------
    # Utility
    # --------------------------------------------------

    def __len__(self) -> int:
        return self.count()

    def __contains__(self, item: str) -> bool:
        return self.exists(item)

    def __repr__(self) -> str:
        return (
            f"DataFrameManager("
            f"datasets={self.list_datasets()})"
        )
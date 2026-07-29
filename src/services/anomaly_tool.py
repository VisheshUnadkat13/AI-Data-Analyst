"""
anomaly_tool.py

Detects anomalies using multiple statistical techniques and
generates business-friendly explanations using an LLM.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from src.llm.groq_client import GroqClient


class AnomalyTool:
    """
    Detect anomalies in datasets.
    """

    def __init__(self):

        self.llm = GroqClient()

    # --------------------------------------------------
    # Numeric Columns
    # --------------------------------------------------

    @staticmethod
    def numeric_columns(
        df: pd.DataFrame,
    ) -> list[str]:

        return df.select_dtypes(
            include=np.number
        ).columns.tolist()

    # --------------------------------------------------
    # Z Score
    # --------------------------------------------------

    def zscore_detection(
        self,
        df: pd.DataFrame,
        column: str,
        threshold: float = 3.0,
    ) -> pd.DataFrame:
        """
        Detect anomalies using Z-score.
        """

        if column not in df.columns:
            raise ValueError(f"{column} not found.")

        series = df[column].dropna()

        std = series.std()

        if std == 0:
            return pd.DataFrame()

        mean = series.mean()

        z_scores = ((series - mean) / std).abs()

        anomalies = df.loc[
            z_scores > threshold
        ].copy()

        anomalies["anomaly_score"] = z_scores[
            z_scores > threshold
        ]

        anomalies["method"] = "Z-Score"

        return anomalies

    # --------------------------------------------------
    # IQR
    # --------------------------------------------------

    def iqr_detection(
        self,
        df: pd.DataFrame,
        column: str,
    ) -> pd.DataFrame:
        """
        Detect anomalies using IQR.
        """

        q1 = df[column].quantile(0.25)

        q3 = df[column].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr

        upper = q3 + 1.5 * iqr

        anomalies = df[
            (df[column] < lower)
            | (df[column] > upper)
        ].copy()

        anomalies["method"] = "IQR"

        return anomalies

    # --------------------------------------------------
    # Isolation Forest
    # --------------------------------------------------

    def isolation_forest(
        self,
        df: pd.DataFrame,
        contamination: float = 0.02,
    ) -> pd.DataFrame:
        """
        Detect anomalies using Isolation Forest.
        """

        numeric = df.select_dtypes(
            include=np.number
        )

        if numeric.empty:
            return pd.DataFrame()

        clean = numeric.fillna(
            numeric.median()
        )

        model = IsolationForest(
            contamination=contamination,
            random_state=42,
        )

        predictions = model.fit_predict(clean)

        scores = model.decision_function(clean)

        result = df.copy()

        result["prediction"] = predictions

        result["anomaly_score"] = scores

        result = result[
            result["prediction"] == -1
        ].copy()

        result["method"] = "Isolation Forest"

        return result

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def summary(
        self,
        anomalies: pd.DataFrame,
    ) -> dict[str, Any]:

        return {
            "total_anomalies": len(anomalies),
            "columns": anomalies.columns.tolist(),
        }

    # --------------------------------------------------
    # Explain
    # --------------------------------------------------

    def explain(
        self,
        anomalies: pd.DataFrame,
    ) -> str:
        """
        Generate business explanation.
        """

        if anomalies.empty:

            return "No anomalies detected."

        preview = anomalies.head(10).to_string()

        prompt = f"""
You are a Senior Data Analyst.

The following rows were detected as anomalies.

{preview}

Explain:

1. Why they might be anomalous.

2. Possible business reasons.

3. Potential risks.

4. Suggested next steps.

Keep the explanation concise.
"""

        return self.llm.generate(prompt)

    # --------------------------------------------------
    # Full Report
    # --------------------------------------------------

    def detect(
        self,
        df: pd.DataFrame,
        method: str = "isolation_forest",
        column: str | None = None,
    ) -> dict[str, Any]:
        """
        Main entry point for anomaly detection.
        """

        method = method.lower()

        if method == "zscore":

            if column is None:
                raise ValueError(
                    "Column required for Z-Score."
                )

            anomalies = self.zscore_detection(
                df,
                column,
            )

        elif method == "iqr":

            if column is None:
                raise ValueError(
                    "Column required for IQR."
                )

            anomalies = self.iqr_detection(
                df,
                column,
            )

        elif method in (
            "isolation",
            "isolation_forest",
        ):

            anomalies = self.isolation_forest(df)

        else:

            raise ValueError(
                "Unsupported detection method."
            )

        return {
            "summary": self.summary(anomalies),
            "anomalies": anomalies,
            "explanation": self.explain(anomalies),
        }
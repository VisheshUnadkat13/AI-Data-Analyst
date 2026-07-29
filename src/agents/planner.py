# """
# planner.py

# this is Responsible for understanding the use intent
# and deciding which tool shoul be used.

# """

# from __future__ import annotations

# import json
# from src.llm.groq_client import GroqClient
# from src.llm.prompts import DATA_ANALYST_SYSTEM_PROMPT

# class PlannerAgent:

#     """
#     Decide The next action for use queries.
#     """

#     def __init__(self):

#         self.llm=GroqClient()

#     def plan(
#             self,
#             question:str,
#             dataset_info: str
#     )->str:
#         """
#         create execution plan.
#         """    

#         prompt = f"""

# {DATA_ANALYST_SYSTEM_PROMPT}


# You are a planning agent.

# Dataset information:

# {dataset_info}


# User question:

# {question}


# Choose one action:

# - analysis
# - chart
# - summary
# - anomaly
# - sql


# Return only JSON.

# Example:

# {{
# "action":"analysis"
# }}

# """
#         response=self.llm.generate(prompt)

#         try:

#             return json.loads(response)
        
#         except Exception:
#             return {
#                 "action":"analysis"
#             }



"""
planner.py

Responsible for understanding the user intent
and deciding which tool should be used.
"""

from __future__ import annotations

import json

from src.llm.groq_client import GroqClient
from src.llm.prompts import DATA_ANALYST_SYSTEM_PROMPT


class PlannerAgent:
    """
    Decide the next action for user queries.
    """

    def __init__(self):
        self.llm = GroqClient()

    def plan(
        self,
        question: str,
        dataset_info: str,
    ) -> dict:
        """
        Create an execution plan from the user's question.
        """

        prompt = f"""
{DATA_ANALYST_SYSTEM_PROMPT}

You are an AI Planning Agent.

Your job is ONLY to decide what action should be performed.

Dataset Information:
{dataset_info}

User Question:
{question}

Available actions:

1. analysis
2. summary
3. chart
4. sql
5. anomaly
6. insight

Rules:

- Return ONLY valid JSON.
- Do not explain anything.
- If action is "chart", also return:
    - chart_type
    - x
    - y

- If action is "sql", also return:
    - sql

Examples:

Summary

{{
    "action":"summary"
}}

Analysis

{{
    "action":"analysis"
}}

Chart

{{
    "action":"chart",
    "chart_type":"bar",
    "x":"Region",
    "y":"Revenue"
}}

SQL

{{
    "action":"sql",
    "sql":"SELECT Region, SUM(Revenue) FROM sales GROUP BY Region"
}}

Insight

{{
    "action":"insight"
}}

Anomaly

{{
    "action":"anomaly"
}}
"""

        response = self.llm.generate(prompt)

        try:
            return json.loads(response)

        except Exception:

            return {
                "action": "analysis"
            }
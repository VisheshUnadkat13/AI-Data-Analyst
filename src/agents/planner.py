"""
planner.py

this is Responsible for understanding the use intent
and deciding which tool shoul be used.

"""

from __future__ import annotations

import json
from src.llm.groq_client import GroqClient
from src.llm.prompts import DATA_ANALYST_SYSTEM_PROMPT

class PlannerAgent:

    """
    Decide The next action for use queries.
    """

    def __init__(self):

        self.llm=GroqClient()

    def plan(
            self,
            question:str,
            dataset_info: str
    )->str:
        """
        create execution plan.
        """    

        prompt = f"""

{DATA_ANALYST_SYSTEM_PROMPT}


You are a planning agent.

Dataset information:

{dataset_info}


User question:

{question}


Choose one action:

- analysis
- chart
- summary
- anomaly
- sql


Return only JSON.

Example:

{{
"action":"analysis"
}}

"""
        response=self.llm.generate(prompt)

        try:

            return json.loads(response)
        
        except Exception:
            return {
                "action":"analysis"
            }
                
            
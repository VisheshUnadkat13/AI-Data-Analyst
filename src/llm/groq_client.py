"""
groq_client:

this file is central LLM Client responsible for communicating with GROQ API
"""

from __future__ import annotations

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class GroqClient:

    """
    Wrapper Around GROQ LLM 
    """

    def __init__(
            self,
            model:str = "llama-3.3-70b-versatile",
            temperature: float = 0.1
    ):
        api_key=os.getenv(
            "GROQ_API_KEY"
        )

        if not api_key:
            raise ValueError(
                "GROQ API KEY is missing in environment variables"
            )

        self.llm=ChatGroq(
            model=model,
            temperature=temperature,
            api_key=api_key
        )


    def generate(
            self,
            prompt:str
    )->str:
        
        """
        Generate text response.
        """

        response=self.llm.invoke(
            prompt
        )

        return response.content

    def chat(
            self,
            messages:list
    )->str:
        
        """
        Chat Style Intrection.
        """
        response=self.llm.invoke(
            messages
        )

        return response.content


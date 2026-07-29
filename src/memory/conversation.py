"""
conversation.py

Stores conversation state for the current session.

This module is intentionally independent from
Streamlit so it can later be replaced with
Redis, PostgreSQL, MongoDB, etc.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Message:
    """
    Represents one conversation message.
    """

    role: str
    content: str


@dataclass
class ConversationState:
    """
    Stores the current conversation context.
    """

    active_dataset: str | None = None

    previous_question: str | None = None

    previous_answer: Any = None

    previous_plan: dict | None = None

    current_chart: str | None = None

    filters: dict = field(default_factory=dict)

    messages: list[Message] = field(default_factory=list)


class ConversationMemory:
    """
    Maintains the conversation state.
    """

    def __init__(self):

        self.state = ConversationState()

    # --------------------------------------------------
    # Messages
    # --------------------------------------------------

    def add_user_message(self, question: str):

        self.state.messages.append(
            Message(
                role="user",
                content=question
            )
        )

        self.state.previous_question = question

    def add_assistant_message(self, answer: str):

        self.state.messages.append(
            Message(
                role="assistant",
                content=answer
            )
        )

        self.state.previous_answer = answer

    # --------------------------------------------------
    # Dataset
    # --------------------------------------------------

    def set_active_dataset(
        self,
        dataset: str
    ):

        self.state.active_dataset = dataset

    def get_active_dataset(self):

        return self.state.active_dataset

    # --------------------------------------------------
    # Planner
    # --------------------------------------------------

    def save_plan(
        self,
        plan: dict
    ):

        self.state.previous_plan = plan

    def get_plan(self):

        return self.state.previous_plan

    # --------------------------------------------------
    # Filters
    # --------------------------------------------------

    def update_filters(
        self,
        filters: dict
    ):

        self.state.filters.update(filters)

    def get_filters(self):

        return self.state.filters

    def clear_filters(self):

        self.state.filters.clear()

    # --------------------------------------------------
    # Chart
    # --------------------------------------------------

    def set_chart(
        self,
        chart: str
    ):

        self.state.current_chart = chart

    def get_chart(self):

        return self.state.current_chart

    # --------------------------------------------------
    # History
    # --------------------------------------------------

    def history(self):

        return self.state.messages

    def last_question(self):

        return self.state.previous_question

    def last_answer(self):

        return self.state.previous_answer

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    def clear(self):

        self.state = ConversationState()

    # --------------------------------------------------
    # Context
    # --------------------------------------------------

    def build_context(self) -> str:
        """
        Build conversation history for LLM prompts.
        """

        history = []

        for message in self.state.messages:

            history.append(
                f"{message.role.upper()}: {message.content}"
            )

        return "\n".join(history)
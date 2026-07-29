"""
chat.py

Chat interface for AI Data Analyst.

Responsible for:

- Displaying chat history
- Accepting user questions
- Calling PlannerAgent
- Calling AnalystAgent
- Updating ConversationMemory
"""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

from src.agents.planner import PlannerAgent
from src.agents.analyst import AnalystAgent
from src.memory.conversation import ConversationMemory

from ui.components import UIComponents


class ChatUI:
    """
    AI Chat Interface.
    """

    def __init__(self):

        self.planner = PlannerAgent()

        self.analyst = AnalystAgent()

        self.memory = ConversationMemory()

    # ----------------------------------------------------------
    # Main Render
    # ----------------------------------------------------------

    def render(
        self,
        df: pd.DataFrame,
        dataset_name: str,
    ) -> None:

        UIComponents.section(
            "AI Data Chat",
            "🤖"
        )

        if df is None or df.empty:

            UIComponents.info(
                "Upload a dataset to start chatting."
            )

            return

        self.memory.set_active_dataset(
            dataset_name
        )

        self._render_history()

        question = st.chat_input(
            "Ask anything about your data..."
        )

        if question:

            self._handle_question(
                question,
                df,
            )

    # ----------------------------------------------------------
    # Render History
    # ----------------------------------------------------------

    def _render_history(self):

        history = self.memory.history()

        for message in history:

            with st.chat_message(
                message.role
            ):

                if isinstance(
                    message.content,
                    str,
                ):

                    st.markdown(
                        message.content
                    )

                else:

                    st.write(
                        message.content
                    )

    # ----------------------------------------------------------
    # Handle Question
    # ----------------------------------------------------------

    def _handle_question(
        self,
        question: str,
        df: pd.DataFrame,
    ):

        self.memory.add_user_message(
            question
        )

        with st.chat_message("user"):

            st.markdown(question)

        dataset_info = self._dataset_info(df)

        with st.spinner(
            "Thinking..."
        ):

            plan = self.planner.plan(
                question=question,
                dataset_info=dataset_info,
            )

            self.memory.save_plan(
                plan
            )

            response = self.analyst.execute(
                plan=plan,
                df=df,
            )

        with st.chat_message(
            "assistant"
        ):

            self._render_response(
                response
            )

        self.memory.add_assistant_message(
            str(response)
        )

    # ----------------------------------------------------------
    # Dataset Summary
    # ----------------------------------------------------------

    def _dataset_info(
        self,
        df: pd.DataFrame,
    ) -> str:

        return f"""
Rows: {len(df)}

Columns: {len(df.columns)}

Column Names:

{", ".join(df.columns)}
"""

    # ----------------------------------------------------------
    # Response Renderer
    # ----------------------------------------------------------

    def _render_response(
        self,
        response: Any,
    ):

        if response is None:

            UIComponents.warning(
                "No response generated."
            )

            return

        if isinstance(
            response,
            pd.DataFrame,
        ):

            UIComponents.dataframe(
                response
            )

            return

        if isinstance(
            response,
            dict,
        ):

            for key, value in response.items():

                st.subheader(
                    key.replace(
                        "_",
                        " "
                    ).title()
                )

                if isinstance(
                    value,
                    pd.DataFrame,
                ):

                    UIComponents.dataframe(
                        value
                    )

                elif isinstance(
                    value,
                    dict,
                ):

                    UIComponents.json(
                        value
                    )

                else:

                    st.write(
                        value
                    )

            return

        if hasattr(
            response,
            "to_dict"
        ):

            UIComponents.dataframe(
                response
            )

            return

        if hasattr(
            response,
            "data"
        ):

            st.plotly_chart(
                response,
                use_container_width=True,
            )

            return

        st.write(
            response
        )
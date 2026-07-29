from ui.sidebar import Sidebar
from src.services.dataframe_manager import DataFrameManager
sidebar_state = Sidebar.render(
    dataframe_manager = DataFrameManager()

)

uploaded_files = sidebar_state["uploaded_files"]

selected_dataset = sidebar_state["active_dataset"]

clear_session = sidebar_state["clear_session"]
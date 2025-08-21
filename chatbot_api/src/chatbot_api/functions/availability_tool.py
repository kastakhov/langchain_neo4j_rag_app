from __future__ import annotations
from typing import (
    Optional,
    Type
)

from pydantic import BaseModel

from langchain_core.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool

from chatbot_api.tools.wait_times import WaitTime
from chatbot_api.utils.files import get_template_from_file
from chatbot_api.utils.neo4j_graph import GraphConnector


class AvailabilityToolInput(BaseModel):
    """
    Without this class, the following error occurs:
    TypeError: Object of type CallbackManagerForToolRun is not JSON serializable
    """
    pass

class AvailabilityTool(BaseTool):
    name: str = "availability_tool"
    description: str = get_template_from_file(f"tools_description/{name}.txt")
    args_schema: Type[AvailabilityToolInput] = AvailabilityToolInput
    neo4j_connector: GraphConnector

    def get_most_available_hospital(self) -> dict[str, float]:
        """
        Initialize the wait time tool.
        """
        wait_time = WaitTime(self.neo4j_connector)
        return wait_time.get_most_available_hospital()

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """
        Use the tool.
        """
        return self.get_most_available_hospital()

    async def _arun(
        self,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """
        Use the tool asynchronously.
        """
        return self.get_most_available_hospital()

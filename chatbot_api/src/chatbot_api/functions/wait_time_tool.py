from __future__ import annotations
from typing import Optional, Type

from pydantic import BaseModel, Field

from langchain_core.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool

from chatbot_api.tools.wait_times import WaitTime
from chatbot_api.utils.files import get_template_from_file
from chatbot_api.utils.neo4j_graph import GraphConnector

class WaitTimeToolInput(BaseModel):
    input: str = Field(
        title="Hospital Name",
        description="The name of the hospital. Without article and another words.",
    )


class WaitTimeTool(BaseTool):
    name: str = "wait_time_tool"
    description: str = get_template_from_file(f"tools_description/{name}.txt")
    args_schema: Type[WaitTimeToolInput] = WaitTimeToolInput
    neo4j_connector: GraphConnector

    def get_current_wait_times(self, input) -> str:
        """
        Initialize the wait time tool.
        """
        wait_time = WaitTime(
            neo4j_connector = self.neo4j_connector
        )
        return wait_time.get_current_wait_times(input)

    def _run(
        self,
        input: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """
        Use the tool.
        """
        return self.get_current_wait_times(input)

    async def _arun(
        self,
        input: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """
        Use the tool asynchronously.
        """
        return self.get_current_wait_times(input)

from __future__ import annotations
from typing import (
    Dict,
    List
)

from langchain.agents import (
    create_tool_calling_agent,
    AgentExecutor
)

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

from langchain_core.tools import BaseTool
from langchain_core.runnables import Runnable
from langchain.callbacks.base import BaseCallbackHandler

from langfuse.client import StatefulTraceClient

from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from chatbot_api.llm_models.agent_executor_model import AgentExecutorModel

from chatbot_api.functions.objective_tool import ObjectiveTool
from chatbot_api.functions.semantic_tool import SemanticTool
from chatbot_api.functions.wait_time_tool import WaitTimeTool
from chatbot_api.functions.availability_tool import AvailabilityTool

from chatbot_api.utils.configuration import Configuration
from chatbot_api.utils.files import get_template_from_file
from chatbot_api.utils.neo4j_graph import GraphConnector
from chatbot_api.utils.callbacks import AppCallbacks


class RagAgent:
    tools: list[BaseTool]
    chat_model: ChatOpenAI | ChatOllama
    agent: Runnable | None = None
    agent_executor: AgentExecutor | None = None
    callbacks: List[BaseCallbackHandler] | None = None
    langfuse_trace: StatefulTraceClient | None = None
    prompt: ChatPromptTemplate | None = None

    def __init__(self, callbacks_config: Dict[str, Dict[str, str]] | dict = {}) -> None:
        app_config = Configuration()
        neo4j_connector = GraphConnector(app_config)

        print ("Initializing Callbacks...")
        self.__get_callbacks(callbacks_config)

        print("Initializing tools...")
        self.__get_tools(app_config, neo4j_connector)

        print("Initializing chat model...")
        self.chat_model = AgentExecutorModel(app_config).get_agent_model(
            temperature = app_config.agent_executor['models']['agent']['temperature']
        )

        self.__get_prompt()

        self.__get_calling_agent()

    def invoke_sync_agent(self, query: str):
        """
        Sync invoke the agent.
        """
        return self.agent_executor.invoke({"input": query})

    async def invoke_async_agent(self, query: str):
        """
        Async invoke the agent.
        """
        return await self.agent_executor.ainvoke({"input": query})

    def create_rag_agent_executor(self) -> None:
        """
        Create the agent executor.
        """
        self.agent_executor = AgentExecutor(
            agent = self.agent,
            tools = self.tools,
            return_intermediate_steps = True,
            callbacks = self.callbacks,
            handle_parsing_errors = True,
        )

    def __get_callbacks(self, callbacks_config) -> None:
        """
        Get the callbacks for the agent.
        """
        callbacks = []
        app_callbacks = AppCallbacks()
        self.langfuse_trace = app_callbacks.get_lanfuse_trace(callbacks_config.get('langfuse', {}))
        if self.langfuse_trace:
            handler = self.langfuse_trace.get_langchain_handler()
            callbacks.append(handler)
        
        if callbacks: 
            self.callbacks = callbacks

    def __get_prompt(self) -> None:
        """
        Create a system prompt for the agent.
        """
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", get_template_from_file('agent_prompts/agent_system_prompt.txt')),
                MessagesPlaceholder("chat_history", optional=True),
                ("human", "{input}"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )

    def __get_calling_agent(self) -> None:
        """
        Get the tool calling agent for the agent executor.
        """
        self.agent = create_tool_calling_agent(
            llm = self.chat_model,
            tools = self.tools,
            prompt = self.prompt,
        )

    def __get_tools(self, app_config: Configuration, neo4j_connector: GraphConnector) -> None:
        """
        Get the tools for the agent.
        """
        self.tools = [
            ObjectiveTool(
                app_config = app_config,
                neo4j_connector = neo4j_connector,
                langfuse_trace = self.langfuse_trace
            ),
            SemanticTool(
                app_config = app_config,
                langfuse_trace = self.langfuse_trace
            ),
            WaitTimeTool(
                neo4j_connector = neo4j_connector
            ),
            AvailabilityTool(
                neo4j_connector = neo4j_connector
            ),
        ]

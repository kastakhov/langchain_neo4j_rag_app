from __future__ import annotations
from typing import Optional, Type

from pydantic import BaseModel, Field

from langchain_neo4j import GraphCypherQAChain

from langchain_core.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.prompts import (
    FewShotPromptTemplate,
    PromptTemplate
)

from langfuse.client import StatefulTraceClient

from chatbot_api.data.objective_prompts.cypher_query_examples import (
    examples as cypher_examples,
    examples_prompt as cypher_examples_prompt
)
from chatbot_api.utils.configuration import Configuration
from chatbot_api.utils.neo4j_graph import GraphConnector
from chatbot_api.utils.files import get_template_from_file
from chatbot_api.llm_models.objective_tool_model import ObjectiveToolModel

class ObjectiveToolInput(BaseModel):
    input: str = Field(
        title="Human Question",
        description="The entire human question.",
    )


class ObjectiveTool(BaseTool):
    name: str = "objective_tool"
    args_schema: Type[ObjectiveToolInput] = ObjectiveToolInput
    description: str = get_template_from_file(f"tools_description/{name}.txt")
    cypher_template_prefix: str = get_template_from_file('objective_prompts/cypher_query_prefix_template.txt')
    cypher_template_suffix: str = get_template_from_file('objective_prompts/cypher_query_suffix_template.txt')
    qa_prompt_template: str = get_template_from_file('objective_prompts/qa_prompt_template.txt')
    app_config: Configuration
    neo4j_connector: GraphConnector
    langfuse_trace: None | StatefulTraceClient


    def qa_prompt(self) -> Type[PromptTemplate]:
        """
        Create a prompt template for the QA generation.
        """
        return PromptTemplate(
            input_variables = ["context", "question"],
            template = self.qa_prompt_template,
            validate_template = True
        )

    def cypher_prompt(self) -> Type[FewShotPromptTemplate]:
        """
        Create a prompt template for the Cypher query.
        """
        return FewShotPromptTemplate(
            examples = cypher_examples,
            example_prompt = PromptTemplate.from_template(cypher_examples_prompt),
            input_variables = ["schema", "question"],
            prefix = self.cypher_template_prefix,
            suffix = self.cypher_template_suffix,
            validate_template = True
        )

    def hospital_cypher_chain(self) -> GraphCypherQAChain:
        """
        Create a chain for the hospital.
        """
        self.neo4j_connector.refresh_schema()
        return GraphCypherQAChain.from_llm(
            cypher_llm = ObjectiveToolModel(self.app_config).get_cypher_model(
                temperature = self.app_config.objective_tool['models']['cypher']['temperature']
            ),
            qa_llm = ObjectiveToolModel(self.app_config).get_chat_model(
                temperature = self.app_config.objective_tool['models']['qa']['temperature']
            ),
            graph = self.neo4j_connector.get_neo4jgraph(),
            qa_prompt = self.qa_prompt(),
            cypher_prompt = self.cypher_prompt(),
            validate_cypher = True,
            top_k = self.app_config.objective_tool['top_k'],
            allow_dangerous_requests = True,
        )

    def __get_config(self) -> None:
        """
        Get the config.
        """
        config = {}
        callbacks = []
        if self.langfuse_trace is not None:
            span = self.langfuse_trace.span()
            handler = span.get_langchain_handler()
            callbacks.append(handler)
        if callbacks:
            config['callbacks'] = callbacks
        return config

    def _run(
        self,
        input: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """
        Use the tool.
        """
        return self.hospital_cypher_chain().invoke(
            {"query": input},
            config = self.__get_config()
        )

    async def _arun(
        self,
        input: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """
        Use the tool asynchronously.
        """
        return self.hospital_cypher_chain().invoke(
            {"query": input},
            config = self.__get_config()
        )

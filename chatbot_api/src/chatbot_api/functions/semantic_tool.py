from __future__ import annotations
from typing import Optional, Type

from pydantic import BaseModel, Field

from langchain.chains import RetrievalQA

from langchain_core.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_core.tools import BaseTool

from langchain_community.vectorstores.neo4j_vector import Neo4jVector

from langfuse.client import StatefulTraceClient

from chatbot_api.utils.configuration import Configuration
from chatbot_api.utils.files import get_template_from_file
from chatbot_api.llm_models.semantit_tool_model import SemantitToolModel

class SemanticToolInput(BaseModel):
    input: str = Field(
        title="Human Question",
        description="The entire human question.",
    )


class SemanticTool(BaseTool):
    name: str = "semantic_tool"
    args_schema: Type[SemanticToolInput] = SemanticToolInput
    description: str = get_template_from_file(f"tools_description/{name}.txt")
    system_prompt_template: str = get_template_from_file('semantic_prompts/system_prompt_template.txt')
    app_config: Configuration
    langfuse_trace: None | StatefulTraceClient

    def review_system_prompt(self) -> Type[SystemMessagePromptTemplate]:
        """
        Create a prompt template for the system message.
        """
        return SystemMessagePromptTemplate(
            prompt = PromptTemplate(
                input_variables = ["context"],
                template = self.system_prompt_template
            )
        )

    def review_human_prompt(self) -> Type[HumanMessagePromptTemplate]:
        """
        Create a prompt template for the human message.
        """
        return HumanMessagePromptTemplate(
            prompt = PromptTemplate(
                input_variables = ["question"],
                template = "{question}")
        )


    def review_prompt(self, messages: list) -> Type[ChatPromptTemplate]:
        """
        Create a prompt template for the chat.
        """

        return ChatPromptTemplate(
            input_variables = ["context", "question"],
            messages = messages
        )

    def neo4j_vector_index(self) -> Neo4jVector:
        """
        Create a Neo4jVector object.
        """
        return  Neo4jVector.from_existing_graph(
            embedding = SemantitToolModel(self.app_config).get_embeddings_model(),
            url = self.app_config.neo4j_config['uri'],
            username = self.app_config.neo4j_config['username'],
            password = self.app_config.neo4j_config['password'],
            index_name = "reviews",
            node_label = "Review",
            text_node_properties = [
                "physician_name",
                "patient_name",
                "text",
                "hospital_name",
            ],
            distance_strategy = self.app_config.semantic_tool['distance_strategy'],
            pre_delete_collection = self.app_config.semantic_tool['pre_delete_collection'],
            embedding_node_property = "embedding",
        )

    def reviews_vector_chain(self) -> RetrievalQA:
        """
        Create a chain for the reviews.
        """
        reviews_vector_chain = RetrievalQA.from_chain_type(
            llm = SemantitToolModel(self.app_config).get_chat_model(
                temperature = self.app_config.semantic_tool['models']['qa']['temperature']
            ),
            chain_type = "stuff",
            retriever = self.neo4j_vector_index().as_retriever(
                search_kwargs = {
                    'k': self.app_config.semantic_tool['k_doc'],
                    'fetch_k': self.app_config.semantic_tool['fetch_k'],
                }
            ),
        )

        messages = [
            self.review_system_prompt(), 
            self.review_human_prompt()
        ]

        reviews_vector_chain.combine_documents_chain.llm_chain.prompt = self.review_prompt(messages)
        return reviews_vector_chain

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
        return self.reviews_vector_chain().invoke(
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
        return self.reviews_vector_chain().invoke(
            {"query": input},
            config = self.__get_config()
        )

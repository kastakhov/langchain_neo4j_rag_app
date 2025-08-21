from pydantic import BaseModel
from typing import Set
from chatbot_api.structures.tools.agent_executor_model import AgentExecutorConfModel
from chatbot_api.structures.tools.objective_tool_model import ObjectiveToolConfModel
from chatbot_api.structures.tools.semantic_tool_model import SemanticToolConfModel
from chatbot_api.structures.langchain_model import LangchainConfModel
from chatbot_api.structures.langfuse_model import LangfuseConfModel
from chatbot_api.structures.neo4j_model import Neo4jConfModel


class CoreConfigModel(BaseModel):
    ae: AgentExecutorConfModel = AgentExecutorConfModel()
    ot: ObjectiveToolConfModel = ObjectiveToolConfModel()
    st: SemanticToolConfModel = SemanticToolConfModel()
    langchain: LangchainConfModel = LangchainConfModel()
    langfuse: LangfuseConfModel = LangfuseConfModel()
    neo4j: Neo4jConfModel = Neo4jConfModel()

    @classmethod
    def sensetive_keys(cls) -> Set[str]:
        return {
        'api_uri',
        'api_key',
        'neo4j',
        'langfuse'
    }
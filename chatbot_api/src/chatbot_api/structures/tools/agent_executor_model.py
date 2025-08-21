from pydantic import BaseModel
from typing import Dict
from chatbot_api.structures.models.chat_model import ChatModelConf

class AgentExecutorConfModel(BaseModel):
    models: Dict[str, ChatModelConf] = {
        'agent': ChatModelConf()
    }
    invoke_max_retries: int = 5
    invoke_retry_delay: int = 1

from pydantic import BaseModel
from typing import Dict
from chatbot_api.structures.models.chat_model import ChatModelConf


class ObjectiveToolConfModel(BaseModel):
    models: Dict[str, ChatModelConf ] = {
        'cypher': ChatModelConf(),
        'qa': ChatModelConf()
    }
    top_k: int = 5

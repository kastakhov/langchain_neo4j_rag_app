from pydantic import BaseModel
from typing import Dict
from chatbot_api.structures.models.embedding_model import EmbeddingModelConf
from chatbot_api.structures.models.chat_model import ChatModelConf


class SemanticToolConfModel(BaseModel):
    models: Dict[str, ChatModelConf | EmbeddingModelConf] = {
        'qa': ChatModelConf(),
        'embedding': EmbeddingModelConf()
    }
    k_doc: int = 12
    fetch_k: int = 20
    distance_strategy: str = 'COSINE'
    pre_delete_collection: bool = False

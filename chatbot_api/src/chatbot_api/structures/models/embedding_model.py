from pydantic import BaseModel


class EmbeddingModelConf(BaseModel):
    api_uri: str = ''
    api_key: str = ''
    name: str = ''
    engine: str = ''

from pydantic import BaseModel


class ChatModelConf(BaseModel):
    api_uri: str = ''
    api_key: str = ''
    name: str = ''
    engine: str = ''
    temperature: int | float = 0

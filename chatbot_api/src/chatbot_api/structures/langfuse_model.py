from pydantic import BaseModel


class LangfuseConfModel(BaseModel):
    uri: str = ''
    secret_key: str = ''
    public_key: str = ''

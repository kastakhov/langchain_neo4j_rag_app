from pydantic import BaseModel


class Neo4jConfModel(BaseModel):
    uri: str = ''
    username: str = ''
    password: str = ''

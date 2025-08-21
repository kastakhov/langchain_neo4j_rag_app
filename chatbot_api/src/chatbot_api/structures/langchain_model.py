from pydantic import BaseModel


class LangchainConfModel(BaseModel):
    debug: bool = False
    verbose: bool = False

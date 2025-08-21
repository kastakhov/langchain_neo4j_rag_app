from __future__ import annotations
from chatbot_api.structures.singleton import SingletonMeta
from chatbot_api.utils.configuration import Configuration

from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

class ObjectiveToolModel(metaclass = SingletonMeta):
    """
    This class is responsible for initialize the models based on the configuration
    """
    def __init__(self, conf: Configuration) -> None:
        self.app_conf = conf

    def get_chat_model(self, *args, **kwargs) -> ChatOllama | ChatOpenAI:
        engine = self.app_conf.model_engine('ot', 'qa')
        model = self.app_conf.model_name('ot', 'qa')
        api_uri = self.app_conf.model_api_uri('ot', 'qa')
        api_key = self.app_conf.model_api_key('ot', 'qa')
        if engine == "ollama":
            return ChatOllama(
                model = model,
                base_url = api_uri,
                *args,
                **kwargs
            )
        elif engine == "openai":
            return ChatOpenAI(
                model = model,
                openai_api_base = api_uri,
                openai_api_key = api_key,
                *args,
                **kwargs
            )
        else:
            raise ValueError(
                f"Invalid model engine: {engine}"
            )
        
    def get_cypher_model(self, *args, **kwargs) -> ChatOllama | ChatOpenAI:
        engine = self.app_conf.model_engine('ot', 'cypher')
        model = self.app_conf.model_name('ot', 'cypher')
        api_uri = self.app_conf.model_api_uri('ot', 'cypher')
        api_key = self.app_conf.model_api_key('ot', 'cypher')
        if engine == "ollama":
            return ChatOllama(
                model = model,
                base_url = api_uri,
                *args,
                **kwargs
            )
        elif engine == "openai":
            return ChatOpenAI(
                model = model,
                openai_api_base = api_uri,
                openai_api_key = api_key,
                *args,
                **kwargs
            )
        else:
            raise ValueError(
                f"Invalid model engine: {engine}"
            )

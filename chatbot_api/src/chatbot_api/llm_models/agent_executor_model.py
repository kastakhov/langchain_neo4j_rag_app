from __future__ import annotations
from chatbot_api.structures.singleton import SingletonMeta
from chatbot_api.utils.configuration import Configuration

from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama


class AgentExecutorModel(metaclass = SingletonMeta):
    """
    This class is responsible for initialize the models based on the configuration
    """
    def __init__(self, conf: Configuration) -> None:
        self.app_conf = conf

    def get_agent_model(self, *args, **kwargs) -> ChatOpenAI | ChatOllama:
        engine = self.app_conf.model_engine('ae', 'agent')
        model = self.app_conf.model_name('ae', 'agent')
        api_uri = self.app_conf.model_api_uri('ae', 'agent')
        api_key = self.app_conf.model_api_key('ae', 'agent')
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

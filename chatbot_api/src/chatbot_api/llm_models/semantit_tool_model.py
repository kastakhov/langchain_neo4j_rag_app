from __future__ import annotations
from chatbot_api.structures.singleton import SingletonMeta
from chatbot_api.utils.configuration import Configuration

from langchain_ollama import (
    OllamaEmbeddings,
    ChatOllama
)
from langchain_openai import (
    OpenAIEmbeddings,
    ChatOpenAI
)

class SemantitToolModel(metaclass = SingletonMeta):
    """
    This class is responsible for initialize the models based on the configuration
    """
    def __init__(self, conf: Configuration) -> None:
        self.app_conf = conf

    def get_embeddings_model(self, *args, **kwargs) ->  OllamaEmbeddings | OpenAIEmbeddings:
        engine = self.app_conf.model_engine('st', 'embedding')
        model = self.app_conf.model_name('st', 'embedding')
        api_uri = self.app_conf.model_api_uri('st', 'embedding')
        api_key = self.app_conf.model_api_key('st', 'embedding')

        if bool(kwargs) or bool(args):
            print("WARNING: OllamaEmbeddings|OpenAIEmbeddings does not accept any additional parameters and they are ignored.")
        if engine == "ollama":
            return OllamaEmbeddings(
                model = model,
                base_url = api_uri,
            )
        elif engine == "openai":
            return OpenAIEmbeddings(
                model = model,
                openai_api_base = api_uri,
                openai_api_key = api_key,
            )
        else:
            raise ValueError(
                f"Invalid model engine: {engine}"
            )

    def get_chat_model(self, *args, **kwargs) -> ChatOllama | ChatOpenAI:
        engine = self.app_conf.model_engine('st', 'qa')
        model = self.app_conf.model_name('st', 'qa')
        api_uri = self.app_conf.model_api_uri('st', 'qa')
        api_key = self.app_conf.model_api_key('st', 'qa')
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
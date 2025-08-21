from chatbot_api.utils.configuration import Configuration

from langchain.globals import (
    set_debug,
    set_verbose
)

CHATBOT_CONFIG = Configuration()

set_verbose(CHATBOT_CONFIG.langchain_config['verbose'])
set_debug(CHATBOT_CONFIG.langchain_config['debug'])

from fastapi import FastAPI
from chatbot_api.api.routes import api_router


def run_app() -> FastAPI:
    app = FastAPI(
        title="Hospital Chatbot",
        description="Endpoints for a hospital system graph RAG chatbot",
    )
    app.include_router(api_router)
    return app

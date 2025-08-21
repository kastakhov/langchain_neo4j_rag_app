from fastapi.responses import ORJSONResponse
from fastapi import APIRouter

from chatbot_api.structures.api_models import (
    HospitalQueryInput,
    HospitalQueryOutput
)
from chatbot_api.structures.configuration_model import CoreConfigModel

from chatbot_api.tools.helpers import invoke_agent_with_retry
from chatbot_api.utils.configuration import Configuration


api_router = APIRouter()

@api_router.get("/")
async def get_status():
    return {"status": "running"}

@api_router.post("/rag-agent")
async def ask_rag_agent(query: HospitalQueryInput) -> HospitalQueryOutput:
    query_response = await invoke_agent_with_retry(query.text)
    query_response["intermediate_steps"] = [
        str(s) for s in query_response["intermediate_steps"]
    ]

    return query_response

@api_router.get(
    "/config/show",
    response_class = ORJSONResponse
)
async def get_app_configuration():
    return ORJSONResponse(content = Configuration().core_config)

@api_router.post(
    "/config/update",
    response_class = ORJSONResponse
)
async def update_app_configuration(config: CoreConfigModel):
    try:
        Configuration().update_conf(config.model_dump())
        Configuration().save_conf_file()
        return ORJSONResponse(content = Configuration().core_config)
    except Exception as e:
        return ORJSONResponse(
            content = {'Exception': e.args[0]},
            status_code = 500
        )
   

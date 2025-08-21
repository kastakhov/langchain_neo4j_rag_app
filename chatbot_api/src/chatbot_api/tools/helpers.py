from chatbot_api.utils.async_utils import async_retry
from chatbot_api.agents.rag_agent import RagAgent

@async_retry(max_retries=5, delay=1)
async def invoke_agent_with_retry(query: str):
    """
    Retry the agent if a tool fails to run. This can help when there
    are intermittent connection issues to external APIs.
    """
    agent_executor = RagAgent()
    agent_executor.create_rag_agent_executor()
    return await agent_executor.invoke_async_agent(query)

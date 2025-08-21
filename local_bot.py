#!/usr/bin/env python
import sys
sys.path.append('chatbot_api/src')

from os import path

from pprint import pprint

from dotenv import load_dotenv
load_dotenv()

from chatbot_api.utils.configuration import Configuration

from langchain.globals import (
    set_debug,
    set_verbose
)

set_debug(True)
set_verbose(True)

question = "How much was billed for patient 789's stay?"
print(f"Ask a question: {question}")

CHATBOT_CONFIG = Configuration()

# Updating neo4j uri to localhost
# Using orivate __update_conf method to skip sensetive parameters validation
CHATBOT_CONFIG._Configuration__update_conf(
    {
        'neo4j': {
            'uri': 'bolt://localhost:7687'
        }
    }
)

# If configuration for local_bot script exist use it
if path.exists('local_bot.yaml'):
    CHATBOT_CONFIG.load_conf_file('local_bot.yaml')

# Or to save configuration to a file
# CHATBOT_CONFIG.save_conf_file('local_bot.yaml')

# Or to update configuration from a dictionary
# updates = {
#     'ot':  {
#         'models': {
#             'cypher': {
#                 'temperature': 1,
#             },
#         },
#         'params': {
#             'k_top': '20',
#         },
#     },
# }
# CHATBOT_CONFIG.update_conf(updates)

print('Starting agent...')

from chatbot_api.agents.rag_agent import RagAgent

agent = RagAgent(
    callbacks_config = {
        'langfuse': {
            'session_id': 'my_rag_app',
            'trace_name': 'local_rag_agent',
        }
    }
)
agent.create_rag_agent_executor()

agent.invoke_sync_agent(query = question)

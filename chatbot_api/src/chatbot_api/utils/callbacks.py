from __future__ import annotations
from chatbot_api.utils.configuration import Configuration

from langfuse import Langfuse
from langfuse.client import StatefulTraceClient

class AppCallbacks:
    langfuse_handler: None | StatefulTraceClient = None

    def __init__(
            self
        ) -> None:
        self.app_conf = Configuration()

    def get_lanfuse_trace(
            self,
            config: dict
        ) -> None | StatefulTraceClient:
        if self.langfuse_handler is not None: return self.langfuse_handler
        if not self.app_conf.load_langfuse_config():
            print('Failed to load langfuse configuration')
            return None
        
        langfuse_handler = Langfuse(
            public_key = self.app_conf.langfuse_config['public_key'],
            secret_key = self.app_conf.langfuse_config['secret_key'],
            host = self.app_conf.langfuse_config['uri'],
        )

        try:
            langfuse_handler.auth_check()
        except Exception as e:
            print(f'Failed to authenticate with langfuse: {e}')
            return None

        self.langfuse_handler = langfuse_handler.trace(
            session_id = config.get('session_id', None),
            user_id = config.get('user_id', None),
            name = config.get('trace_name', None),
            tags = config.get('tags', None),
        )
        return self.langfuse_handler

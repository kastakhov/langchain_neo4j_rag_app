from __future__ import annotations
from chatbot_api.structures.singleton import SingletonMeta
from chatbot_api.structures.configuration_model import CoreConfigModel
from chatbot_api.structures.neo4j_model import Neo4jConfModel
from chatbot_api.structures.langchain_model import LangchainConfModel
from chatbot_api.structures.langfuse_model import LangfuseConfModel

from typing import Dict, Set
from copy import deepcopy

from os import environ, path
import yaml

class Configuration(metaclass = SingletonMeta):
    '''
    Configuration class for RAG APP.
    '''

    __core_config: CoreConfigModel = CoreConfigModel()
    
    sensetive_keys: Set[str] = __core_config.sensetive_keys() 

    def __init__(self) -> None:
        self.__load_secrets()
        self.load_conf_file()
        self.__load_langchain()

    def save_conf_file(self, conf_file: str = '') -> None:
        '''
        Save configuration to configuration file.
        '''
        if not conf_file or not path.exists(path.dirname(conf_file)):
            conf_file = self.conf_file
        with open(conf_file, 'w') as file:
            conf = deepcopy(self.__core_config_dict)
            self.__remove_sensetive_data(conf)
            yaml.dump(conf, file)

    def load_conf_file(self, conf_file: str = '') -> None:
        '''
        Load configuration from configuration file.
        '''
        if not conf_file or not path.exists(conf_file):
            conf_file = self.conf_file if path.exists(self.conf_file) else self.default_conf_file
        with open(conf_file, 'r') as file:
            updates = yaml.load(file, Loader=yaml.FullLoader)
            self.update_conf(updates)

    def update_conf(self, updates: Dict[any, any] | None) -> None:
        '''
        Update configuration with new dictionary.
        '''
        if updates is None: return
        self.__remove_sensetive_data(updates)
        self.__update_conf(updates)

    def load_langfuse_config(self) -> bool:
        '''
        Load Langfuse parameters from environment variables.
        '''
        try:
            config = self.__core_config_dict
            for param in LangfuseConfModel().model_fields.keys():
                config['langfuse'][param] = self.__load_env(
                    f'LANGFUSE_{param.upper()}'
                )
            self.__update_conf(config)
            return True
        except (KeyError, TypeError):
            return False

    def model_engine(self, funct: str, model: str) -> str:
        '''
        Get model engine.
        '''
        return self.__core_config_dict[funct]['models'][model]['engine']

    def model_name(self, funct: str, model: str) -> str:
        '''
        Get model name.
        '''
        return self.__core_config_dict[funct]['models'][model]['name']

    def model_api_uri(self, funct: str, model: str) -> str:
        '''
        Get model API URI.
        '''
        return self.__core_config_dict[funct]['models'][model]['api_uri']
    
    def model_api_key(self, funct: str, model: str) -> str:
        '''
        Get model API key.
        '''
        return self.__core_config_dict[funct]['models'][model]['api_key']

    # Attributes
    @property
    def base_app_dir(self) -> str:
        '''
        Base application directory.
        '''
        return path.abspath(path.join(path.dirname(__file__), '../'))

    @property
    def persistent_data_dir(self) -> str:
        '''
        Persistent data directory.
        '''
        return path.join(self.base_app_dir, 'persistent_data')

    @property
    def conf_file(self) -> str:
        '''
        Configuration file.
        '''
        return path.join(self.persistent_data_dir, 'configuration.yaml')

    @property
    def default_conf_file(self) -> str:
        '''
        Default configuration file.
        '''
        return path.join(self.base_app_dir, 'configuration.yaml.default')

    @property
    def agent_executor(self) -> Dict[any, any]:
        '''
        Agent Executor configuration.
        '''
        return self.__core_config.ae.model_dump()

    @property
    def objective_tool(self) -> Dict[any, any]:
        '''
        Objective Tool configuration.
        '''
        return self.__core_config.ot.model_dump()
    
    @property
    def semantic_tool(self) -> Dict[any, any]:
        '''
        Semantic Tool configuration.
        '''
        return self.__core_config.st.model_dump()
    
    @property
    def neo4j_config(self) -> Dict[any, any]:
        '''
        Neo4j configuration.
        '''
        return self.__core_config.neo4j.model_dump()

    @property
    def langchain_config(self) -> Dict[any, any]:
        '''
        Langchain configuration.
        '''
        return self.__core_config.langchain.model_dump()
    
    @property
    def langfuse_config(self) -> Dict[any, any]:
        '''
        Langfuse configuration.
        '''
        return self.__core_config.langfuse.model_dump()
    
    @property
    def core_config(self) -> Dict[any, any]:
        '''
        Core configuration.
        '''
        temp_conf = deepcopy(self.__core_config_dict)
        self.__remove_sensetive_data(temp_conf)
        return temp_conf

    # Private
    @property
    def __core_config_dict(self) -> Dict[any, any]:
        return self.__core_config.model_dump()

    def __engine_validator(self, value):
        if value not in ['openai', 'ollama']:
            raise ValueError('Invalid engine')    
    
    def __temperature_validator(self, value):
        if not 0 <= value <= 1.0:
            raise ValueError('Invalid temperature')

    def __update_conf(self, updates: Dict[any, any]) -> None:
        '''
        Update configuration with new dictionary.
        '''
        new_conf = self.__update_conf_dict(
            self.__core_config_dict,
            updates
        )

        self.__core_config = CoreConfigModel(**new_conf)    

    def __update_conf_dict(self, original: Dict[any, any], updates: Dict[any, any]) -> None:
        '''
        Update configuration with new dictionary.
        '''
        for key, value in updates.items():
            if key not in original: continue

            if isinstance(value, dict) and isinstance(original[key], dict):
                self.__update_conf_dict(original[key], value)
                continue


            if original[key] == value: continue
            if key == 'engine': self.__engine_validator(value)
            if key == 'temperature': self.__temperature_validator(value)

            original[key] = value
        return original

    def __remove_sensetive_data(self, conf: Dict[any, any]) -> None:
        '''
        Remove sensetive data from configuration.
        '''
        if isinstance(conf, dict):
            for key in list(conf):
                if key in self.sensetive_keys:
                    del conf[key]
                elif isinstance(conf[key], dict):
                    self.__remove_sensetive_data(conf[key])

    def __load_secrets(self) -> None:
        '''
        Load secrets from environment variables.
        '''
        config = self.__core_config_dict
        for conf in config:
            if not config[conf].get('models'): continue
            for model in config[conf]['models']:
                for param in ['api_uri', 'api_key']:
                    config[conf]['models'][model][param] = self.__load_env(
                        f'{conf.upper()}_{model.upper()}_{param.upper()}'
                    )

        for param in Neo4jConfModel().model_fields.keys():
            config['neo4j'][param] = self.__load_env(f'NEO4J_{param.upper()}')
        self.__update_conf(config)

    def __load_langchain(self) -> None:
        '''
        Load debug and verbose flags from environment variables.
        '''
        config = self.__core_config_dict
        for param in LangchainConfModel().model_fields.keys():
            config['langchain'][param] = self.__str2bool(
                self.__load_env(
                    f'LANGCHAIN_{param.upper()}',
                    f'{config['langchain'][param]}'
                )
            )
        
        self.__update_conf(config)

    def __load_env(self, env_name: str, default: str = None) -> str:
        '''
        Load environment variable. If not found and default value not provided, raise KeyError.
        '''
        if environ.get(env_name) and environ.get(env_name) != '': return environ[env_name]
        if default: return default
        raise KeyError(f"Environment variable {env_name} didn't found. Please check .env file.")

    def __str2bool(self, string: str) -> bool:
        '''
        Convert string to boolean.
        '''
        if string in ['True', 'true']: return True
        return False

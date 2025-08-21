from typing import Any, Dict, Type
from threading import Lock

class SingletonMeta(type):
    _instances: Dict[Type[Any], Type[Any]] = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs) -> Any:
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
            return cls._instances[cls]

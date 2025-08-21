from os import environ
from time import sleep
import requests

def load_var_from_env(env_name: str) -> str:
    try:
        if environ[env_name] == '':
            print(f"Environment variable {env_name} didn't set correctly. Please check .env file.")
            exit(1)
        return environ[env_name]
    except KeyError:
        print(f"Environment variable {env_name} didn't found. Please check .env file.")
        exit(1)

def wait_for_startup() -> bool:
    try:
        resp = requests.get(f"{load_var_from_env('CHATBOT_URL')}")
        if resp.status_code == 200:
            return True
        return False
    except:
        return False


if __name__ == "__main__":
    for _ in range(20):
        if wait_for_startup():
            print("API server is ready.")
            exit(0)
        print("API server is not ready yet, waiting for 10 seconds...")
        sleep(10)
    exit(1)
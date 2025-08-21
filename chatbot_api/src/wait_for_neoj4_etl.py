import requests
from time import sleep
from os import environ


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
        response = requests.get(load_var_from_env("NEO4J_ETL_URL") + "/status.json")
        if response.status_code == 200:
            response_json = response.json()
            if response_json["status"] == "running":
                print("NEO4J ETL is running.")
                return False
            elif response_json["status"] == "loaded":
                print("NEO4J ETL csv loading done.")
                return True
        return False
    except:
        return False

if __name__ == "__main__":
    for _ in range(20):
        if wait_for_startup():
            print("NEO4J ETL is ready.")
            exit(0)
        print("NEO4J ETL is not ready yet, waiting for 10 seconds...")
        sleep(10)
    exit(1)
import neo4j
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
        with neo4j.GraphDatabase.driver(
            load_var_from_env("NEO4J_URI"),
            auth = (
                load_var_from_env("NEO4J_USERNAME"),
                load_var_from_env("NEO4J_PASSWORD")
            )
        ) as driver:
            driver.verify_connectivity()
        return True
    except:
        return False


if __name__ == "__main__":
    for _ in range(20):
        if wait_for_startup():
            print("Neo4j is ready.")
            exit(0)
        print("Neo4j is not ready yet, waiting for 10 seconds...")
        sleep(10)
    exit(1)
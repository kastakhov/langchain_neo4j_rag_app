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

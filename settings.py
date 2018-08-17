import dotenv

env_path = '.env'

def get(key):
    return dotenv.get_key(env_path, key)

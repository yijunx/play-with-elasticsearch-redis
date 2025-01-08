import os

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    # this is to take in all the environment variables
    # this is for the logging purpose
    # when deployed on cloud, the name and ver should come from envvar
    ENV: str
    SERVICE_NAME: str
    SERVICE_VERSION: str
    # NAMESPACE: str

    # postgres if you need, follow your devcontainer settings
    # DATABASE_URI: PostgresDsn

    # listens on the redis channel for messages
    REDIS_MSG_HOST: str
    REDIS_MSG_PORT: int
    REDIS_MSG_USER: str = "default"
    REDIS_MSG_SSL: bool
    REDIS_MSG_PASSWORD: str
    REDIS_MSG_DB: int
    REDIS_MSG_CHANNEL: str

    # create a task into the
    REDIS_TASK_HOST: str
    REDIS_TASK_PORT: int
    REDIS_TASK_USER: str = "default"
    REDIS_TASK_SSL: bool
    REDIS_TASK_PASSWORD: str
    REDIS_TASK_DB: int
    # queues
    REDIS_RAG_TASK_QUEUE: str

    # remote services
    # ACCOUNT_SERVICE_HOST: str
    # ACCOUNT_SERVICE_PORT: int
    # SPACE_SERVICE_HOST: str
    # SPACE_SERVICE_PORT: int
    # PRODUCT_SERVICE_HOST: str
    # PRODUCT_SERVICE_PORT: int


class LocalDevSettings(EnvSettings):
    # it reads from a config file at root
    # this config file is gitignored
    # this config file needs to have a template
    model_config = SettingsConfigDict(env_file="config", extra="ignore")


class DeployedSettings(EnvSettings):
    # takes in env vars from the pod
    ...


def find_config() -> EnvSettings:
    if os.getenv("ENV"):
        return DeployedSettings()
    else:
        return LocalDevSettings()


env = find_config()


if __name__ == "__main__":
    print(env)

import os

from pydantic import BaseSettings, PostgresDsn


class DevConfigs(BaseSettings):
    POSTGRES_DSN: PostgresDsn

    SECRET_KEY: str

    class Config:
        env_file = ".env"
        env_prefix = "DEV_"
        env_file_encoding = "utf-8"


class TestConfigs(DevConfigs):
    class Config:
        env_prefix = "TEST_"


class ProdConfigs(DevConfigs):
    class Config:
        env_prefix = "PROD_"


def factory():
    env = os.environ.get("ENV", "dev")

    development = DevConfigs()
    testing = TestConfigs()
    production = ProdConfigs()

    if env == "dev":
        return development
    elif env == "test":
        return testing
    elif env == "prod":
        return production


configs = factory()

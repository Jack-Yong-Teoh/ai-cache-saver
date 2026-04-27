# pylint: disable=invalid-name
import os
from dataclasses import dataclass

def load_env_file(filepath):
    # FIX: Check if file exists before trying to open it
    if not os.path.exists(filepath):
        print(f"Notice: '{filepath}' not found. Skipping file load (using Docker env vars).")
        return

    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ[key] = value

# Now this is safe to run
load_env_file(".env")

@dataclass(frozen=True)
class AuthConfig:
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    PASSWORD_SALT: str = os.environ.get("PASSWORD_SALT")


@dataclass(frozen=True)
class DBConfig:
    HOST: str = os.environ.get("DB_HOST")
    USERNAME: str = os.environ.get("DB_USERNAME")
    PASSWORD: str = os.environ.get("DB_PASSWORD")
    PORT: str = os.environ.get("DB_PORT")
    DATABASE: str = os.environ.get("DB_DATABASE")


@dataclass(frozen=True)
class RedisConfig:
    HOST: str = os.environ.get("REDIS_HOST")
    PASSWORD: str = os.environ.get("REDIS_PASSWORD")
    PORT: str = os.environ.get("REDIS_PORT")


@dataclass(frozen=True)
class SlaveDBConfig:
    HOST: str = os.environ.get("DB_HOST")
    USERNAME: str = os.environ.get("DB_USERNAME")
    PASSWORD: str = os.environ.get("DB_PASSWORD")
    PORT: str = os.environ.get("DB_PORT")
    DATABASE: str = os.environ.get("DB_DATABASE")


@dataclass(frozen=True)
class Config:
    AUTH: AuthConfig = AuthConfig()
    DB: DBConfig = DBConfig()
    REDIS: RedisConfig = RedisConfig()
    SLAVE_DB: SlaveDBConfig = SlaveDBConfig()


CONFIG = Config()

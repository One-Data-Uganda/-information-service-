from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, HttpUrl, PostgresDsn, RedisDsn, validator


class Settings(BaseSettings):
    CONFIG_TYPE: str = "prod"
    DEPLOYMENT: str = "easy-portal"
    APPLICATION_NAME: str = "Information Service"
    API_V1_STR: str = "/v1"
    SECRET_KEY: str = (
        "ife1f905fbf223243cc7d2ec2a3d4a6dd4889d2c5dce51fb9219e9659bbe1becd"
    )
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SENTRY_ENVIRONMENT: str = "production"
    SENTRY_DSN: Optional[HttpUrl] = None

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if not v or len(v) == 0:
            return None
        return v

    UPLOADED_FILES_DEST: str = "/project/data"

    WEBSERVICE_HOST: str = "http://192.168.150.53:10018"
    WEBSERVICE_PATH: str = "feedwebservice"
    NSQD_HOST: str = "nsqd"
    NSQD_PORT: int = 4150

    JAEGER_HOST: str = "192.168.150.113"

    GRAYLOG_SERVER: str = "5.189.184.162"
    GRAYLOG_PORT: int = 12201

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_TYPE: str = "redis"
    REDIS_URL: Optional[RedisDsn] = None
    CELERY_BACKEND_DB: int = 1
    CELERY_BROKER_DB: int = 0

    CELERY_BACKEND: Optional[RedisDsn] = None
    CELERY_BROKER: Optional[RedisDsn] = None

    @validator("REDIS_URL", pre=True)
    def assemble_redis_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme=values.get("REDIS_TYPE"),
            port=str(values.get("REDIS_PORT")),
            host=values.get("REDIS_HOST"),
        )

    @validator("CELERY_BACKEND", pre=True)
    def assemble_celery_backend(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme=values.get("REDIS_TYPE"),
            port=str(values.get("REDIS_PORT")),
            host=values.get("REDIS_HOST"),
            path=f"/{values.get('CELERY_BACKEND_DB')}",
        )

    @validator("CELERY_BROKER", pre=True)
    def assemble_celery_broker(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme=values.get("REDIS_TYPE"),
            port=str(values.get("REDIS_PORT")),
            host=values.get("REDIS_HOST"),
            path=f"/{values.get('CELERY_BROKER_DB')}",
        )

    POSTGRES_SERVER: str = "information-db"
    POSTGRES_USER: str = "one_information"
    POSTGRES_PASSWORD: str = "one_information"
    POSTGRES_PORT_5432_TCP_PORT: str = "5432"
    POSTGRES_DB: str = "one_information"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT_5432_TCP_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True


settings = Settings()

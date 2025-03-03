from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str
    port: int
    login: str
    password: str
    base_host: str
    base_port: int
    base_name: str
    gigachat_credentials: str
    milvus_host: str
    milvus_port: str


settings = Settings(
    _env_file= '.env',
    _env_file_encoding='utf-8',
)

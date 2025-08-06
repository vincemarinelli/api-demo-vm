from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    aws_profile: str
    aws_region: str
    ssl_flag: bool
    athena_s3_staging_dir: str
    athena_database: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

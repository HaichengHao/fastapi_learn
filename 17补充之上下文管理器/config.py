"""
@File    :config.py
@Editor  : 百年
@Date    :2026/2/9 17:49 
"""
import os

from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL : str
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

Config = Settings()
print(Config.DATABASE_URL)
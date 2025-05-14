from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, Literal
import yaml
from pathlib import Path
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env.local
load_dotenv('.env.local')

class Settings(BaseSettings):
    # Database Settings
    database_url: str
    db_echo: bool = False
    
    # JWT Settings
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    
    # Service Settings
    core_service_url: str = "http://localhost:13080"
    cors_origins: Optional[str] = None  # Comma-separated list of allowed origins
    
    # Logging Settings
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=('.env', '.env.local'),
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )

def substitute_env_vars(value: str) -> str:
    """Replace ${VAR} with environment variable values"""
    if not isinstance(value, str):
        return value
    
    def replace_var(match):
        var_name = match.group(1)
        return os.getenv(var_name, match.group(0))
    
    return re.sub(r'\${([^}]+)}', replace_var, value)

def process_config_values(config: dict) -> dict:
    """Process config values to substitute environment variables"""
    processed = {}
    for key, value in config.items():
        if isinstance(value, dict):
            processed[key] = process_config_values(value)
        elif isinstance(value, list):
            processed[key] = [substitute_env_vars(item) for item in value]
        else:
            processed[key] = substitute_env_vars(value)
    return processed

def load_configmap(config_path: str = "configmap.yml") -> dict:
    """Load and process configuration from configmap.yml"""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            return process_config_values(config)
    except FileNotFoundError:
        return {}

def get_settings() -> Settings:
    """Get settings with processed configmap overrides"""
    configmap = load_configmap()
    return Settings(**configmap)

settings = get_settings() 
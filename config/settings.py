"""
Configuration Settings
File: config/settings.py
"""

import os
from pathlib import Path

# Try to load dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, use system environment variables


class Settings:
    """Application settings"""
    
    # API Configuration
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "claude-sonnet-4-5-20250929")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "4096"))
    
    # Agent Configuration
    MAX_ITERATIONS: int = int(os.getenv("MAX_ITERATIONS", "10"))
    ENABLE_LOGGING: bool = os.getenv("ENABLE_LOGGING", "true").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Tool Configuration
    ENABLE_FILE_OPERATIONS: bool = os.getenv("ENABLE_FILE_OPERATIONS", "true").lower() == "true"
    ENABLE_WEB_SEARCH: bool = os.getenv("ENABLE_WEB_SEARCH", "false").lower() == "true"
    ENABLE_DATABASE: bool = os.getenv("ENABLE_DATABASE", "false").lower() == "true"
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    LOG_DIR: Path = BASE_DIR / os.getenv("LOG_DIR", "logs")
    DATA_DIR: Path = BASE_DIR / os.getenv("DATA_DIR", "data")
    CACHE_DIR: Path = BASE_DIR / os.getenv("CACHE_DIR", "cache")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        if not cls.ANTHROPIC_API_KEY:
            print("⚠️  Warning: ANTHROPIC_API_KEY is not set in .env file")
            print("   Please set it before running the agent")
        
        # Create directories if they don't exist
        cls.LOG_DIR.mkdir(exist_ok=True)
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.CACHE_DIR.mkdir(exist_ok=True)
        
        return True


# Create settings instance
settings = Settings()

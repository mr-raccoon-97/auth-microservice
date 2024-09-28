from dotenv import load_dotenv
from pydantic import Field
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class DatabaseSettings(BaseSettings):
    host: str = Field(default='localhost')
    port: int = Field(default=5432)
    user: str = Field(...)
    name: str = Field(...)
    password: SecretStr = Field(...)
    model_config = SettingsConfigDict(env_prefix='DATABASE_')

    @property
    def dns(self) -> str:
        return f'postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}'
    

class Settings(BaseSettings):
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
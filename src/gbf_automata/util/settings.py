from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from gbf_automata.enums.content_type import ContentType
from gbf_automata.schema.arcarum_v2 import ArcarumV2Model

load_dotenv()


class Settings(BaseSettings):
    display: str = Field(default=None)
    log_level: str = "INFO"
    log_format: str = "[%(asctime)s] [%(levelname)s] [%(thread)s] - %(message)s"

    content_type: ContentType = Field(default=None)
    arcarum_v2: ArcarumV2Model = Field(default=None)

    @field_validator("content_type", mode="before")
    @classmethod
    def str_to_enum(cls, value) -> ContentType:
        for member in ContentType:
            if member.name.lower() == value.lower():
                return member
        raise TypeError("Invalid Enum")

    class Config:
        env_file = ".env"
        envi_file_encoding = "utf-8"


settings = Settings()

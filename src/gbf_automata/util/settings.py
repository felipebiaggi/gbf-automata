from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from gbf_automata.enums.content_type import ContentType
from gbf_automata.schema.arcarum_v2 import ArcarumV2Model

class Settings(BaseSettings):
    display: str = Field(default=None)
    log_level: str = "INFO"
    log_format: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

    image_menu: str = Field(default=None)
    image_news: str = Field(default=None)
    image_home_top: str = Field(default=None)
    image_home_bottom: str = Field(default=None)
    image_back: str = Field(default=None)
    image_reload: str = Field(default=None)
    image_arcarum: str = Field(default=None)
    image_gw: str = Field(default=None)

    image_button_classic: str = Field(default=None)
    image_button_sandbox: str = Field(default=None)
    image_zone_mundus: str = Field(default=None)

    image_zone_eletio: str = Field(default=None)
    image_zone_faym: str = Field(default=None)
    image_zone_goliath: str = Field(default=None)
    image_zone_harbinger: str = Field(default=None)

    image_zone_invidia: str = Field(default=None)
    image_zone_joculator: str = Field(default=None)
    image_zone_kalendae: str = Field(default=None)
    image_zone_liber: str = Field(default=None)

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


if __name__ == "__main__":
    print(settings.arcarum_v2)    

    pass    



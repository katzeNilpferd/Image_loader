import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Config:
    upload_url: str
    max_concurrent: int
    images_dir: str
    mode: str 


def load_config() -> Config:
    return Config(
        upload_url=os.getenv("UPLOAD_URL", ""),
        max_concurrent=int(os.getenv("MAX_CONCURRENT", "4")),
        images_dir=os.getenv("IMAGES_DIR", "./images"),
        mode=os.getenv("UPLOADER_MODE", "sync"),
    )

import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Config:
    upload_url: str
    max_workers: int
    images_dir: str


def load_config() -> Config:
    return Config(
        upload_url=os.getenv("UPLOAD_URL", ""),
        max_workers=int(os.getenv("MAX_WORKERS", "4")),
        images_dir=os.getenv("IMAGES_DIR", "./images")
    )

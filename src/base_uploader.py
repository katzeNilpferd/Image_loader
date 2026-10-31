from abc import ABC, abstractmethod
from pathlib import Path


class ImageCollectorMixin:
    """Общий код для sync/async загрузчиков: расширения, URL, лимит, сбор файлов."""

    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

    def __init__(self, upload_url: str, max_concurrent: int) -> None:
        self.upload_url = upload_url
        self.max_concurrent = max_concurrent

    def collect_images(self, images_dir: str) -> list[Path]:
        """Возвращает список файлов-картинок из указанной папки."""
        folder = Path(images_dir)
        return [
            p for p in folder.iterdir()
            if p.is_file() and p.suffix.lower() in self.IMAGE_EXTENSIONS
        ]


class BaseSyncUploader(ImageCollectorMixin, ABC):
    """Контракт синхронного загрузчика."""

    @abstractmethod
    def upload(self, paths: list[Path]) -> list[tuple[Path, object]]:
        """Загружает все файлы, соблюдая лимит."""
        raise NotImplementedError


class BaseAsyncUploader(ImageCollectorMixin, ABC):
    """Контракт асинхронного загрузчика."""

    @abstractmethod
    async def upload(self, paths: list[Path]) -> list[tuple[Path, object]]:
        """Загружает все файлы, соблюдая лимит (await)."""
        raise NotImplementedError

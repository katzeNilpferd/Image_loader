import asyncio
from pathlib import Path

import aiofiles
import aiohttp


class AsyncImageUploader:

    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

    def __init__(self, upload_url: str) -> None:
        self.upload_url = upload_url

    def collect_images(self, images_dir: str) -> list[Path]:
        """Возвращает список файлов-картинок из папки."""
        folder = Path(images_dir)

        return [
            p for p in folder.iterdir()
            if p.is_file() and p.suffix.lower() in self.IMAGE_EXTENSIONS
        ]

    async def upload_all(
        self,
        paths: list[Path],
        max_concurrent_uploads: int = 4,
    ) -> list[tuple[Path, object]]:
        semaphore = asyncio.Semaphore(max_concurrent_uploads)

        async with aiohttp.ClientSession() as session:
            tasks = [
                self._upload_with_limit(session, path, semaphore)
                for path in paths
            ]
            return await asyncio.gather(*tasks)

    async def _upload_with_limit(
        self,
        session: aiohttp.ClientSession,
        path: Path,
        semaphore: asyncio.Semaphore,
    ) -> tuple[Path, object]:
        async with semaphore:
            try:
                result: object = await self._upload_one(session, path)
            except Exception as e:
                result = e
            return path, result

    async def _upload_one(
        self,
        session: aiohttp.ClientSession,
        path: Path,
    ) -> dict:
        async with aiofiles.open(path, "rb") as f:
            content = await f.read()

        form = aiohttp.FormData()
        form.add_field(
            "file",
            content,
            filename=path.name,
            content_type="application/octet-stream",
        )

        async with session.post(self.upload_url, data=form) as resp:
            resp.raise_for_status()
            return await resp.json()

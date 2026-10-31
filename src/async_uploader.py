import asyncio
from typing import Any
from pathlib import Path

import aiofiles
import aiohttp

from src.base_uploader import BaseAsyncUploader


class AsyncImageUploader(BaseAsyncUploader):
    """Асинхронный загрузчик картинок на семафоре."""

    async def upload(self, paths: list[Path]) -> list[tuple[Path, object]]:
        semaphore = asyncio.Semaphore(self.max_concurrent)

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
    ) -> dict[str, Any]:
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

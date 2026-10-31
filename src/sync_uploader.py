from typing import Any
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

from src.base_uploader import BaseSyncUploader


class SyncImageUploader(BaseSyncUploader):
    """Синхронный загрузчик картинок на пуле потоков."""

    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


    def upload(self, paths: list[Path]) -> list[tuple[Path, object]]:
        results: list[tuple[Path, object]] = []

        with requests.Session() as session:
            with ThreadPoolExecutor(max_workers=self.max_concurrent) as pool:
                futures = {
                    pool.submit(self._upload_one, session, path): path
                    for path in paths
                }
                for fut in as_completed(futures):
                    path = futures[fut]
                    try:
                        results.append((path, fut.result()))
                    except Exception as e:
                        results.append((path, e))

        return results

    def _upload_one(
        self,
        session: requests.Session,
        path: Path,
    ) -> dict[str, Any]:
        with open(path, "rb") as f:
            resp = session.post(
                self.upload_url,
                files={"file": f},
            )
            resp.raise_for_status()
            return resp.json()

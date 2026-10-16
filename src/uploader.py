from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


class ImageUploader:

    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

    def __init__(
        self,
        upload_url: str,
        max_workers: int
    ):
        self.upload_url = upload_url
        self.max_workers = max_workers

    def collect_images(self, images_dir: str) -> list[Path]:
        folder = Path(images_dir)

        return [
            p for p in folder.iterdir()
            if p.is_file() and p.suffix.lower() in self.IMAGE_EXTENSIONS
        ]

    def upload_all(self, paths: list[Path]) -> list[tuple[Path, object]]:
        results: list[tuple[Path, object]] = []

        with requests.Session() as session:
            with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
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
        path: Path
    ) -> dict:
        with open(path, "rb") as f:
            resp = session.post(
                self.upload_url,
                files={"file": f}
            )
            resp.raise_for_status()
            return resp.json()

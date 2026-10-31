import argparse
import asyncio

from src.config import load_config
from src.base_uploader import BaseAsyncUploader, BaseSyncUploader
from src.sync_uploader import SyncImageUploader
from src.async_uploader import AsyncImageUploader


def parse_args(config) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload images to server")
    parser.add_argument(
        "--mode",
        choices=["sync", "async"],
        default=config.mode,
        help="Uploader implementation (default: from UPLOADER_MODE env, else sync)",
    )
    return parser.parse_args()


def print_results(results: list[tuple[object, object]]) -> None:
    for path, result in results:
        status = "FAIL" if isinstance(result, Exception) else "OK"
        print(f"{status} - {path}: {result}")


def run_sync(uploader: BaseSyncUploader, paths: list) -> None:
    print_results(uploader.upload(paths))


async def run_async(uploader: BaseAsyncUploader, paths: list) -> None:
    print_results(await uploader.upload(paths))


def main() -> None:
    config = load_config()
    args = parse_args(config)

    uploader_cls = AsyncImageUploader if args.mode == "async" else SyncImageUploader
    uploader = uploader_cls(
        upload_url=config.upload_url,
        max_concurrent=config.max_concurrent,
    )

    paths = uploader.collect_images(images_dir=config.images_dir)
    if not paths:
        print("No images found")
        return

    if isinstance(uploader, BaseAsyncUploader):
        asyncio.run(run_async(uploader, paths))
    else:
        run_sync(uploader, paths)


if __name__ == "__main__":
    main()

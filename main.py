from src.uploader import ImageUploader
from src.config import load_config


def main() -> None:
    config = load_config()
    uploader = ImageUploader(
        upload_url=config.upload_url,
        max_workers=config.max_workers
    )

    paths = uploader.collect_images(
        images_dir=config.images_dir
    )
    
    if not paths:
        print("No images found")
        return

    print(f"Uploading {len(paths)} images with {4} workers")

    for path, result in uploader.upload_all(paths):
        if isinstance(result, Exception):
            print(f"FAIL - {path}: {result}")
        else:
            print(f"OK - {path}: {result}")


if __name__ == "__main__":
    main()

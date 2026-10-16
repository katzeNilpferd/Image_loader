from src.uploader import ImageUploader


def main() -> None:
    uploader = ImageUploader(
        upload_url="http://127.0.0.1:8000/upload",
        max_workers=4
    )

    paths = uploader.collect_images(
        images_dir="./images"
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

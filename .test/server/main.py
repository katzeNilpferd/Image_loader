import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, UploadFile, File


app = FastAPI(title="Test Upload Server")


UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/upload")
async def upload(
    file: UploadFile = File(...)
) -> dict[str, Any]:
    ext = Path(file.filename).suffix.lower()

    saved_name = f"{uuid.uuid4().hex}{ext}"
    dest = UPLOAD_DIR / saved_name

    content = await file.read()
    dest.write_bytes(content)

    return {
        "filename": file.filename,
        "size": len(content),
    }

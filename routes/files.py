import time
from fastapi import APIRouter, Request, Depends
from fastapi.responses import FileResponse
from pathvalidate import sanitize_filename
from config import db
from dependencies import require_session_user, rate_limiter
from uuid import UUID
from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException
import filetype

from pathlib import Path
import uuid

STORAGE_DIR = Path("storage")

MAX_SIZE = 25 * 1024 * 1024
router = APIRouter(prefix="/files", tags=["files"])

@router.get("/files")
async def list_files(user=Depends(require_session_user)):
    files = db.table("files") \
        .select("*") \
        .eq("owner_id", user["id"]) \
        .cache(ttl=300)\
        .execute()
    return files.data

@router.post("/upload", dependencies=[Depends(rate_limiter)])
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    folder_id: str | None = Form(None),
    user=Depends(require_session_user)
):
    user_id = user["id"]
    print (user_id)
    data = await file.read(MAX_SIZE + 1)
    if not data:
        raise HTTPException(422, "Empty file")
    if len(data) > MAX_SIZE:
        raise HTTPException(413, "File too large")

    kind = filetype.guess(data)
    mime = kind.mime if kind else (file.content_type or "application/octet-stream")

    name = sanitize_filename(file.filename or "")[:255]
    if not name:
        raise HTTPException(422, "Invalid filename")



    storage_key = f"{user_id}/{uuid.uuid4()}"
    # insert into files table: name, folder_id, owner_id=user_id,
    dest = STORAGE_DIR / storage_key
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)

    size = len(data)
    try:
        result = db.table("files").insert({
                "name": name,
                "owner_id": user["id"],
                "storage_key": storage_key,
                "mime_type": mime,
                "size": size
        }).execute()
    except:
        dest.unlink(missing_ok=True)
        raise

    return {"success": "True"}

@router.get("/download/{file_id}")
async def download(file_id: UUID, user=Depends(require_session_user)):
    user_id = user["id"]

    result = (
        db.table("files")
        .select("*")
        .eq("id", str(file_id))
        .eq("owner_id", user_id)
        .execute()
    )
    if not result.data:
        raise HTTPException(404, "File not found")
    row = result.data[0]

    path = (STORAGE_DIR / row["storage_key"]).resolve()
    if STORAGE_DIR.resolve() not in path.parents or not path.is_file():
        raise HTTPException(404, "File not found")

    return FileResponse(
        path,
        filename=row["name"],
        media_type=row["mime_type"],
        content_disposition_type="attachment",
    )

# Invalidate cache after mutation
@router.delete("/files/{file_id}")
async def delete_file(file_id: str):
    db.table("files").delete().eq("id", file_id).execute()
    db.cache_invalidate("files")

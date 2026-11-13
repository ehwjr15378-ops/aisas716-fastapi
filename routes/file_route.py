import os
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

# 저장 위치 : 프로젝트 -> /static/files
BASE_DIR = Path(__file__).resolve().parent.parent   # 프로젝트 폴더
UPLOAD_DIR = BASE_DIR / "static" / "files"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

file_router = APIRouter(tags=["File"])


def safe_path(filename: str) -> Path:
    """파일명만 사용하도록 정리 (../ 같은 경로 이동 방지)"""
    name = Path(filename).name
    if not name or name.startswith("."):
        raise HTTPException(status_code=400, detail="올바른 파일명이 아닙니다.")
    return UPLOAD_DIR / name


# 1. 파일 업로드 : 파일 선택 후 전송
@file_router.post("/upload", status_code=status.HTTP_201_CREATED, summary="파일 업로드")
async def upload_file(file: UploadFile = File(...)) -> dict:
    save_path = safe_path(file.filename)
    content = await file.read()
    with open(save_path, "wb") as f:
        f.write(content)
    return {"msg": "업로드 성공", "filename": save_path.name, "size": len(content)}


# 2. 파일 다운로드 : 파일명 입력 후 전송 -> 다운로드
@file_router.get("/download", summary="파일 다운로드")
async def download_file(filename: str):
    file_path = safe_path(filename)
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="존재하지 않는 파일입니다.")
    return FileResponse(path=file_path, filename=file_path.name,
                        media_type="application/octet-stream")


# 3. 전체 파일 목록 보기
@file_router.get("/", summary="전체 파일 목록")
async def list_files() -> dict:
    files = [
        {"filename": name, "size": os.path.getsize(UPLOAD_DIR / name)}
        for name in sorted(os.listdir(UPLOAD_DIR))
        if (UPLOAD_DIR / name).is_file() and not name.startswith(".")
    ]
    return {"count": len(files), "files": files}
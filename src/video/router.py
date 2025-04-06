from fastapi import APIRouter,HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from typing import Annotated
import os
from pathlib import Path
from enum import Enum

from src.config import MY_VIDEOS_PATH


router = APIRouter(
    prefix="/video",
    tags=["Video"],
)

folder_path = Path(MY_VIDEOS_PATH)

# Получаем список всех видеофайлов
def get_video_list() -> list[str]:
    return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# Динамически создаем Enum на основе доступных файлов
class VideoFile(str, Enum):
    @classmethod
    def load(cls):
        return {video: video for video in get_video_list()}

# Динамически создаем Enum
VideoFile = Enum("VideoFile", VideoFile.load())

@router.get("/get_videos_name/")
async def get_videos_name():
    try:
        video_files = get_video_list()

        if len(video_files) != 0:
            return {"Videos_name": video_files}
        else:
            return {"detail": "no videos"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@router.get("/look_videos/{video}")
async def look_videos(video: Annotated[VideoFile, Path()]):
    file_path = folder_path / video.value

    return FileResponse(file_path,
                        media_type="video/mp4",
                        headers={"Content-Disposition": "inline"})

'''
def iterfile(file_path: str):
    with open(file_path, "rb") as file:
        while chunk := file.read(2048*2048):
            yield chunk

@router.get("/look_streaming_videos/{video}")
async def look_streaming_videos(video: Annotated[VideoFile, Path()]):
    file_path = folder_path / video.value

    return StreamingResponse(iterfile(file_path),
                        media_type="video/mp4")
'''

@router.get("/download_video/{video}")
async def download_video(video: Annotated[VideoFile, Path()]):
    file_path = folder_path / video.value
    return FileResponse(
        file_path,
        media_type="application/octet-stream",  # Универсальный бинарный тип (гарантирует скачивание)
        headers={"Content-Disposition": f"attachment; filename={file_path.name}"}
    )

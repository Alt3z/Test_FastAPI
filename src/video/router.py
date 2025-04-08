from fastapi import APIRouter,HTTPException, Depends
from fastapi.responses import FileResponse, StreamingResponse
from typing import Annotated
import os
from pathlib import Path
from enum import Enum

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.video.models import Video
from src.database import get_async_session, async_session_maker
from src.config import MY_VIDEOS_PATH


router = APIRouter(
    prefix="/video",
    tags=["Video"],
)

folder_path = Path(MY_VIDEOS_PATH)


async def get_video_list():
    try:
        async with async_session_maker() as session:
            stmt = select(Video)
            result = await session.execute(stmt)
            return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/get_videos_name/")
async def get_videos_name(videos: Annotated[list[Video], Depends(get_video_list)]):
    try:
        if videos:
            response = [{"id": video.id, "name": video.name} for video in videos]
            return {"Videos": response}
        return {"Videos": "no videos"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


async def get_need_video(video_name: str):
    try:
        async with async_session_maker() as session:
            stmt = select(Video.path).where(Video.name == video_name)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/look_videos/{video_name}")
async def look_videos(video_path: Annotated[str, Depends(get_need_video)]):
    try:
        if video_path:
            return FileResponse(video_path,
                                media_type="video/mp4",
                                headers={"Content-Disposition": "inline"})
        raise HTTPException(status_code=404, detail=f"No video in database")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@router.get("/get_videos/{video_name}")
async def get_videos(video_path: Annotated[str, Depends(get_need_video)]):
    try:
        if video_path:  # Если видео найдено в базе данных
            # Извлекаем только имя файла без пути
            video_filename = Path(video_path).name
            return FileResponse(
                video_path,
                media_type="application/octet-stream",  # Универсальный тип для скачивания
                headers={"Content-Disposition": f"attachment; filename=\"{video_filename}\""}
            )
        raise HTTPException(status_code=404, detail="No video found in database")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error while downloading video: {str(e)}")



# I will drop 250 thousand tons of TNT on you.mp4
# Rick Astley - Never Gonna Give You Up.mp4

'''
return FileResponse(
    video_path,
    media_type="application/octet-stream",
    headers={"Content-Disposition": f"attachment; filename=\"{video_filename}\""}
)
'''

'''
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

'''
@router.get("/download_video/{video}")
async def download_video(video: Annotated[VideoFile, Path()]):
    file_path = folder_path / video.value
    return FileResponse(
        file_path,
        media_type="application/octet-stream",  # Универсальный бинарный тип (гарантирует скачивание)
        headers={"Content-Disposition": f"attachment; filename={file_path.name}"}
    )
'''
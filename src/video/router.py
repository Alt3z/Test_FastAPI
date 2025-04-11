from fastapi import APIRouter,HTTPException, Depends
from fastapi.responses import FileResponse
from typing import Annotated
from pathlib import Path
import json

import redis.asyncio as redis
from redis.asyncio import ConnectionPool

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from src.video.models import Video
from src.database import async_session_maker
from src.config import MY_VIDEOS_PATH


router = APIRouter(
    prefix="/video",
    tags=["Video"],
)


# Создаём асинхронный пул соединений
redis_pool = ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
redis_client = redis.Redis(connection_pool=redis_pool)

#redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

folder_path = Path(MY_VIDEOS_PATH)

async def get_video_list():
    try:
        cache_key = "video_list"

        cached_data = await redis_client.get(cache_key)
        if cached_data:
            # Декодируем JSON в Python-объекты
            return json.loads(cached_data)

        async with async_session_maker() as session:
            stmt = select(Video)
            result = await session.execute(stmt)
            videos = result.scalars().all()

            videos_data = [{"id": video.id, "name": video.name} for video in videos]

            # Кэшируем в Redis (на 60 секунд)
            await redis_client.set(cache_key, json.dumps(videos_data), ex=60)
            return videos_data
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/get_videos_name/")
async def get_videos_name(videos: Annotated[list[Video], Depends(get_video_list)]):
    try:
        if videos:
            return {"Videos": videos}
        return {"Videos": "no videos"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


async def get_need_video(video_name: str):
    try:
        cache_key = f"video:{video_name}"

        cached_data = await redis_client.get(cache_key)
        if cached_data:
            video = json.loads(cached_data)
            return video["path"]

        async with async_session_maker() as session:
            stmt = select(Video.name, Video.path).where(Video.name == video_name)
            result = await session.execute(stmt)
            video = result.one_or_none()

            if video:
                # Кэшируем в Redis на 60 секунд
                await redis_client.set(
                    cache_key,
                    json.dumps({"name": video.name, "path": video.path}),
                    ex=60
                )
                return video.path

            raise HTTPException(status_code=404, detail="Video not found")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/look_videos/{video_name}")
async def look_videos(video_path: Annotated[str, Depends(get_need_video)]):
    try:
        video_file = Path(video_path)
        if not video_file.exists():
            raise HTTPException(status_code=404, detail="File not found on disk")

        if not video_file.resolve().is_relative_to(folder_path.resolve()):
            raise HTTPException(status_code=403, detail="Access denied")

        return FileResponse(
            video_file,
            media_type="video/mp4",
            headers={"Content-Disposition": "inline"}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@router.get("/get_videos/{video_name}")
async def get_videos(video_path: Annotated[str, Depends(get_need_video)]):
    try:
        video_file = Path(video_path)
        if not video_file.exists():
            raise HTTPException(status_code=404, detail="File not found on disk")

        if not video_file.resolve().is_relative_to(folder_path.resolve()):
            raise HTTPException(status_code=403, detail="Access denied")

        return FileResponse(
            video_file,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename=\"{video_file.name}\""}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error while downloading video: {str(e)}")


# I will drop 250 thousand tons of TNT on you.mp4
# Rick Astley - Never Gonna Give You Up.mp4
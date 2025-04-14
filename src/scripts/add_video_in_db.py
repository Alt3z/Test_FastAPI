import os
from pathlib import Path
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database import get_async_session
from src.config import MY_VIDEOS_PATH
from src.video.models import Video

# Путь к папке с видео
VIDEO_FOLDER = Path(MY_VIDEOS_PATH)


async def load_videos_to_db(session: AsyncSession):
    # Сканируем папку на наличие видеофайлов
    video_files = [f for f in os.listdir(VIDEO_FOLDER) if os.path.isfile(VIDEO_FOLDER / f)]

    # Получаем список уже существующих записей в БД
    existing_videos = await session.execute(select(Video.name))
    existing_names = {row[0] for row in existing_videos.fetchall()}

    # Добавляем только те файлы, которых нет в БД
    for video_name in video_files:
        if video_name not in existing_names:
            video_path = str(VIDEO_FOLDER / video_name)
            new_video = Video(name=video_name, path=video_path)
            session.add(new_video)
            print(f"Добавлено: {video_name}")

    # Сохраняем изменения
    await session.commit()


async def main():
    # Получаем сессию для работы с БД
    session_generator = get_async_session()  # Получаем генератор
    session = await anext(session_generator)  # Извлекаем сессию
    try:
        await load_videos_to_db(session)
    finally:
        await session.close()


if __name__ == "__main__":
    asyncio.run(main())

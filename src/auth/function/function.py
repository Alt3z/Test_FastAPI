import re

from sqlalchemy import select, insert

from passlib.context import CryptContext

from src.database import async_session_maker

from src.auth.models import Registration
from src.auth.schemas import RegUser, LogUser

from src.config import ALGORITHM_HASH_PASSWORD


# Проверка на существующего пользователя по user_name
async def find_existing_user(user_name: str):
    async with async_session_maker() as session:
        stmt = select(Registration).where(Registration.user_name == user_name)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

async def find_errors(reg: RegUser) -> dict:
    errors = {}

    # Проверка имени пользователя
    if not re.match(r'^[a-zA-Z0-9-_]+$', reg.user_name):
        errors["user_name"] = "Имя пользователя может содержать только буквы латинского алфавита, цифры, - и _"
    elif len(reg.user_name) > 25:
        errors["user_name"] = "Имя пользователя слишком длинное"

    # Проверка на существующего пользователя
    if not errors:
        existing_user = await find_existing_user(reg.user_name.lower())
        if existing_user:
            errors["user_name"] = "Пользователь с таким именем уже существует"

    return errors

pwd_context = CryptContext(schemes=[ALGORITHM_HASH_PASSWORD], deprecated="auto")

async def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def add_new_user_in_db(reg: RegUser):
    async with async_session_maker() as session:
        stmt = insert(Registration).values(
            user_name=reg.user_name,
            hashed_password=reg.password
        )
        await session.execute(stmt)
        await session.commit()

async def check_user(user_name: str, password: str):
    async with async_session_maker() as session:
        # Формируем условие поиска по email или телефону
        stmt = select(Registration).where(Registration.user_name == user_name)

        result = await session.execute(stmt)
        user = result.scalar_one_or_none()  # Возвращает первого пользователя или None, если не найден

        if user and pwd_context.verify(password, user.hashed_password):
            return user

        return None
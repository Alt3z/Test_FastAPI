from fastapi import APIRouter, HTTPException, Body, Request, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from datetime import datetime, timedelta
import jwt

from src.auth.schemas import RegUser, LogUser

from src.auth.function.function import find_errors, hash_password, add_new_user_in_db, check_user

from src.config import SECRET_KEY, ALGORITHM


router = APIRouter(
    prefix="/auth",
    tags=["Auth JWT"],
)

def create_jwt_token(user_name: str, time: int) -> str:
    expiration_time = datetime.now() + timedelta(seconds=time)  # Время действия токена
    payload = {
        "sub": user_name,  # Идентификатор пользователя
        "exp": expiration_time  # Время истечения токена
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def set_access_token_cookie(response: JSONResponse, token: str, time: int):
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        max_age=time,
        secure=True,
        httponly=True,
        samesite="Strict"
    )

def delete_access_token_cookie(response: JSONResponse):
    response.delete_cookie("access_token")

# Зависимость для получения токена из куки
def get_token_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not logged in or invalid token")
    return token

def verify_token(token: str) -> dict:
    try:
        if token.startswith("Bearer "):
            token = token[7:]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

def get_current_user(token: Annotated[str, Depends(get_token_from_cookie)]) -> str:
    payload = verify_token(token)
    user_name = payload.get("sub")
    if user_name is None:
        raise HTTPException(status_code=400, detail="Token does not contain user information")
    return user_name

@router.post("/reg")
async def user_reg(reg: Annotated[RegUser, Body()]):

    errors = await find_errors(reg)
    if errors:
        raise HTTPException(status_code=400, detail=errors)

    reg.password = await hash_password(reg.password)

    await add_new_user_in_db(reg)

    response = {"user_name": reg.user_name}
    return JSONResponse(status_code=200, content=response)


@router.post("/log")
async def user_log(log: Annotated[LogUser, Body()]):

    if not await check_user(log.user_name, log.password):
        raise HTTPException(status_code=400, detail="User is not registered or password is incorrect")

    time = 3600 # 1 час в секундах
    token = create_jwt_token(log.user_name, time)

    response = JSONResponse(
        status_code=200,
        content={"message": f"User {log.user_name} logged in successfully"}
    )

    set_access_token_cookie(response, token, time)

    return response

@router.get("/check_user")
async def user_check(user_name: Annotated[str, Depends(get_current_user)]):

    response = JSONResponse(
        status_code=200,
        content={"message": f"User in system", "user_name": user_name}
    )

    return response

@router.get("/logout")
async def user_logout(token: Annotated[str, Depends(get_token_from_cookie)]):

    response = JSONResponse(
        status_code=200,
        content={"message": f"User logout in successfully"}
    )
    delete_access_token_cookie(response)

    return response
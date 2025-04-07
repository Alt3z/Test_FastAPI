from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from typing import Annotated

from src.auth.models import Registration
from src.auth.schemas import RegUser

from src.auth.function.function import find_errors, find_existing_user, hash_password, add_new_user_in_db


router = APIRouter(
    prefix="/auth",
    tags=["Auth JWT"],
)

@router.post("/reg")
async def user_reg(reg: Annotated[RegUser, Body()]):

    errors = await find_errors(reg)
    if errors:
        raise HTTPException(status_code=400, detail=errors)

    reg.password = await hash_password(reg.password)

    await add_new_user_in_db(reg)

    response = {"user_name": reg.user_name}
    return JSONResponse(status_code=200, content=response)

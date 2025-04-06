from typing import Annotated
from fastapi import APIRouter, HTTPException, File, UploadFile, Form

from src.cryptography.hash.models import HashMethod, hash_functions


router = APIRouter(
    prefix="/cryptography",
    tags=["Сryptography"],
)

async def validate_input(text: str | None, upload_file: UploadFile | None):
    if text and upload_file:
        raise HTTPException(status_code=400, detail="Hash error: must be either text or file")
    if not text and not upload_file:
        raise HTTPException(status_code=400, detail="Hash error: no information provided for hashing")

@router.post("/hash/")
async def generate_hash(method: Annotated[HashMethod, Form(description="Метод хэширования")],
                    text: Annotated[str | None, Form(description="Текст для получения хэша")] = None,
                    upload_file: Annotated[UploadFile | None, File(description="Файл для получения хэша")] = None):
    try:
        await validate_input(text, upload_file)

        file_name = None
        content = text

        if upload_file:
            file_name = upload_file.filename
            content = await upload_file.read()

        # Если content - строка, кодируем её в байты
        if isinstance(content, str):
            content = content.encode()

        hash = hash_functions[method](content).hexdigest()

        if file_name:
            return {
                "File_name": file_name,
                "File_hash": hash
            }
        else:
            return {"Hash": hash }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hash error: {str(e)}")
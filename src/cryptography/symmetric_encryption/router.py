from datetime import datetime
from typing import Annotated
from fastapi import APIRouter,HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse

from pathlib import Path

from src.cryptography.symmetric_encryption.schemas import SymEncMethod
from src.cryptography.symmetric_encryption.my_crypters.aes.aes import aes128
from src.kafka_manager import KafkaManager
from src.config import ENC_FILE_PATH, KAFKA_SERVERS


router = APIRouter(
    prefix="/cryptography_symmetric_encryption",
    tags=["Сryptography"],
)

kafka_manager = KafkaManager(bootstrap_servers=KAFKA_SERVERS)

enc_param = {
    "aes128": {"key_len": 16, "iv_len": 16}
}

enc_functions = {
    "aes128": aes128
}


@router.post("/encrypt/")
async def encrypt_text(method: Annotated[SymEncMethod, Form(description="Метод шифрования")],
                       key: Annotated[str, Form(description="Ключ")],
                       iv: Annotated[str | None, Form(description="Вектор инициализации")] = None,
                       text: Annotated[str | None, Form(description="Текст для шифрования")] = None,
                       upload_file: Annotated[UploadFile | None, File(description="Файл для шифрования")] = None):
    try:
        if text is not None and upload_file is not None:
            raise HTTPException(status_code=400, detail=f"Encryption error: must be either text or file")
        if text is None and upload_file is None:
            raise HTTPException(status_code=400, detail=f"Encryption error: no information provided for encryption")

        if len(key) != enc_param[method]["key_len"]:
            raise HTTPException(status_code=400,
                                detail=f"The length of the key must be {enc_param[method]["key_len"]}")

        if iv is not None:
            if len(iv) != enc_param[method]["iv_len"]:
                raise HTTPException(status_code=400,
                                    detail=f"The length of the vector must be {enc_param[method]["iv_len"]}")

        file_name = None
        content = text

        if upload_file is not None:
            file_name = upload_file.filename
            extension = Path(file_name).suffix
            if extension != ".txt":
                raise HTTPException(status_code=400,
                                    detail=f"Only txt is supported")
            content = await upload_file.read()

        enc_content = enc_functions[method]("enc", content, key, iv)

        if file_name:
            ENCRYPTED_DIR = Path(ENC_FILE_PATH)
            new_filename = f"enc_{file_name}"
            file_path = ENCRYPTED_DIR / new_filename

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(enc_content)

            return FileResponse(
                path=file_path,
                media_type="application/octet-stream",
                filename=file_path.name,
                headers={"Content-Disposition": f"attachment; filename={file_path.name}"}
            )

        # Отправка события в Kafka
        event = {
            "event": "ENC_TEXT",
            "details": {
                "text_length": len(enc_content),
                "timestamp": datetime.now().isoformat()
            }
        }
        await kafka_manager.send_event("enc_log", event)

        return {"enc_text": enc_content}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Encryption error: {str(e)}")


@router.post("/decrypt/")
async def decrypt_text(method: Annotated[SymEncMethod, Form(description="Метод дешифрования")],
                       key: Annotated[str, Form(description="Ключ")],
                       iv: Annotated[str | None, Form(description="Вектор инициализации")] = None,
                       text: Annotated[str | None, Form(description="Текст для дешифрования")] = None,
                       upload_file: Annotated[UploadFile | None, File(description="Файл для дешифрования")] = None):
    try:
        if text is not None and upload_file is not None:
            raise HTTPException(status_code=400, detail=f"Encryption error: must be either text or file")
        if text is None and upload_file is None:
            raise HTTPException(status_code=400, detail=f"Encryption error: no information provided for encryption")


        if len(key) != enc_param[method]["key_len"]:
            raise HTTPException(status_code=400,
                                detail=f"The length of the key must be {enc_param[method]["key_len"]}")

        if iv is not None:
            if len(iv) != enc_param[method]["iv_len"]:
                raise HTTPException(status_code=400,
                                    detail=f"The length of the vector must be {enc_param[method]["iv_len"]}")

        file_name = None
        content = text

        if upload_file is not None:
            file_name = upload_file.filename
            extension = Path(file_name).suffix
            if extension != ".txt":
                raise HTTPException(status_code=400,
                                    detail=f"Only txt is supported")

            file_bytes = await upload_file.read()
            try:
                content = file_bytes.decode("utf-8")
            except UnicodeDecodeError:
                raise HTTPException(status_code=400, detail="Файл не является корректной hex-строкой")

        enc_content = enc_functions[method]("dec", content, key, iv)

        if file_name:
            ENCRYPTED_DIR = Path(ENC_FILE_PATH)
            new_filename = f"dec_{file_name}"
            file_path = ENCRYPTED_DIR / new_filename

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(enc_content)

            return FileResponse(
                path=file_path,
                media_type="application/octet-stream",
                filename=file_path.name,
                headers={"Content-Disposition": f"attachment; filename={file_path.name}"}
            )

        return {"dec_text": enc_content}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Encryption error: {str(e)}")


# 1234567812345678
from enum import Enum
from pydantic import BaseModel, Field


# Доступные методы шифрования
class SymEncMethod(str, Enum):
    aes128 = "aes128"


class CryptographySymEnc(BaseModel):
    method: SymEncMethod
    key: str = Field(min_length=8, max_length=256, description="Ключ шифрования")
    iv: str = Field(default=None, description="Инициализационный вектор. Если он задан, то шифрования производится в "
                                              "режиме сцепления блоков")

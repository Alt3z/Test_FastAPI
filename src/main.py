from fastapi import FastAPI

from src.cryptography.hash.router import router as router_cryptography_hash
from src.cryptography.symmetric_encryption.router import router as router_cryptography_symmetric_encryption

from src.video.router import router as router_video

app = FastAPI(
    title="Afina",
    description="Шифрование, хэщ, видео, стороннее API",
    version="0.0.1"
)

#app.include_router(router_cryptography_symmetric_encryption)
#app.include_router(router_cryptography_hash)

#app.include_router(router_video)


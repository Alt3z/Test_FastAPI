import io
from unittest.mock import AsyncMock, patch
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.mark.asyncio
async def test_generate_hash_with_text():
    with patch("src.cryptography.hash.router.kafka_manager.send_event", new_callable=AsyncMock) as mock_kafka:
        mock_kafka.return_value = None  # ничего не делает

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            data = {
                "method": "sha256",
                "text": "test text"
            }
            response = await ac.post("/cryptography/hash/", data=data)

            assert response.status_code == 200

            response_json = response.json()
            assert "Hash" in response_json

            hash_value = response_json["Hash"]
            assert len(hash_value) == 64

@pytest.mark.asyncio
async def test_generate_hash_with_file():
    with patch("src.cryptography.hash.router.kafka_manager.send_event", new_callable=AsyncMock) as mock_kafka:
        mock_kafka.return_value = None

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            file_content = b"test file content"
            files = {
                "method": (None, "sha256"),
                "upload_file": ("test_file.txt", file_content, "text/plain"),
            }

            response = await ac.post("/cryptography/hash/", files=files)

            assert response.status_code == 200

            response_json = response.json()
            assert "File_hash" in response_json
            assert "File_name" in response_json

            file_hash = response_json["File_hash"]
            file_name = response_json["File_name"]

            assert file_name == "test_file.txt"
            assert len(file_hash) == 64
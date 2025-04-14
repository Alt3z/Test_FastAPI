import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from src.main import app


@pytest.mark.asyncio
async def test_encrypt_text_aes128():
    with patch("src.cryptography.symmetric_encryption.router.kafka_manager.send_event", new_callable=AsyncMock) as mock_kafka:
        mock_kafka.return_value = None

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            data = {
                "method": "aes128",
                "key": "1234567812345678",
                "iv": "1234567812345678",
                "text": "Test secret message"
            }
            response = await ac.post("/cryptography_symmetric_encryption/encrypt/", data=data)

        assert response.status_code == 200
        assert "enc_text" in response.json()
        mock_kafka.assert_called_once()

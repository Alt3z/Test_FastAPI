from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def aes128_enc(data: bytes | str, key: str, iv: str | None = None) -> str:
    # Приводим данные к байтам
    if isinstance(data, str):
        data = data.encode('utf-8')

    key_bytes = key.encode('utf-8')

    # Паддинг (AES блок — 16 байт)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Выбор режима
    if iv:
        iv_bytes = iv.encode('utf-8')
        mode = modes.CBC(iv_bytes)
    else:
        mode = modes.ECB()

    cipher = Cipher(algorithms.AES(key_bytes), mode, backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    # Возвращаем в hex-строке (можно base64, если нужно)
    return encrypted.hex()

def aes128_dec(data: str, key: str, iv: str | None = None) -> str:
    # Преобразуем hex-строку обратно в байты
    encrypted_bytes = bytes.fromhex(data)
    key_bytes = key.encode('utf-8')

    # Выбор режима
    if iv:
        iv_bytes = iv.encode('utf-8')
        mode = modes.CBC(iv_bytes)
    else:
        mode = modes.ECB()

    cipher = Cipher(algorithms.AES(key_bytes), mode, backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(encrypted_bytes) + decryptor.finalize()

    # Убираем паддинг
    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

    # Возвращаем как строку
    return decrypted.decode('utf-8')

def aes128(mode: str, data: str, key: str, iv: str | None = None):
    if mode == "enc":
        return aes128_enc(data, key, iv)
    return aes128_dec(data, key, iv)
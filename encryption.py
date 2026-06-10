# encryption.py
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidTag

NONCE_SIZE = 12
SALT_SIZE = 16
PBKDF2_ITERATIONS = 600000  # OWASP 2023 рекомендация для SHA-256


# --- Старые функции (для обратной совместимости) ---
def generate_key() -> bytes:
    return os.urandom(32)


def encrypt_bytes(data: bytes, key: bytes) -> bytes:
    if len(key) != 32: raise ValueError("Ключ должен быть 32 байта.")
    if not data: raise ValueError("Данные не могут быть пустыми.")
    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE)
    return nonce + aesgcm.encrypt(nonce, data, None)


def decrypt_bytes(encrypted_data: bytes, key: bytes) -> bytes:
    if len(key) != 32: raise ValueError("Ключ должен быть 32 байта.")
    if len(encrypted_data) < NONCE_SIZE + 16: raise ValueError("Некорректный размер данных.")
    aesgcm = AESGCM(key)
    nonce, ciphertext = encrypted_data[:NONCE_SIZE], encrypted_data[NONCE_SIZE:]
    try:
        return aesgcm.decrypt(nonce, ciphertext, None)
    except InvalidTag:
        raise ValueError("Неверный ключ или повреждённые данные.")


# --- Новые функции для работы с ПАРОЛЕМ ---
def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=PBKDF2_ITERATIONS)
    return kdf.derive(password.encode("utf-8"))


def encrypt_with_password(data: bytes, password: str) -> bytes:
    """Шифрует данные паролем. Возвращает: salt(16) + nonce(12) + ciphertext+tag"""
    if not password: raise ValueError("Пароль не может быть пустым.")
    salt = os.urandom(SALT_SIZE)
    key = _derive_key(password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE)
    ciphertext = aesgcm.encrypt(nonce, data, None)
    return salt + nonce + ciphertext


def decrypt_with_password(encrypted_data: bytes, password: str) -> bytes:
    """Расшифровывает данные паролем. Извлекает соль из начала потока."""
    if not password: raise ValueError("Пароль не может быть пустым.")
    min_len = SALT_SIZE + NONCE_SIZE + 16
    if len(encrypted_data) < min_len: raise ValueError("Некорректный размер зашифрованных данных.")

    salt = encrypted_data[:SALT_SIZE]
    nonce = encrypted_data[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
    ciphertext = encrypted_data[SALT_SIZE + NONCE_SIZE:]

    key = _derive_key(password, salt)
    try:
        return AESGCM(key).decrypt(nonce, ciphertext, None)
    except InvalidTag:
        raise ValueError("❌ Неверный пароль или повреждённые данные.")
import hashlib
import hmac
import time


def check_telegram_auth(data: dict, BOT_TOKEN: str) -> bool:
    """Проверка подлинности данных от Telegram"""
    auth_data = data.copy()
    hash_ = auth_data.pop("hash")

    # Сортируем ключи и собираем строку
    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(auth_data.items())])

    # Вычисляем HMAC-SHA256
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if hmac_hash != hash_:
        return False

    # Проверка свежести (1 день)
    if time.time() - int(auth_data["auth_date"]) > 86400:
        return False

    return True
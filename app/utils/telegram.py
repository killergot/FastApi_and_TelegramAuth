import hashlib
import hmac
import time


def check_telegram_auth(data: dict, bot_token: str) -> bool:
    """
    Проверка данных от Telegram Login.
    data: словарь с Pydantic (telegram_id вместо id)
    """
    # Telegram использует ключ 'id', поэтому нужно вернуть его
    auth_data = data.copy()
    auth_data["id"] = str(auth_data.pop("telegram_id"))

    hash_ = auth_data.pop("hash")

    # Сортировка по ключам
    data_check_arr = [f"{k}={v}" for k, v in sorted(auth_data.items())]
    data_check_string = "\n".join(data_check_arr)

    # secret key
    secret_key = hashlib.sha256(bot_token.encode()).digest()

    # HMAC
    hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    # сравнение
    if not hmac.compare_digest(hmac_hash, hash_):
        return False

    # проверка свежести (1 день)
    if time.time() - int(auth_data["auth_date"]) > 86400:
        return False

    return True
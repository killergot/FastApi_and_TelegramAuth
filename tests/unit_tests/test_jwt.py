from app.core.security import (create_access_token, decode_access_token,
                               create_refresh_token,decode_refresh_token)

def test_create_access_token():
    a = create_access_token(1, 123123, 1)
    assert decode_access_token(a)['id'] == 1
    assert decode_access_token(a)['telegram_id'] == 123123
    assert decode_access_token(a)['role'] == 1

def test_create_refresh_token():
    a = create_refresh_token(1)
    assert decode_refresh_token(a)['sub'] == 1
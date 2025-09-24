from app.utils.hash import get_hash

def test_get_hash_consistency():
    data = "test_data"
    hash1 = get_hash(data)
    hash2 = get_hash(data)
    assert hash1 == hash2
    assert isinstance(hash1, str)
    assert len(hash1) == 64  # sha256 hex digest length

def test_get_hash_different_inputs():
    data1 = "data1"
    data2 = "data2"
    assert get_hash(data1) != get_hash(data2)
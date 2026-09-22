import time

from app.utils import cache


def test_set_and_get_roundtrip():
    cache.set("test:cache:roundtrip", {"a": 1}, ttl=30)

    assert cache.get("test:cache:roundtrip") == {"a": 1}

    cache.invalidate("test:cache:roundtrip")


def test_get_missing_key_returns_none():
    assert cache.get("test:cache:missing") is None


def test_invalidate_deletes_key():
    cache.set("test:cache:to_delete", "value", ttl=30)

    cache.invalidate("test:cache:to_delete")

    assert cache.get("test:cache:to_delete") is None


def test_invalidate_pattern_deletes_matching_keys():
    cache.set("test:cache:list:1", "a", ttl=30)
    cache.set("test:cache:list:2", "b", ttl=30)

    cache.invalidate("test:cache:list:*")

    assert cache.get("test:cache:list:1") is None
    assert cache.get("test:cache:list:2") is None


def test_ttl_expires_key():
    cache.set("test:cache:ttl", "value", ttl=1)

    assert cache.get("test:cache:ttl") == "value"

    time.sleep(1.5)

    assert cache.get("test:cache:ttl") is None

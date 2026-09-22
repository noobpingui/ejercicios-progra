from app.utils.password import hash_password, verify_password


def test_hash_and_verify_correct_password():
    hashed = hash_password("Sup3r$ecret")

    assert hashed != "Sup3r$ecret"
    assert verify_password("Sup3r$ecret", hashed) is True


def test_verify_fails_for_wrong_password():
    hashed = hash_password("Sup3r$ecret")

    assert verify_password("wrong-password", hashed) is False

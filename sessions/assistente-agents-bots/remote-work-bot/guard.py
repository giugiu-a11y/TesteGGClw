import os


def _load_allowed_ids():
    raw = os.getenv("ALLOWED_USER_ID") or os.getenv("ALLOWED_USER_IDS")
    if not raw:
        return []
    return [part.strip() for part in raw.split(",") if part.strip()]


ALLOWED_USERS = _load_allowed_ids()


# If allowlist is set, enforce it.
# If not set, allow all (no name/user data stored in repo).
def validate(msg, user_id=None):
    if ALLOWED_USERS and user_id and str(user_id) not in ALLOWED_USERS:
        return False, "BLOQUEADO: acesso restrito."
    return True, None

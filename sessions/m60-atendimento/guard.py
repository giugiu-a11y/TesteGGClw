BLOCKED = ["jesus", "tweet", "twitter", "tiktok", "viral", "sincero"]

def validate(msg):
    msg_lower = msg.lower()
    for term in BLOCKED:
        if term in msg_lower:
            return False, f"BLOQUEADO: termo '{term}' não pertence a esta session"
    return True, None

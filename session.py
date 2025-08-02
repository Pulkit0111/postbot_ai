user_sessions = {}

def get_session(user_id):
    return user_sessions.setdefault(user_id, {
        "topic": None,
        "summary": None,
        "draft": None
    })

def clear_session(user_id):
    user_sessions.pop(user_id, None)

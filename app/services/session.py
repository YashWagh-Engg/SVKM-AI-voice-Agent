from uuid import uuid4


sessions = {}


def create_session():
    session_id = str(uuid4())

    sessions[session_id] = {
        "messages": []
    }

    return session_id


def add_message(session_id, role, content):
    if session_id not in sessions:
        return False

    sessions[session_id]["messages"].append({
        "role": role,
        "content": content
    })

    return True


def get_session(session_id):
    return sessions.get(session_id)
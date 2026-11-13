from fastapi import Request, HTTPException

class NotAuthenticated(Exception):

    pass

def get_current_user(request: Request):

    user_id = request.session.get("user_id")

    if not user_id:
        raise NotAuthenticated()
    else:
        return user_id
from fastapi import Request

from fastapi import HTTPException

from profile.managers.managers import ProfileManager
from profile.schemas import GetProfile


class ProfileLogic:

    @staticmethod
    def get_user(request: Request) -> GetProfile:
        if not hasattr(request.state, "user"):
            raise HTTPException(status_code=401, detail="User not authenticated")
        usr = request.state.user
        schema = GetProfile(profile_id=usr.get("user_id"))
        return schema
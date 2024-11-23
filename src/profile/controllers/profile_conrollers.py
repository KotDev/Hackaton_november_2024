from http.client import responses

from fastapi import APIRouter, Response
from fastapi.params import Depends
from pydantic.v1.schema import schema

from profile.logic.profile_logic import ProfileLogic
from profile.managers.managers import ProfileManager
from profile.schemas import GetProfile, ProfileSchema, ResponseProfileSchema, BusinessFormSchema

manager = ProfileManager()

profile_logic = ProfileLogic()
profile_router = APIRouter(prefix="/profile", tags=["Profiles"])

@profile_router.get("/me")
async def get_me_profile(user: GetProfile = Depends(profile_logic.get_user)):
    profile = await manager.get_full_data_profile(profile_id=user.profile_id)
    profile = profile.scalars().first()

    if not profile:
        return Response(status_code=404, content="Profile not found")

    profile_data = ProfileSchema.model_validate(profile)
    business_forms = [
        BusinessFormSchema.model_validate(bf) for bf in profile.buisness_forms
    ]
    response = ResponseProfileSchema(
        profile_id=profile.profile_id,
        email=profile.user.email,
        profile=profile_data,
        business_forms=business_forms,
    )
    return response


@profile_router.patch("/me")
async def patch_me_profile(schema_profile: ProfileSchema, user: GetProfile = Depends(profile_logic.get_user)):
    update_data = schema_profile.model_dump(exclude_none=True)
    await manager.update_profile(user.profile_id, update_data)
    return Response(status_code=200, content={"detail": "Update profile successful"})


@profile_router.post("/new_profile", status_code=201)
async def create_profile(user: GetProfile = Depends(profile_logic.get_user)):
    profile = await manager.get_profile(user.profile_id)
    profile = profile.scalars().first()
    if profile:
        return Response(status_code=409, content="Profile has already been created")

    new_profile = await manager.add_profile(user.profile_id, schema=ProfileSchema())
    return ProfileSchema.model_validate(new_profile).model_dump()




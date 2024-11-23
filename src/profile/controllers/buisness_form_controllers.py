from fastapi import APIRouter

from profile.managers.managers import BusinessFormManager
from profile.schemas import BusinessFormSchema, UpdateBusinessFormSchema
from fastapi import APIRouter, Depends, Response
from profile.schemas import GetProfile
from profile.logic.profile_logic import ProfileLogic

business_form_router = APIRouter(prefix="/business_form", tags=["BusinessForm"])

@business_form_router.get("/business_form")
async def get_business_form(
    profile: GetProfile = Depends(ProfileLogic.get_user), manager: BusinessFormManager = Depends(BusinessFormManager)
):
    business_form = await manager.get_business_form(business_form_id=profile.profile_id)
    return BusinessFormSchema.model_validate(business_form)

@business_form_router.post("/business_form")
async def create_business_form(
    profile: GetProfile = Depends(ProfileLogic.get_user), manager: BusinessFormManager = Depends(BusinessFormManager)
):
    business_form = await manager.add_business_form(profile.profile_id)
    return BusinessFormSchema(business_id=business_form.business_id)

@business_form_router.patch("/business_form")
async def update_business_form(
    schema_data: UpdateBusinessFormSchema,
    manager: BusinessFormManager = Depends(BusinessFormManager),
    profile: GetProfile = Depends(ProfileLogic.get_user)
):
    update_data = schema_data.model_dump(exclude_none=True)
    await manager.update_business_form(business_id=profile.profile_id, update_data=update_data)
    return Response(status_code=200, content={"detail": "Update profile successful"})



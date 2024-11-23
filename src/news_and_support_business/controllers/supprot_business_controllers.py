from fastapi import APIRouter
from fastapi.params import Depends

from news_and_support_business.schemas import BusinessSupportTagSchema, CreateTagBusinessSupportSchema
from profile.controllers.buisness_form_controllers import business_form_router
from profile.logic.profile_logic import ProfileLogic
from profile.schemas import ResponseProfileSchema, GetProfile
from profile.managers.managers import BusinessFormManager
from news_and_support_business.manager.managers import BusinessSupportManager

router_support_business = APIRouter(prefix="/support", tags=["BusinessSupport"])


@router_support_business.post("/write_request_ml")
async def request_ml(profile: GetProfile = Depends(ProfileLogic.get_user),
                     manager: BusinessFormManager = Depends(BusinessFormManager)) -> BusinessSupportTagSchema:
    business_form = await manager.get_business_form(profile_id=profile.profile_id)
    pass


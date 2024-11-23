from fastapi import APIRouter
from ml.schemas import BusinessSupportTagSchema, CreateTagBusinessSupportSchema
from profile.schemas import ResponseProfileSchema

router_support_business = APIRouter(prefix="/business_support", tags=["BusinessSupport"])


@router_support_business.post("/write_request_ml")
async def request_ml(schema: ResponseProfileSchema=ResponseProfileSchema) -> BusinessSupportTagSchema:
    pass


@router_support_business.get("/all_business_support")
async def get_all_business_support() -> BusinessSupportTagSchema:
    pass


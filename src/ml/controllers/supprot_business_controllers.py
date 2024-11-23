from fastapi import APIRouter
from ml.schemas import BusinessSupportTagSchema


router_support_business = APIRouter(prefix="/business_support", tags=["BusinessSupport"])


@router_support_business.post("/write_request_ml")
async def request_ml() -> BusinessSupportTagSchema:
    pass


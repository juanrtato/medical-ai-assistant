from app.models.triage import TriageRequest, TriageResponse
from app.services.triage_service import TriageService
from fastapi import APIRouter

router = APIRouter()
service = TriageService()


@router.post("", response_model=TriageResponse)
def triage(request: TriageRequest):
    return service.classify(request)

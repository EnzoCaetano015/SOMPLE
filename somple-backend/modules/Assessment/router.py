from fastapi import APIRouter, Depends

from core.authorization import AuthenticatedUser, require_authenticated_user
from modules.Assessment.schemas import AssessmentDetailResponse
from modules.Assessment.service import get_assessment_detail

router = APIRouter(prefix="/assessments", tags=["Risk Assessments"])


@router.get("/{assessment_id}", response_model=AssessmentDetailResponse, summary="Assessment detail")
def assessment_detail(
    assessment_id: int,
    _: AuthenticatedUser = Depends(require_authenticated_user),
) -> AssessmentDetailResponse:
    return get_assessment_detail(assessment_id)

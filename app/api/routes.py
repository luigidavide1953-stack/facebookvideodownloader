from fastapi import APIRouter, HTTPException, Query
from ..services.resolver import resolver
from ..services.models import ExtractionResult, ErrorResponse
from typing import Union

router = APIRouter()

@router.get("/extract", response_model=Union[ExtractionResult, ErrorResponse])
async def extract_video(url: str = Query(..., description="The Facebook video URL to extract")):
    result = await resolver.resolve(url)
    if isinstance(result, ErrorResponse):
        raise HTTPException(status_code=400, detail=result.model_dump())
    return result

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

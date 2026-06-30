from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any

class VideoMetadata(BaseModel):
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    duration: Optional[str] = None
    uploader: Optional[str] = None
    views: Optional[int] = None
    likes: Optional[int] = None
    upload_date: Optional[str] = None

class VideoFormat(BaseModel):
    url: str
    quality: str
    format: str
    size: Optional[int] = None

class ExtractionResult(BaseModel):
    url: str
    metadata: VideoMetadata
    formats: List[VideoFormat]
    raw_data: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

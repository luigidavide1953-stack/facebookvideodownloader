from .extractor import fb_extractor
from .models import ExtractionResult, ErrorResponse
from typing import Union

class Resolver:
    async def resolve(self, url: str) -> Union[ExtractionResult, ErrorResponse]:
        try:
            if not url or "facebook.com" not in url and "fb.watch" not in url:
                return ErrorResponse(error="Invalid URL", detail="Please provide a valid Facebook video URL.")
            
            result = await fb_extractor.extract(url)
            
            if not result.formats:
                return ErrorResponse(error="Extraction Failed", detail="Could not find any video formats for this URL.")
                
            return result
        except Exception as e:
            return ErrorResponse(error="Internal Server Error", detail=str(e))

resolver = Resolver()

import re
from typing import Optional, Dict, Any
from .playwright import playwright_service
from .parser import fb_parser
from .models import ExtractionResult, VideoMetadata, VideoFormat
from .cache import cache_service

class FBExtractor:
    def __init__(self):
        self.url_patterns = [
            r'facebook\.com/.*videos/(\d+)',
            r'facebook\.com/watch/\?v=(\d+)',
            r'facebook\.com/reel/(\d+)',
            r'fb\.watch/([\w-]+)'
        ]

    def extract_id(self, url: str) -> Optional[str]:
        for pattern in self.url_patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    async def extract(self, url: str) -> ExtractionResult:
        # Check cache first
        video_id = self.extract_id(url) or url
        cached = await cache_service.get(video_id)
        if cached:
            return ExtractionResult(**cached)

        # Use Playwright as fallback/primary for complex pages
        html_content = await playwright_service.get_page_content(url)
        
        metadata_raw = fb_parser.extract_metadata(html_content)
        video_urls = fb_parser.extract_video_urls(html_content)
        
        metadata = VideoMetadata(
            id=video_id,
            title=metadata_raw.get("title"),
            description=metadata_raw.get("description"),
            thumbnail=metadata_raw.get("thumbnail"),
            duration=metadata_raw.get("duration"),
            upload_date=metadata_raw.get("upload_date")
        )
        
        formats = [
            VideoFormat(url=v["url"], quality=v["quality"], format="mp4")
            for v in video_urls
        ]
        
        # If no formats found via simple parsing, this is where GraphQL logic would go
        
        result = ExtractionResult(
            url=url,
            metadata=metadata,
            formats=formats,
            raw_data={"html_length": len(html_content)}
        )
        
        # Save to cache
        await cache_service.set(video_id, result.model_dump())
        
        return result

fb_extractor = FBExtractor()

from bs4 import BeautifulSoup
import re
import json
from typing import Dict, Any, Optional

class FBParser:
    def extract_metadata(self, html_content: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html_content, "html.parser")
        metadata = {}
        
        # Try to find JSON-LD or script tags containing video data
        scripts = soup.find_all("script", type="application/ld+json")
        for script in scripts:
            try:
                data = json.loads(script.string)
                if data.get("@type") == "VideoObject":
                    metadata["title"] = data.get("name")
                    metadata["description"] = data.get("description")
                    metadata["thumbnail"] = data.get("thumbnailUrl")
                    metadata["duration"] = data.get("duration")
                    metadata["upload_date"] = data.get("uploadDate")
                    break
            except:
                continue
        
        # Fallback to meta tags
        if not metadata.get("title"):
            title_tag = soup.find("meta", property="og:title")
            metadata["title"] = title_tag["content"] if title_tag else "Facebook Video"
            
        if not metadata.get("thumbnail"):
            thumb_tag = soup.find("meta", property="og:image")
            metadata["thumbnail"] = thumb_tag["content"] if thumb_tag else None
            
        return metadata

    def extract_video_urls(self, html_content: str) -> list:
        # Simple regex to find video URLs in the page source
        # This is a basic implementation; real-world FB extraction often requires GraphQL or specific script parsing
        urls = []
        sd_match = re.search(r'browser_native_sd_url":"([^"]+)"', html_content)
        hd_match = re.search(r'browser_native_hd_url":"([^"]+)"', html_content)
        
        if hd_match:
            urls.append({"quality": "HD", "url": hd_match.group(1).replace("\\/", "/")})
        if sd_match:
            urls.append({"quality": "SD", "url": sd_match.group(1).replace("\\/", "/")})
            
        return urls

fb_parser = FBParser()

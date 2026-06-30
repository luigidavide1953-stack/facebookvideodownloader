import pytest
from unittest.mock import AsyncMock, patch
from app.services.extractor import FBExtractor
from app.services.models import ExtractionResult, VideoMetadata, VideoFormat

@pytest.fixture
def fb_extractor():
    return FBExtractor()

@pytest.mark.asyncio
async def test_extract_id(fb_extractor):
    assert fb_extractor.extract_id("https://www.facebook.com/user/videos/1234567890") == "1234567890"
    assert fb_extractor.extract_id("https://www.facebook.com/watch/?v=1234567890") == "1234567890"
    assert fb_extractor.extract_id("https://www.facebook.com/reel/1234567890") == "1234567890"
    assert fb_extractor.extract_id("https://fb.watch/abcdefg/") == "abcdefg"
    assert fb_extractor.extract_id("https://example.com") is None

@pytest.mark.asyncio
async def test_extract_success(fb_extractor):
    mock_html_content = """
    <html>
        <head>
            <meta property="og:title" content="Test Video Title"/>
            <meta property="og:image" content="http://example.com/thumbnail.jpg"/>
            <script type="application/ld+json">{"@type": "VideoObject", "name": "JSON-LD Title"}</script>
        </head>
        <body>
            <script>var data = {browser_native_hd_url: \"http://example.com/hd.mp4\", browser_native_sd_url: \"http://example.com/sd.mp4\"};</script>
        </body>
    </html>
    """
    
    with patch("app.services.playwright.playwright_service.get_page_content", new_callable=AsyncMock) as mock_get_content,
         patch("app.services.cache.cache_service.get", new_callable=AsyncMock) as mock_cache_get,
         patch("app.services.cache.cache_service.set", new_callable=AsyncMock) as mock_cache_set:
        
        mock_cache_get.return_value = None
        mock_get_content.return_value = mock_html_content

        result = await fb_extractor.extract("https://www.facebook.com/watch/?v=1234567890")

        assert isinstance(result, ExtractionResult)
        assert result.metadata.title == "JSON-LD Title"
        assert result.metadata.thumbnail == "http://example.com/thumbnail.jpg"
        assert len(result.formats) == 2
        assert any(f.quality == "HD" and f.url == "http://example.com/hd.mp4" for f in result.formats)
        assert any(f.quality == "SD" and f.url == "http://example.com/sd.mp4" for f in result.formats)
        mock_cache_set.assert_called_once()

@pytest.mark.asyncio
async def test_extract_no_video_formats(fb_extractor):
    mock_html_content = """
    <html>
        <head>
            <meta property="og:title" content="Test Video Title"/>
        </head>
        <body>
            <!-- No video URLs in script tags -->
        </body>
    </html>
    """
    
    with patch("app.services.playwright.playwright_service.get_page_content", new_callable=AsyncMock) as mock_get_content,
         patch("app.services.cache.cache_service.get", new_callable=AsyncMock) as mock_cache_get,
         patch("app.services.cache.cache_service.set", new_callable=AsyncMock) as mock_cache_set:
        
        mock_cache_get.return_value = None
        mock_get_content.return_value = mock_html_content

        result = await fb_extractor.extract("https://www.facebook.com/watch/?v=1234567890")

        assert isinstance(result, ExtractionResult)
        assert result.metadata.title == "Test Video Title"
        assert len(result.formats) == 0
        mock_cache_set.assert_called_once()

@pytest.mark.asyncio
async def test_extract_from_cache(fb_extractor):
    cached_data = {
        "url": "https://www.facebook.com/watch/?v=1234567890",
        "metadata": {"id": "1234567890", "title": "Cached Title"},
        "formats": [{
            "url": "http://example.com/cached.mp4",
            "quality": "HD",
            "format": "mp4"
        }]
    }
    
    with patch("app.services.cache.cache_service.get", new_callable=AsyncMock) as mock_cache_get,
         patch("app.services.playwright.playwright_service.get_page_content", new_callable=AsyncMock) as mock_get_content:
        
        mock_cache_get.return_value = cached_data

        result = await fb_extractor.extract("https://www.facebook.com/watch/?v=1234567890")

        assert isinstance(result, ExtractionResult)
        assert result.metadata.title == "Cached Title"
        assert len(result.formats) == 1
        assert result.formats[0].url == "http://example.com/cached.mp4"
        mock_cache_get.assert_called_once()
        mock_get_content.assert_not_called() # Should not call playwright if cached

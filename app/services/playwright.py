from playwright.async_api import async_playwright
import os
from .cookies import cookie_manager

class PlaywrightService:
    def __init__(self):
        self.headless = os.getenv("HEADLESS", "true").lower() == "true"

    async def get_page_content(self, url: str) -> str:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context()
            
            # Load cookies if available
            cookies = cookie_manager.load_cookies()
            if cookies:
                await context.add_cookies(cookies)
            
            page = await context.new_page()
            # Set a common user agent
            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
            })
            
            await page.goto(url, wait_until="networkidle")
            content = await page.content()
            
            # Optionally update cookies after page load
            # new_cookies = await context.cookies()
            # cookie_manager.save_cookies(new_cookies)
            
            await browser.close()
            return content

playwright_service = PlaywrightService()

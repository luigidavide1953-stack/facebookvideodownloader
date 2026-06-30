import json
import os
from typing import List, Dict

class CookieManager:
    def __init__(self, cookies_path: str = "cookies/facebook.txt"):
        self.cookies_path = cookies_path

    def load_cookies(self) -> List[Dict]:
        if not os.path.exists(self.cookies_path):
            return []
        
        try:
            with open(self.cookies_path, "r") as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except (json.JSONDecodeError, IOError):
            return []

    def save_cookies(self, cookies: List[Dict]):
        os.makedirs(os.path.dirname(self.cookies_path), exist_ok=True)
        with open(self.cookies_path, "w") as f:
            json.dump(cookies, f, indent=2)

cookie_manager = CookieManager()

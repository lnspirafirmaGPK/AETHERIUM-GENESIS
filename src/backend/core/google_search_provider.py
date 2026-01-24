import os
import requests
from typing import List, Dict, Optional

class SearchProvider:
    def search(self, query: str) -> List[Dict]:
        raise NotImplementedError

class GoogleSearchProvider(SearchProvider):
    def __init__(self, api_key: Optional[str] = None, cse_id: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        self.cse_id = cse_id or os.environ.get("GOOGLE_CSE_ID")

        if not self.api_key or not self.cse_id:
            print("Warning: Google Search API Key or CSE ID not found. Search will fail.")

    def search(self, query: str) -> List[Dict]:
        if not self.api_key or not self.cse_id:
            return []

        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.api_key,
            "cx": self.cse_id,
            "q": query
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json().get("items", [])
        except Exception as e:
            print(f"Google Search Error: {e}")
            return []

import os
import requests
import json
from typing import Dict

def fetch_salary_data(query: str, location: str) -> Dict:
    url = "https://google.serper.dev/search"
    headers = {
        'X-API-KEY': os.getenv('SERPER_API_KEY'),
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "q": f"salary {query} {location}",
        "location": "US",
        "type": "search",
        "engine": "google"
    })
    response = requests.post(url, headers=headers, data=payload)
    return response.json() if response.status_code == 200 else None

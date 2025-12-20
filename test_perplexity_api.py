import requests
import json
import os

api_key = os.getenv('PERPLEXITY_API_KEY')

response = requests.post(
    "https://api.perplexity.ai/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": "sonar-pro",
        "messages": [
            {
                "role": "user",
                "content": "Test: return JSON with status: ok"
            }
        ]
    }
)

print("Status:", response.status_code)
print("Response:", response.json())

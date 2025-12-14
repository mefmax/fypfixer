import requests
import json

api_key = "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"

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

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv('PERPLEXITY_API_KEY')

client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

# **ПРАВИЛЬНЫЙ способ с return_videos=true**
response = client.chat.completions.create(
    model="sonar-pro",
    messages=[{"role": "user", "content": "personal growth tips 2025 actionable habits mindset tools success stories"}],
    extra_body={  # ← КРИТИЧНО!
        "media_response": {
            "overrides": {
                "return_videos": True  # ← ЭТО КЛЮЧ!
            }
        }
    }
)

print(json.dumps(response.to_dict(), indent=2))

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv('PERPLEXITY_API_KEY')
if not API_KEY:
    print("❌ PERPLEXITY_API_KEY not found in .env")
    exit(1)

print(f"\n🔍 GENERATING IDEAL PROMPT FOR PERSONAL GROWTH TIKTOK VIDEOS\n")
print("=" * 80)

client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

# STAGE 1: Generate ideal prompt for our audience
stage1_prompt = """
You are a TikTok content strategist. 

Target Audience: 18-35 years old, seeking quality personal growth content, want to train their FYP algorithm with intentional consumption.

Pain: Tired of algorithm chaos, want curated, concrete, actionable content.

Task: Generate a concise TikTok search prompt that will find 10 BEST trending videos about "personal growth" that appeal to this audience. The videos should be:
- Actionable tips (not just motivation quotes)
- 30-60 seconds format (typical TikTok)
- High engagement (100k+ views, verified/popular creators)
- Recent (last 3 months)
- Mix of: habit hacks, mindset shifts, practical tools, success stories

Return ONLY the prompt text (no JSON, no explanation). Just the exact search prompt I should use with TikTok API or web search.
"""

print("📧 STAGE 1: Generating ideal prompt...\n")
response1 = client.chat.completions.create(
    model="sonar-pro",
    messages=[{"role": "user", "content": stage1_prompt}],
)

ideal_prompt = response1.choices[0].message.content
print(f"✅ IDEAL PROMPT GENERATED:\n\n{ideal_prompt}\n")
print("=" * 80)

# STAGE 2: Use that prompt to find videos
stage2_prompt = f"""
{ideal_prompt}

Now find 10 REAL trending TikTok videos matching this criteria.

Return ONLY JSON in this exact format:
{{
  "videos": [
    {{
      "video_url": "https://www.tiktok.com/@username/video/7...",
      "title": "Video title",
      "creator": "@username",
      "engagement_score": 95.5,
      "reason": "Why this video is perfect for personal growth learners aged 18-35"
    }}
  ]
}}

If you cannot find real videos with real URLs, return:
{{"videos": []}}

IMPORTANT: Each video_url MUST start with https://www.tiktok.com/@
"""

print("\n📧 STAGE 2: Searching for videos using ideal prompt...\n")
response2 = client.chat.completions.create(
    model="sonar-pro",
    messages=[{"role": "user", "content": stage2_prompt}],
)

raw_response = response2.choices[0].message.content
print(f"📨 RAW RESPONSE (NO PARSING):\n\n{raw_response}\n")
print("=" * 80)

# Try to parse and analyze
print("\n🔧 ATTEMPTING JSON PARSE...\n")
try:
    data = json.loads(raw_response)
    print(f"✅ JSON PARSED SUCCESSFULLY!")
    print(f"   Found {len(data.get('videos', []))} videos\n")
    print(json.dumps(data, indent=2))
except json.JSONDecodeError as e:
    print(f"❌ JSON PARSE FAILED: {e}\n")
    print(f"First 1000 chars of response:\n{raw_response[:1000]}")

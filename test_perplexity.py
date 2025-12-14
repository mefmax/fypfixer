import os
import json
import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv('PERPLEXITY_API_KEY')

if not API_KEY:
    print("❌ API_KEY not found")
    sys.exit(1)

client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

category_name = "cute cats videos"

prompt = f"""Find 10 real, popular TikTok videos about {category_name}.

Return ONLY valid JSON with real working TikTok video URLs. Each video must have:
- creator: TikTok username (@handle)
- title: Video title
- video_url: Full TikTok URL (https://www.tiktok.com/@.../video/...)
- engagement_score: Estimated engagement (0-100)
- reason: Why this video is popular

If you cannot find real videos, return: {{"videos": []}}

Return only JSON, no other text.
"""

print(f"\n🧪 SEARCHING: {category_name}\n")
print("=" * 80)

try:
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=[{"role": "user", "content": prompt}]
    )
    
    content = response.choices[0].message.content
    
    print("\n📨 RESPONSE:\n")
    print(content)
    print("\n" + "=" * 80)
    
    try:
        data = json.loads(content)
        videos = data.get("videos", [])
        
        if not videos:
            print("\n❌ NO VIDEOS FOUND (empty response)")
        else:
            print(f"\n✅ FOUND {len(videos)} VIDEOS:\n")
            
            for i, video in enumerate(videos, 1):
                url = video.get('video_url', '')
                creator = video.get('creator', 'Unknown')
                title = video.get('title', 'Untitled')
                
                print(f"{i}. {creator} - {title}")
                print(f"   {url}")
                print()
            
    except json.JSONDecodeError as e:
        print(f"\n❌ INVALID JSON: {e}")
        
except Exception as e:
    print(f"\n❌ API ERROR: {e}")

print("=" * 80)

import json
from TikTokApi import TikTokApi
import asyncio
from collections import Counter

async def main():
    async with TikTokApi() as api:
        trending = [video async for video in api.trending.videos(count=20)]
    
    data = []
    hashtags = []
    
    for video in trending:
        info = video
        data.append({
            "desc": info.get('desc', ''),
            "views": info.get('stats', {}).get('playCount', 0),
            "likes": info.get('stats', {}).get('diggCount', 0),
            "author": info.get('author', {}).get('uniqueId', 'unknown'),
            "hashtags": [ht.get('hashtagName', '') for ht in info.get('textExtra', [])]
        })
        hashtags.extend(data[-1]['hashtags'])
    
    with open('trending_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Saved {len(data)} trending videos to trending_data.json")
    
    counter = Counter(hashtags)
    print("Top hashtags:")
    for tag, count in counter.most_common(10):
        print(f"{tag}: {count}")

if __name__ == "__main__":
    asyncio.run(main())

import requests
from bs4 import BeautifulSoup
import json
from collections import Counter

print("FYPFixer Day 3: Web Scraper")

url = "https://www.tiktok.com/tag/trending"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'lxml')

    hashtags = []
    trending_tags = soup.find_all('a', href=lambda x: x and '/tag/' in x)
    for tag in trending_tags[:20]:
        hashtag = tag.get_text().strip().replace('#', '')
        if hashtag:
            hashtags.append(hashtag)

    top_hashtags = Counter(hashtags).most_common(10)
    print("TOP 10 TRENDING HASHTAGS:")
    for i, (tag, count) in enumerate(top_hashtags, 1):
        print(f"{i}. #{tag} ({count})")

    data = {"trending_hashtags": dict(top_hashtags)}
    with open('trending_hashtags.json', 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\nDay 3 COMPLETE: {len(hashtags)} hashtags analyzed!")
    print("Saved to trending_hashtags.json")
except Exception as e:
    print(f"Error: {e}")

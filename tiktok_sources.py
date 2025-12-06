TIKTOK_SOURCES = {
    "primary": "Unofficial TikTokApi (Python)",
    "backup": "TikTok Scraper (Node.js CLI)",
    "data": [
        "views",
        "likes",
        "comments",
        "shares",
        "hashtags",
        "description",
    ],
}

if __name__ == "__main__":
    print("✅ TikTok data sources defined:")
    for k, v in TIKTOK_SOURCES.items():
        print(f"{k}: {v}")
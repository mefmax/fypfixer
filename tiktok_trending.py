import asyncio
from TikTokApi import TikTokApi

async def main():
    async with TikTokApi() as api:
        trending = [video async for video in api.trending.videos(count=10)]

        print("🔥 TOP 10 TRENDING VIDEOS:")
        for i, video in enumerate(trending, 1):
            desc = video.get('desc', 'No desc')[:50] + "..."
            stats = video.get('stats', {})
            print(f"{i}. {desc}")
            print(f"   Views: {stats.get('playCount', 0):,}")
            print(f"   Likes: {stats.get('diggCount', 0):,}")
            print("---")

if __name__ == "__main__":
    asyncio.run(main())

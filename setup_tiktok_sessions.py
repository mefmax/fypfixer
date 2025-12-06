from TikTokApi import TikTokApi
import asyncio

async def setup_sessions():
    print("🔧 Создаём сессии для TikTokApi...")
    
    async with TikTokApi(custom_verify_fp="verify_abc123") as api:
        # Тестовый запрос
        trending = [video async for video in api.trending.videos(count=3)]
        
        print("✅ Сессии созданы успешно!")
        print(f"Получено {len(trending)} трендовых видео")
        
        for i, video in enumerate(trending, 1):
            print(f"{i}. {video.get('desc', 'No desc')[:50]}")

if __name__ == "__main__":
    asyncio.run(setup_sessions())

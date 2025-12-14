import os
import sys
import json
from datetime import date
import time


sys.path.insert(0, '.')


from app import create_app, db
from app.models import Category, Plan, PlanStep, StepItem, User
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


API_KEY = os.getenv('PERPLEXITY_API_KEY')
if not API_KEY:
    print("❌ PERPLEXITY_API_KEY not found in .env")
    sys.exit(1)


print(f"\n🔍 DIAGNOSTICS:")
print(f"  API Key: {API_KEY[:20]}...{API_KEY[-10:]}")
print(f"  API Key length: {len(API_KEY)}")


def extract_json_from_response(content: str) -> str:
    """
    Извлекает JSON-строку из ответа, который может быть:
    - чистым JSON
    - JSON внутри код-блока без указания языка
    - JSON внутри код-блока с указанием языка
    """
    if not content:
        return "{}"

    marker = "`" * 3
    first = content.find(marker)
    if first == -1:
        return content.strip()

    line_end = content.find("\n", first + len(marker))
    if line_end == -1:
        return "{}"

    start = line_end + 1
    second = content.find(marker, start)
    if second == -1:
        return content[start:].strip()

    return content[start:second].strip()


def try_direct_tiktok_search(category_name: str) -> list:
    """Level 1: прямой поиск реальных TikTok-видео."""
    try:
        client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")
        prompt = (
            f"Search for 10 REAL trending TikTok videos about {category_name}.\n"
            "Return ONLY JSON in the form {\"videos\": [...]}.\n"
            "Each video must have: video_url, title, creator, engagement_score, reason.\n"
            "If no real videos found, return {\"videos\": []}."
        )

        print(f"      📧 Prompt: {prompt[:100]}...")

        response = client.chat.completions.create(
            model="sonar-pro",
            messages=[{"role": "user", "content": prompt}],
        )
        
        print(f"      🔧 Response type: {type(response)}")
        print(f"      🔧 Response dir: {[x for x in dir(response) if not x.startswith('_')]}")
        
        try:
            content = response.choices[0].message.content
        except (AttributeError, IndexError, TypeError) as e:
            print(f"      🔧 Error accessing .choices[0].message.content: {e}")
            print(f"      🔧 Response.choices type: {type(response.choices)}")
            print(f"      🔧 Response.choices: {response.choices}")
            return []
        
        print(f"      📨 Raw response (first 300 chars): {content[:300]}")

        json_str = extract_json_from_response(content)
        print(f"      🔍 Extracted JSON (first 200 chars): {json_str[:200]}")
        
        data = json.loads(json_str)
        print(f"      ✅ Parsed JSON, videos count: {len(data.get('videos', []))}")

        videos = data.get("videos", [])
        real_videos = [
            v
            for v in videos
            if v.get("video_url", "").startswith("https://www.tiktok.com/@")
            and "/video/7" in v.get("video_url", "")
        ]

        if real_videos:
            print(f"    [Level 1] ✅ Found {len(real_videos)} videos")
        else:
            print(f"    [Level 1] ❌ No real videos (found {len(videos)} total, {len(real_videos)} with valid URL)")
        return real_videos
    except json.JSONDecodeError as e:
        print(f"    [Level 1] ❌ JSON Error: {str(e)[:80]}")
        return []
    except Exception as e:
        print(f"    [Level 1] ❌ Error: {str(e)[:80]}")
        import traceback
        traceback.print_exc()
        return []


def try_hashtag_discovery(category_name: str) -> list:
    """Level 2: поиск по хэштегам."""
    try:
        client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")
        prompt = (
            f"Find REAL trending TikTok videos about {category_name} using hashtag discovery.\n"
            "Return ONLY JSON in the form {\"videos\": [...]}.\n"
            "Each video must have: video_url, title, creator, engagement_score, reason.\n"
            "If no real videos, return {\"videos\": []}."
        )

        print(f"      📧 Prompt: {prompt[:100]}...")

        response = client.chat.completions.create(
            model="sonar-pro",
            messages=[{"role": "user", "content": prompt}],
        )
        
        try:
            content = response.choices[0].message.content
        except (AttributeError, IndexError, TypeError) as e:
            print(f"      🔧 Error accessing .choices[0].message.content: {e}")
            return []
        
        print(f"      📨 Raw response (first 300 chars): {content[:300]}")

        json_str = extract_json_from_response(content)
        print(f"      🔍 Extracted JSON (first 200 chars): {json_str[:200]}")
        
        data = json.loads(json_str)
        print(f"      ✅ Parsed JSON, videos count: {len(data.get('videos', []))}")

        videos = data.get("videos", [])
        real_videos = [
            v
            for v in videos
            if v.get("video_url", "").startswith("https://www.tiktok.com/@")
            and "/video/7" in v.get("video_url", "")
        ]

        if real_videos:
            print(f"    [Level 2] ✅ Found {len(real_videos)} videos")
        else:
            print(f"    [Level 2] ❌ No real videos (found {len(videos)} total, {len(real_videos)} with valid URL)")
        return real_videos
    except json.JSONDecodeError as e:
        print(f"    [Level 2] ❌ JSON Error: {str(e)[:80]}")
        return []
    except Exception as e:
        print(f"    [Level 2] ❌ Error: {str(e)[:80]}")
        import traceback
        traceback.print_exc()
        return []


def try_creator_search(category_name: str) -> list:
    """Level 3: поиск по создателям/инфлюенсерам."""
    try:
        client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")
        prompt = (
            f"Find REAL TikTok creators in category {category_name} and one viral video from each.\n"
            "Return ONLY JSON in the form {\"videos\": [...]}.\n"
            "Each video must have: video_url, title, creator, engagement_score, reason.\n"
            "If no real videos, return {\"videos\": []}."
        )

        print(f"      📧 Prompt: {prompt[:100]}...")

        response = client.chat.completions.create(
            model="sonar-pro",
            messages=[{"role": "user", "content": prompt}],
        )
        
        try:
            content = response.choices[0].message.content
        except (AttributeError, IndexError, TypeError) as e:
            print(f"      🔧 Error accessing .choices[0].message.content: {e}")
            return []
        
        print(f"      📨 Raw response (first 300 chars): {content[:300]}")

        json_str = extract_json_from_response(content)
        print(f"      🔍 Extracted JSON (first 200 chars): {json_str[:200]}")
        
        data = json.loads(json_str)
        print(f"      ✅ Parsed JSON, videos count: {len(data.get('videos', []))}")

        videos = data.get("videos", [])
        real_videos = [
            v
            for v in videos
            if v.get("video_url", "").startswith("https://www.tiktok.com/@")
            and "/video/7" in v.get("video_url", "")
        ]

        if real_videos:
            print(f"    [Level 3] ✅ Found {len(real_videos)} videos")
        else:
            print(f"    [Level 3] ❌ No real videos (found {len(videos)} total, {len(real_videos)} with valid URL)")
        return real_videos
    except json.JSONDecodeError as e:
        print(f"    [Level 3] ❌ JSON Error: {str(e)[:80]}")
        return []
    except Exception as e:
        print(f"    [Level 3] ❌ Error: {str(e)[:80]}")
        import traceback
        traceback.print_exc()
        return []


def fetch_videos_from_perplexity(category_name: str, category_code: str) -> list:
    """Последовательно пробует 3 уровня и останавливается на первом успешном."""
    print("  [Searching...]")

    videos = try_direct_tiktok_search(category_name)
    if videos:
        return videos
    time.sleep(1)

    videos = try_hashtag_discovery(category_name)
    if videos:
        return videos
    time.sleep(1)

    videos = try_creator_search(category_name)
    if videos:
        return videos

    print("  [No videos found]")
    return []


def save_videos_to_db(videos: list, step_id: int, category_code: str) -> int:
    """Сохраняет видео в БД, только с валидными URL."""
    added = 0
    for i, video in enumerate(videos):
        try:
            url = video.get("video_url", "")
            if not url.startswith("https://www.tiktok.com/@"):
                continue

            item = StepItem(
                plan_step_id=step_id,
                video_id=f"video_{category_code}_{i}",
                creator_username=video.get("creator", "@unknown"),
                title=video.get("title", "Video"),
                thumbnail_url="https://p16-sign.tiktokcdn.com/avatar-80x80.jpg",
                video_url=url,
                engagement_score=float(video.get("engagement_score", 50)),
                reason_text=video.get("reason", ""),
            )
            db.session.add(item)
            added += 1
        except Exception as e:
            print(f"    ⚠️ Skipped: {str(e)[:80]}")
    db.session.commit()
    return added


def main():
    app = create_app()
    with app.app_context():
        categories = Category.query.all()
        if not categories:
            print("❌ No categories in database")
            return

        print(f"📊 Found {len(categories)} categories")
        print("=" * 70)

        user = User.query.filter_by(client_id="ai_generator").first()
        if not user:
            user = User(client_id="ai_generator", language="en")
            db.session.add(user)
            db.session.commit()

        total_videos = 0
        successful = 0

        for i, category in enumerate(categories, 1):
            print(f"\n[{i}/{len(categories)}] 🎬 {category.name_en} ({category.code})")

            plan = Plan.query.filter_by(
                user_id=user.id,
                category_id=category.id,
                plan_date=date.today(),
            ).first()
            if not plan:
                plan = Plan(
                    user_id=user.id,
                    category_id=category.id,
                    plan_date=date.today(),
                    language="en",
                    title=f"Daily Plan: {category.name_en}",
                )
                db.session.add(plan)
                db.session.commit()

            step = PlanStep.query.filter_by(plan_id=plan.id, step_order=1).first()
            if not step:
                step = PlanStep(
                    plan_id=plan.id,
                    step_order=1,
                    action_type="watch",
                    text_en=f"Watch about {category.name_en}",
                )
                db.session.add(step)
                db.session.commit()

            videos = fetch_videos_from_perplexity(category.name_en, category.code)

            if videos:
                StepItem.query.filter_by(plan_step_id=step.id).delete()
                db.session.commit()

                added = save_videos_to_db(videos, step.id, category.code)
                print(f"  💾 Saved {added} videos")
                total_videos += added
                successful += 1
            else:
                print("  ⏭️  Skipped (no real videos)")

        print("\n" + "=" * 70)
        print(f"🎉 Done! Total: {total_videos} videos, {successful}/{len(categories)} categories")


if __name__ == "__main__":
    main()

import os
import sys
import json
from datetime import date

sys.path.insert(0, '.')

from app import create_app, db
from app.models import Category, Plan, PlanStep, StepItem, User

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get API key
API_KEY = os.getenv('PERPLEXITY_API_KEY')
if not API_KEY:
    print("❌ PERPLEXITY_API_KEY not found in .env")
    sys.exit(1)

print(f"✅ API Key loaded (first 20 chars): {API_KEY[:20]}...")

# Use OpenAI SDK (more reliable)
try:
    from openai import OpenAI
except ImportError:
    print("❌ openai package not installed")
    print("Run: pip install openai")
    sys.exit(1)


def fetch_videos_from_perplexity(category_name: str, category_code: str) -> list:
    """Call Perplexity API using OpenAI SDK"""
    
    prompt = f"""Find 10 real, popular TikTok videos about {category_name}.
Return ONLY this JSON, nothing else:

{{
  "videos": [
    {{
      "creator": "@handle",
      "title": "Video Title",
      "video_url": "https://www.tiktok.com/@handle/video/7123456789012345678",
      "engagement_score": 85,
      "reason": "Why it's good"
    }}
  ]
}}
"""

    try:
        # Create OpenAI client pointing to Perplexity API
        client = OpenAI(
            api_key=API_KEY,
            base_url="https://api.perplexity.ai"
        )
        
        print(f"  Making API call...")
        response = client.chat.completions.create(
            model="sonar-pro",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.choices[0].message.content
        
        # Parse JSON
        try:
            data = json.loads(content)
            videos = data.get("videos", [])
            print(f"  ✅ Got {len(videos)} videos from API")
            return videos
        except json.JSONDecodeError as e:
            print(f"  ⚠️  JSON Parse Error: {e}")
            print(f"  Raw response: {content[:300]}")
            return []
            
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:200]}")
        return []


def save_videos_to_db(videos: list, step_id: int, category_code: str) -> int:
    """Save videos to database"""
    
    added = 0
    for i, video in enumerate(videos):
        try:
            item = StepItem(
                plan_step_id=step_id,
                video_id=f"video_{category_code}_{i}",
                creator_username=video.get("creator", "@unknown"),
                title=video.get("title", "Video"),
                thumbnail_url="https://p16-sign.tiktokcdn.com/avatar-80x80.jpg",
                video_url=video.get("video_url", ""),
                engagement_score=float(video.get("engagement_score", 50)),
                reason_text=video.get("reason", "")
            )
            db.session.add(item)
            added += 1
        except Exception as e:
            print(f"    ⚠️ Skipped: {e}")
    
    try:
        db.session.commit()
    except Exception as e:
        print(f"    ❌ DB commit failed: {e}")
        db.session.rollback()
    
    return added


def main():
    app = create_app()
    
    with app.app_context():
        categories = Category.query.all()
        
        if not categories:
            print("❌ No categories in database")
            return
        
        print(f"📊 Found {len(categories)} categories")
        print("=" * 60)
        
        # Get or create user
        user = User.query.filter_by(client_id="ai_generator").first()
        if not user:
            user = User(client_id="ai_generator", language="en")
            db.session.add(user)
            db.session.commit()
        
        total_videos = 0
        
        for category in categories:
            print(f"\n🎬 {category.name_en} ({category.code})")
            
            # Get or create plan
            plan = Plan.query.filter_by(
                user_id=user.id,
                category_id=category.id,
                plan_date=date.today()
            ).first()
            
            if not plan:
                plan = Plan(
                    user_id=user.id,
                    category_id=category.id,
                    plan_date=date.today(),
                    language="en",
                    title=f"Daily Plan: {category.name_en}"
                )
                db.session.add(plan)
                db.session.commit()
            
            # Get or create step
            step = PlanStep.query.filter_by(plan_id=plan.id, step_order=1).first()
            if not step:
                step = PlanStep(
                    plan_id=plan.id,
                    step_order=1,
                    action_type="watch",
                    text_en=f"Watch videos about {category.name_en}"
                )
                db.session.add(step)
                db.session.commit()
            
            # Clear old videos
            StepItem.query.filter_by(plan_step_id=step.id).delete()
            db.session.commit()
            
            # Fetch videos
            videos = fetch_videos_from_perplexity(category.name_en, category.code)
            
            if videos:
                added = save_videos_to_db(videos, step.id, category.code)
                print(f"  💾 Saved {added}/{len(videos)} videos")
                total_videos += added
            else:
                print(f"  ⚠️  No videos returned")
        
        print("\n" + "=" * 60)
        print(f"🎉 Done! Total: {total_videos} videos")


if __name__ == "__main__":
    main()

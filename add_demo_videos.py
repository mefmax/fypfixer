import sys
sys.path.insert(0, '.')

from app import create_app, db
from app.models import StepItem

app = create_app()

with app.app_context():
    # Реальные TikTok видео про личностный рост
    videos = [
        {
            'plan_step_id': 1,
            'video_id': 'demo_vid_1',
            'creator': '@growthcoach',
            'title': '5 Habits to Change Your Life',
            'thumbnail_url': 'https://p16-sign.tiktokcdn.com/avatar-80x80.jpg',
            'video_url': 'https://www.tiktok.com/@fermer_tok_161/video/7040387962705677570',
            'engagement_score': 98.5,
            'reason': 'High engagement, great for beginners'
        },
        {
            'plan_step_id': 1,
            'video_id': 'demo_vid_2',
            'creator': '@mindsetmotivation',
            'title': 'Daily Affirmations That Work',
            'thumbnail_url': 'https://p16-sign.tiktokcdn.com/avatar-80x80.jpg',
            'video_url': 'https://www.tiktok.com/@anardreams/video/7043384466559094017',
            'engagement_score': 87.3,
            'reason': 'Proven techniques, 2M+ views'
        },
        {
            'plan_step_id': 1,
            'video_id': 'demo_vid_3',
            'creator': '@successhabits',
            'title': 'How to Build Discipline in 30 Days',
            'thumbnail_url': 'https://p16-sign.tiktokcdn.com/avatar-80x80.jpg',
            'video_url': 'https://www.tiktok.com/@smaglianna_life/video/7066502157331221761',
            'engagement_score': 92.1,
            'reason': 'Step-by-step guide, actionable'
        },
    ]

    # Очистить старые видео
    StepItem.query.filter_by(plan_step_id=1).delete()

    # Добавить новые
    for v in videos:
        item = StepItem(
            plan_step_id=v['plan_step_id'],
            video_id=v['video_id'],
            creator_username=v['creator'],
            title=v['title'],
            thumbnail_url=v['thumbnail_url'],
            video_url=v['video_url'],
            engagement_score=v['engagement_score'],
            reason_text=v['reason']
        )
        db.session.add(item)

    db.session.commit()
    print('✅ Added 3 demo videos to step 1')

from flask import Blueprint, request, jsonify
from datetime import datetime

plan_bp = Blueprint('plan', __name__, url_prefix='/api')

# Mock данные планов по категориям
PLANS = {
    'personal_growth': {
        'title': 'Personal Growth Plan',
        'steps': [
            {
                'title': 'Identify Your Goal',
                'description': 'Watch inspirational videos about personal development',
                'items': [
                    {
                        'title': '5 Habits to Change Your Life',
                        'creator': '@growthcoach',
                        'reason': 'High engagement, great for beginners',
                        'video_url': 'https://www.tiktok.com/@growthcoach/video/123456',
                        'thumbnail_url': 'https://via.placeholder.com/300x200?text=Growth+Habits'
                    },
                    {
                        'title': 'Morning Routine for Success',
                        'creator': '@successmind',
                        'reason': 'Practical tips for daily improvement',
                        'video_url': 'https://www.tiktok.com/@successmind/video/123457',
                        'thumbnail_url': 'https://via.placeholder.com/300x200?text=Morning+Routine'
                    },
                    {
                        'title': 'Productivity Hacks',
                        'creator': '@timemaster',
                        'reason': 'Learn to manage your time better',
                        'video_url': 'https://www.tiktok.com/@timemaster/video/123458',
                        'thumbnail_url': 'https://via.placeholder.com/300x200?text=Productivity'
                    }
                ]
            },
            {
                'title': 'Learn From Experts',
                'description': 'Follow creators who share valuable insights',
                'items': [
                    {
                        'title': 'The Science of Success',
                        'creator': '@sciencebro',
                        'reason': 'Evidence-based growth strategies',
                        'video_url': 'https://www.tiktok.com/@sciencebro/video/123459',
                        'thumbnail_url': 'https://via.placeholder.com/300x200?text=Science+Success'
                    }
                ]
            },
            {
                'title': 'Take Action',
                'description': 'Apply what you learned today',
                'items': [
                    {
                        'title': 'Challenge: 30 Days of Growth',
                        'creator': '@challengeking',
                        'reason': 'Join a community of learners',
                        'video_url': 'https://www.tiktok.com/@challengeking/video/123460',
                        'thumbnail_url': 'https://via.placeholder.com/300x200?text=30+Day+Challenge'
                    }
                ]
            }
        ]
    },
    'fitness': {
        'title': 'Fitness Plan',
        'steps': [
            {
                'title': 'Warm Up & Stretch',
                'description': 'Prepare your body for exercise',
                'items': [
                    {
                        'title': '5-Minute Full Body Stretch',
                        'creator': '@fitnessguru',
                        'reason': 'Easy warm-up for all levels',
                        'video_url': 'https://www.tiktok.com/@fitnessguru/video/123461',
                        'thumbnail_url': 'https://via.placeholder.com/300x200?text=Warm+Up'
                    }
                ]
            },
            {
                'title': 'Main Workout',
                'description': 'Follow a guided workout routine',
                'items': [
                    {
                        'title': '10-Minute HIIT Workout',
                        'creator': '@fitcoach',
                        'reason': 'Effective cardio training',
                        'video_url': 'https://www.tiktok.com/@fitcoach/video/123462',
                        'thumbnail_url': 'https://via.placeholder.com/300x200?text=HIIT+Workout'
                    }
                ]
            },
            {
                'title': 'Cool Down',
                'description': 'Relax and recover after workout',
                'items': [
                    {
                        'title': 'Cooldown Stretches',
                        'creator': '@stretchmaster',
                        'reason': 'Prevent muscle soreness',
                        'video_url': 'https://www.tiktok.com/@stretchmaster/video/123463',
                        'thumbnail_url': 'https://via.placeholder.com/300x200?text=Cool+Down'
                    }
                ]
            }
        ]
    },
    'education': {
        'title': 'Learning Plan',
        'steps': [
            {
                'title': 'Learn New Skill',
                'description': 'Watch educational content',
                'items': [
                    {
                        'title': 'Python Basics in 60 Seconds',
                        'creator': '@codetok',
                        'reason': 'Quick programming tips',
                        'video_url': 'https://www.tiktok.com/@codetok/video/123464',
                        'thumbnail_url': 'https://via.placeholder.com/300x200?text=Python+Basics'
                    }
                ]
            }
        ]
    },
    'entertainment': {
        'title': 'Entertainment Plan',
        'steps': [
            {
                'title': 'Discover New Content',
                'description': 'Enjoy trending entertainment videos',
                'items': [
                    {
                        'title': 'Funny Fails Compilation',
                        'creator': '@laughtrack',
                        'reason': 'Trending entertainment',
                        'video_url': 'https://www.tiktok.com/@laughtrack/video/123465',
                        'thumbnail_url': 'https://via.placeholder.com/300x200?text=Funny+Fails'
                    }
                ]
            }
        ]
    }
}

@plan_bp.route('/plan', methods=['GET'])
def get_plan():
    category = request.args.get('category', 'personal_growth').lower()
    lang = request.args.get('lang', 'en')
    
    plan = PLANS.get(category, PLANS['personal_growth'])
    
    return jsonify({
        'category': category,
        'language': lang,
        'generated_at': datetime.now().isoformat(),
        'title': plan['title'],
        'steps': plan['steps']
    })

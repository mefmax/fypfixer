import subprocess
from flask import Flask, render_template, jsonify
from flask import request

import json
import os
from collections import Counter

app = Flask(__name__)
GOAL_CATEGORIES = {
    'IT': {
        'goal': '💻 IT Knowledge',
        'steps': [
            {'num': 1, 'action': 'Search for "Python tutorials" or "Web development"', 'time': '2 min'},
            {'num': 2, 'action': 'Like 5 tech/coding videos that interest you', 'time': '3 min'},
            {'num': 3, 'action': 'Follow 2 tech creators or developer accounts', 'time': '2 min'},
            {'num': 4, 'action': 'Use "Not interested" on non-tech content', 'time': '2 min'},
            {'num': 5, 'action': 'Refresh your For You feed', 'time': '1 min'}
        ]
    },
    'фитнес': {
        'goal': '💪 Fitness Motivation',
        'steps': [
            {'num': 1, 'action': 'Search for "home workout" or "gym tips"', 'time': '2 min'},
            {'num': 2, 'action': 'Like 5 fitness videos that motivate you', 'time': '3 min'},
            {'num': 3, 'action': 'Follow 2 fitness trainers or athletes', 'time': '2 min'},
            {'num': 4, 'action': 'Remove unrelated content with "Not interested"', 'time': '2 min'},
            {'num': 5, 'action': 'Refresh your feed', 'time': '1 min'}
        ]
    },
    'мода': {
        'goal': '👗 Fashion & Style',
        'steps': [
            {'num': 1, 'action': 'Search for "fashion trends" or your style', 'time': '2 min'},
            {'num': 2, 'action': 'Like 5 fashion videos you love', 'time': '3 min'},
            {'num': 3, 'action': 'Follow 2 fashion creators', 'time': '2 min'},
            {'num': 4, 'action': 'Remove non-fashion content', 'time': '2 min'},
            {'num': 5, 'action': 'Refresh your feed', 'time': '1 min'}
        ]
    },
    'default': {
        'goal': '🎯 Train Your FYP',
        'steps': [
            {'num': 1, 'action': 'Search for your interest', 'time': '2 min'},
            {'num': 2, 'action': 'Like 5 videos that interest you', 'time': '3 min'},
            {'num': 3, 'action': 'Follow 2 creators in your niche', 'time': '2 min'},
            {'num': 4, 'action': 'Use "Not interested" on unwanted content', 'time': '2 min'},
            {'num': 5, 'action': 'Refresh your For You feed', 'time': '1 min'}
        ]
    }
}

def detect_category(goal_text):
    """Detect category from user goal"""
    goal_lower = goal_text.lower()
    
    if any(keyword in goal_lower for keyword in ['it', 'code', 'programming', 'dev', 'tech']):
        return 'IT'
    elif any(keyword in goal_lower for keyword in ['fitness', 'фитнес', 'workout', 'gym', 'sport', 'спорт']):
        return 'фитнес'
    elif any(keyword in goal_lower for keyword in ['fashion', 'мода', 'style', 'clothes', 'outfit']):
        return 'мода'
    else:
        return 'default'


def run_scraper():
    try:
        result = subprocess.run(
            ["python", "tiktok_web_scraper.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        print("Scraper stdout:", result.stdout[:500])
        print("Scraper stderr:", result.stderr[:500])
    except Exception as e:
        print("Scraper error:", e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/plan', methods=['GET', 'POST'])
def get_plan():
    try:
        # Получить goal из query-параметра или POST
        goal = request.args.get('goal', '').strip()
        if not goal and request.is_json:
            goal = request.json.get('goal', '').strip()
        
        goal = goal or 'default'
        category = detect_category(goal)
        category_data = GOAL_CATEGORIES.get(category, GOAL_CATEGORIES['default'])
        
        plan = {
            'goal': category_data['goal'],
            'steps': category_data['steps'],
            'total_time': '10 min'
        }
        return jsonify(plan)
    except Exception as e:
        return jsonify({'error': str(e), 'goal': 'default', 'steps': GOAL_CATEGORIES['default']['steps'], 'total_time': '10 min'})


@app.route('/api/hashtags')
def get_hashtags():
    run_scraper()
    try:
        if os.path.exists('trending_hashtags.json'):
            with open('trending_hashtags.json', 'r') as f:
                data = json.load(f)
                hashtags = data.get('trending_hashtags', {})
                top10 = Counter(hashtags).most_common(10)
                return jsonify({
                    'total': len(hashtags),
                    'top10': [{'tag': tag, 'count': count} for tag, count in top10]
                })
        else:
            return jsonify({'total': 0, 'top10': [], 'message': 'Файл trending_hashtags.json не найден'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("🚀 FYPFixer MVP запущен!")
    print("Открой: http://localhost:5000")
    app.run(debug=True, port=5000)

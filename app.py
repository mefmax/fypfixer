import subprocess
from flask import Flask, render_template, jsonify
import json
import os
from collections import Counter

app = Flask(__name__)

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

@app.route('/api/plan')
def get_plan():
    try:
        # Мок‑план с 5 шагами на сегодня
        plan = {
            'goal': 'Train your FYP',
            'steps': [
                {'num': 1, 'action': 'Search for "IT support"', 'time': '2 min'},
                {'num': 2, 'action': 'Like 5 videos that interest you', 'time': '3 min'},
                {'num': 3, 'action': 'Follow 2 creators in your niche', 'time': '2 min'},
                {'num': 4, 'action': 'Use "Not interested" on 3 videos you don\'t want', 'time': '2 min'},
                {'num': 5, 'action': 'Refresh your For You feed', 'time': '1 min'}
            ],
            'total_time': '10 min'
        }
        return jsonify(plan)
    except Exception as e:
        return jsonify({'error': str(e)})

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

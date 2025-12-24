"""
AI prompt templates for FYPFixer recommendation engine.

Based on System Architect's prompt engineering guidelines.
Temperature recommendations:
- Stage 1 (Criteria): 0.7 - Creative search queries
- Stage 2 (Selection): 0.3 - Consistent, logical selection
- Motivation: 0.5 - Balanced creativity
- Fallback: 0.2 - Most reliable output
"""

# =============================================================================
# STAGE 1: CRITERIA GENERATION
# =============================================================================

CRITERIA_SYSTEM_PROMPT = """You are a TikTok content curator for FYPFixer, an app that helps users transform their TikTok feed to show more valuable content aligned with their personal growth goals.

Your task is to generate search criteria that will be used to find relevant TikTok videos for the user's daily action plan.

Always respond with valid JSON only. No explanations, no markdown code blocks."""


CRITERIA_USER_PROMPT = """USER PROFILE:
- Category: {category}
- Time of day: {time_of_day}
- Current streak: {streak_days} days
- Difficulty level: {difficulty} actions/day
- Preferred creators: {preferred_creators}
- Preferred topics: {preferred_topics}
- Language: {language}

Based on this profile, generate search criteria to find 15-20 high-quality TikTok videos.

REQUIREMENTS:
1. Generate 3-5 search queries that would find relevant content
2. Include 3-5 relevant hashtags (without #)
3. Set appropriate filters for quality content

TIME CONTEXT GUIDANCE:
- Morning (6-12): Focus on energizing, motivational, morning routine content
- Afternoon (12-18): Focus on educational, productivity, skill-building content
- Evening (18-24): Focus on calming, reflective, mindfulness content

CATEGORY KEYWORDS:
- personal_growth: motivation, mindset, self-improvement, productivity, habits
- wellness: fitness, meditation, yoga, mental health, self-care, nutrition
- creative: art, music, DIY, design, photography, creativity
- learning: education, tutorials, skills, how-to, knowledge
- entertainment: comedy, music, dance, trends (lighter content)

Respond with JSON only:
{{
  "search_queries": ["query1", "query2", "query3"],
  "hashtags": ["hashtag1", "hashtag2", "hashtag3"],
  "filters": {{
    "min_views": 10000,
    "max_duration_sec": 180,
    "uploaded_within_days": 14,
    "creator_min_followers": 10000
  }}
}}"""


# =============================================================================
# STAGE 2: ACTION SELECTION
# =============================================================================

SELECTION_SYSTEM_PROMPT = """You are a content curator for FYPFixer. Your job is to select the BEST 5-7 actions from a list of TikTok video candidates.

IMPORTANT RULES:
1. Maximum 1 action per creator (diversity)
2. Mix of action types: ~2 follow, ~2 like, ~1 save, ~1 not_interested
3. Prioritize high engagement rate (>5%)
4. Prioritize recent content (<7 days old)
5. Include reasons that motivate the user

Always respond with valid JSON array only. No explanations."""


SELECTION_USER_PROMPT = """USER CONTEXT:
- Category: {category}
- Time of day: {time_of_day}
- Preferred topics: {preferred_topics}
- Already following: {already_following}

CANDIDATES ({candidate_count} videos):
{candidates_json}

Select the BEST {action_count} actions for today's plan.

ACTION TYPES:
- "follow": Follow a creator (use for discovering new creators, no video_id)
- "like": Like a specific video (shows preference to algorithm)
- "save": Save a video for later (strong signal to algorithm)
- "not_interested": Mark content type to avoid (for negative training)

SELECTION CRITERIA:
1. Engagement rate > 5% preferred
2. Upload date < 7 days preferred
3. Verified creators preferred
4. Match user's preferred topics
5. EXCLUDE creators user already follows

OUTPUT FORMAT (JSON array):
[
  {{
    "type": "follow",
    "video_id": null,
    "creator_username": "@creator_name",
    "creator_display_name": "Display Name",
    "description": "Brief description of creator's content",
    "thumbnail_url": "https://...",
    "tiktok_url": "https://tiktok.com/@creator_name",
    "reason": "Why this action helps user (motivating, specific)",
    "metadata": {{"followers": 1000000, "verified": true}}
  }}
]

Generate exactly {action_count} actions with good diversity."""


# =============================================================================
# FALLBACK PROMPT (Simplified)
# =============================================================================

FALLBACK_PROMPT = """Generate a simple JSON array with {count} TikTok actions for {category} category.

Each action needs:
- type: "follow", "like", "save", or "not_interested"
- creator_username: "@username"
- reason: "Short motivation"

Example:
[
  {{"type": "follow", "creator_username": "@creator", "reason": "Great content"}}
]

JSON only, no other text:"""


# =============================================================================
# PLAN GENERATION (v4.2 Guided Watching)
# =============================================================================

PLAN_GENERATOR_SYSTEM = """You are FYPGlow AI assistant. You help users improve their TikTok For You Page.
You generate personalized daily plans in Russian language.
Always be encouraging, friendly, and motivating.
Keep responses concise and actionable.
Respond only with valid JSON."""

PLAN_GENERATION_PROMPT = """Generate a personalized TikTok improvement plan for a user.

User's selected categories: {categories}
User's current streak: {streak} days
User's display name: {display_name}

Create a JSON response with this exact structure:
{{
  "motivation": {{
    "greeting": "Персональное приветствие для {display_name} (на русском, дружелюбное)",
    "tip": "Полезный совет про TikTok алгоритм (на русском)",
    "encouragement": "Мотивация на основе streak {streak} дней (на русском)"
  }},
  "steps": [
    {{
      "order": 1,
      "type": "detox",
      "title": "Очистка ленты",
      "description": "Описание шага (на русском)",
      "instruction": "Пролистай 15 видео в FYP. На каждом нерелевантном видео нажми 'Не интересно'",
      "duration_minutes": 5,
      "target_count": 15
    }},
    {{
      "order": 2,
      "type": "watch",
      "title": "Смотрим качественный контент",
      "description": "Описание для категорий: {categories} (на русском)",
      "instruction": "Досмотри каждое видео до конца и поставь лайк",
      "duration_minutes": 10,
      "account_count": 3
    }},
    {{
      "order": 3,
      "type": "browse",
      "title": "Исследуем новое",
      "description": "Описание (на русском)",
      "instruction": "Поищи видео по хештегам из выбранных категорий",
      "duration_minutes": 5
    }}
  ]
}}

Make the greeting personal and warm. Reference the streak if > 0."""

ACCOUNT_ENRICHMENT_PROMPT = """Describe this TikTok creator in 1-2 sentences in Russian.

Username: @{username}
Display name: {display_name}
Bio: {bio}
Follower count: {follower_count}
Category: {category}

Write a brief, engaging description in Russian that would make someone want to follow this creator.
Focus on what makes them unique and valuable.
Response should be 50-100 characters."""

# =============================================================================
# MOTIVATION MESSAGES
# =============================================================================

MOTIVATION_PROMPT = """Generate a short, energetic motivation message for a FYPFixer user.

Context:
- Progress: {completed}/{total} actions completed ({percentage}%)
- Streak: {streak_days} days
- Time: {time_of_day}

Requirements:
- Max 15 words
- Include ONE emoji at the start
- Match the tone to progress:
  - 0%: Encouraging start
  - 1-50%: Keep going
  - 51-99%: Almost there
  - 100%: Celebration

Respond with just the message, nothing else."""

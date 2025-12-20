"""
Ollama LocalProvider for FYPFixer AI recommendations.

Uses local Ollama instance for free inference.
Fallback to hardcoded defaults if Ollama unavailable.

Environment variables:
- OLLAMA_URL: Ollama API endpoint (default: http://localhost:11434)
- OLLAMA_MODEL: Model to use (default: llama3)
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime

from .base import AIProvider, UserContext, SearchCriteria, SelectedAction
from .prompts import (
    CRITERIA_SYSTEM_PROMPT,
    CRITERIA_USER_PROMPT,
    SELECTION_SYSTEM_PROMPT,
    SELECTION_USER_PROMPT,
    FALLBACK_PROMPT,
    MOTIVATION_PROMPT,
)
from app.config import AI_TEMPERATURES, AI_TIMEOUTS, AI_DEFAULTS, ACTION_LIMITS, OTHER_LIMITS


class LocalProvider(AIProvider):
    """
    AI Provider using local Ollama instance.

    Ollama must be running: ollama serve
    Model must be pulled: ollama pull llama3
    """

    def __init__(self):
        self.ollama_url = os.environ.get('OLLAMA_URL', AI_DEFAULTS['ollama_url'])
        self.model = os.environ.get('OLLAMA_MODEL', AI_DEFAULTS['ollama_model'])
        self._available = None  # Cached availability check

    @property
    def name(self) -> str:
        return f"ollama/{self.model}"

    def _is_available(self) -> bool:
        """Check if Ollama is running and model is available."""
        if self._available is not None:
            return self._available

        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=AI_TIMEOUTS['health_check'])
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m.get('name', '').split(':')[0] for m in models]
                self._available = self.model in model_names
            else:
                self._available = False
        except requests.exceptions.RequestException:
            self._available = False

        return self._available

    def _call_ollama(
        self,
        prompt: str,
        system: str = None,
        temperature: float = AI_TEMPERATURES['criteria'],
        timeout: int = AI_TIMEOUTS['default']
    ) -> Optional[str]:
        """
        Make request to Ollama API.

        Args:
            prompt: User prompt
            system: System prompt (optional)
            temperature: Sampling temperature (0.0-1.0)
            timeout: Request timeout in seconds

        Returns:
            Response text or None if failed
        """
        try:
            payload = {
                'model': self.model,
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temperature': temperature,
                }
            }

            if system:
                payload['system'] = system

            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()

            return response.json().get('response', '')

        except requests.exceptions.Timeout:
            print(f"Ollama timeout after {timeout}s")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Ollama request error: {e}")
            return None

    def _parse_json(self, response: str) -> Optional[Dict]:
        """
        Extract JSON from LLM response.
        Handles markdown code blocks and extra text.
        """
        if not response:
            return None

        # Remove markdown code blocks
        response = response.replace('```json', '').replace('```', '')
        response = response.strip()

        try:
            # Try direct parse
            return json.loads(response)
        except json.JSONDecodeError:
            pass

        # Try to find JSON object
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(response[start:end])
        except json.JSONDecodeError:
            pass

        # Try to find JSON array
        try:
            start = response.find('[')
            end = response.rfind(']') + 1
            if start != -1 and end > start:
                return json.loads(response[start:end])
        except json.JSONDecodeError:
            pass

        return None

    # =========================================================================
    # STAGE 1: CRITERIA GENERATION
    # =========================================================================

    def generate_criteria(self, context: UserContext) -> SearchCriteria:
        """Generate search criteria using Ollama."""

        if not self._is_available():
            print(f"Ollama not available, using default criteria for {context.category}")
            return self._get_default_criteria(context.category)

        # Format prompt with context
        prompt = CRITERIA_USER_PROMPT.format(
            category=context.category,
            time_of_day=context.time_of_day,
            streak_days=context.streak_days,
            difficulty=context.difficulty,
            preferred_creators=', '.join(context.preferred_creators) or 'none',
            preferred_topics=', '.join(context.preferred_topics) or 'none',
            language=context.language,
        )

        # Call Ollama with creative temperature
        response = self._call_ollama(
            prompt=prompt,
            system=CRITERIA_SYSTEM_PROMPT,
            temperature=AI_TEMPERATURES['criteria'],
            timeout=AI_TIMEOUTS['criteria']
        )

        result = self._parse_json(response)

        if result and 'search_queries' in result:
            return SearchCriteria(
                search_queries=result.get('search_queries', []),
                hashtags=result.get('hashtags', []),
                filters=result.get('filters', {})
            )

        # Fallback to defaults
        print(f"Failed to parse criteria, using defaults for {context.category}")
        return self._get_default_criteria(context.category)

    def _get_default_criteria(self, category: str) -> SearchCriteria:
        """Fallback criteria when AI fails."""

        defaults = {
            'personal_growth': SearchCriteria(
                search_queries=['morning routine motivation', 'productivity tips', 'self improvement habits', 'mindset coaching'],
                hashtags=['personalgrowth', 'motivation', 'selfimprovement', 'mindset', 'habits'],
                filters={'min_views': 10000, 'max_duration_sec': 180, 'uploaded_within_days': 14}
            ),
            'wellness': SearchCriteria(
                search_queries=['meditation for beginners', 'healthy habits', 'mental health tips', 'yoga routine'],
                hashtags=['wellness', 'mindfulness', 'mentalhealth', 'selfcare', 'meditation'],
                filters={'min_views': 10000, 'max_duration_sec': 180, 'uploaded_within_days': 14}
            ),
            'creative': SearchCriteria(
                search_queries=['art tutorial', 'creative process', 'DIY projects', 'design tips'],
                hashtags=['creative', 'art', 'design', 'diy', 'creativity'],
                filters={'min_views': 10000, 'max_duration_sec': 180, 'uploaded_within_days': 14}
            ),
            'learning': SearchCriteria(
                search_queries=['learn new skill', 'educational content', 'how to tutorial', 'knowledge sharing'],
                hashtags=['learning', 'education', 'howto', 'tutorial', 'knowledge'],
                filters={'min_views': 10000, 'max_duration_sec': 180, 'uploaded_within_days': 14}
            ),
            'entertainment': SearchCriteria(
                search_queries=['comedy sketch', 'music cover', 'trending dance', 'funny moments'],
                hashtags=['entertainment', 'comedy', 'music', 'trending', 'funny'],
                filters={'min_views': 50000, 'max_duration_sec': 60, 'uploaded_within_days': 7}
            ),
        }

        return defaults.get(category, defaults['personal_growth'])

    # =========================================================================
    # STAGE 2: ACTION SELECTION
    # =========================================================================

    def select_actions(
        self,
        candidates: List[Dict[str, Any]],
        context: UserContext,
        count: int = ACTION_LIMITS['default_count']
    ) -> List[SelectedAction]:
        """Select best actions from candidates using Ollama."""

        if not candidates:
            print("No candidates provided, returning default actions")
            return self._get_default_actions(context.category, count)

        # If few candidates, just format them
        if len(candidates) <= count:
            return self._format_candidates_as_actions(candidates, count)

        if not self._is_available():
            print("Ollama not available, selecting first candidates")
            return self._format_candidates_as_actions(candidates[:count], count)

        # Prepare candidates JSON (limit for context window)
        candidates_for_prompt = candidates[:OTHER_LIMITS['candidates_for_ai']]
        candidates_json = json.dumps(candidates_for_prompt, indent=2, default=str)

        # Format prompt
        prompt = SELECTION_USER_PROMPT.format(
            category=context.category,
            time_of_day=context.time_of_day,
            preferred_topics=', '.join(context.preferred_topics) or 'none',
            already_following=', '.join(context.already_following) or 'none',
            candidate_count=len(candidates_for_prompt),
            candidates_json=candidates_json,
            action_count=count,
        )

        # Call Ollama with low temperature for consistent selection
        response = self._call_ollama(
            prompt=prompt,
            system=SELECTION_SYSTEM_PROMPT,
            temperature=AI_TEMPERATURES['selection'],
            timeout=AI_TIMEOUTS['selection']
        )

        result = self._parse_json(response)

        if result and isinstance(result, list) and len(result) >= count:
            actions = []
            for item in result[:count]:
                try:
                    action = SelectedAction(
                        type=item.get('type', 'like'),
                        video_id=item.get('video_id'),
                        creator_username=item.get('creator_username', '@unknown'),
                        creator_display_name=item.get('creator_display_name', 'Unknown'),
                        description=item.get('description', ''),
                        thumbnail_url=item.get('thumbnail_url'),
                        tiktok_url=item.get('tiktok_url'),
                        reason=item.get('reason', 'Recommended for you'),
                        metadata=item.get('metadata', {})
                    )
                    actions.append(action)
                except Exception as e:
                    print(f"Error parsing action: {e}")
                    continue

            if len(actions) >= count:
                return actions[:count]

        # Fallback: format candidates as actions
        print("Failed to parse selection, using fallback")
        return self._format_candidates_as_actions(candidates[:count], count)

    def _format_candidates_as_actions(
        self,
        candidates: List[Dict],
        count: int
    ) -> List[SelectedAction]:
        """Convert raw candidates to SelectedAction objects."""

        actions = []
        action_types = ['follow', 'like', 'like', 'save', 'not_interested']

        for i, candidate in enumerate(candidates[:count]):
            action_type = action_types[i % len(action_types)]

            # Determine if this is a negative action
            is_negative = action_type == 'not_interested'

            if is_negative:
                # Create negative action (no specific video)
                action = SelectedAction(
                    type='not_interested',
                    video_id=None,
                    creator_username='',
                    creator_display_name='',
                    description='Find a video like this in your feed',
                    thumbnail_url=None,
                    tiktok_url=None,
                    reason='Teach the algorithm what you don\'t want to see',
                    metadata={'content_type': 'dance' if i % 2 == 0 else 'meme'}
                )
            else:
                action = SelectedAction(
                    type=action_type,
                    video_id=candidate.get('video_id'),
                    creator_username=candidate.get('creator_username', '@unknown'),
                    creator_display_name=candidate.get('creator_display_name', 'Unknown'),
                    description=candidate.get('description', '')[:100],
                    thumbnail_url=candidate.get('thumbnail_url'),
                    tiktok_url=candidate.get('tiktok_url') or candidate.get('url'),
                    reason=self._generate_reason(action_type, candidate),
                    metadata={
                        'views': candidate.get('views'),
                        'likes': candidate.get('likes'),
                        'verified': candidate.get('verified', False),
                    }
                )

            actions.append(action)

        return actions

    def _generate_reason(self, action_type: str, candidate: Dict) -> str:
        """Generate a simple reason for the action."""

        creator = candidate.get('creator_username', 'this creator')
        views = candidate.get('views', 0)
        verified = candidate.get('verified', False)

        reasons = {
            'follow': f"{'Verified creator' if verified else 'Great content creator'} - follow to see more!",
            'like': f"High engagement video - liking trains your algorithm",
            'save': f"Save this for later - strong signal to TikTok",
        }

        return reasons.get(action_type, 'Recommended for your feed')

    def _get_default_actions(self, category: str, count: int) -> List[SelectedAction]:
        """Get hardcoded default actions when no candidates available."""

        # Seed data by category
        seed_data = {
            'personal_growth': [
                {'type': 'follow', 'creator': '@jayshetty', 'desc': 'Motivation, mindfulness, purpose', 'followers': '12M'},
                {'type': 'follow', 'creator': '@simonsinek', 'desc': 'Leadership, inspiration', 'followers': '5M'},
                {'type': 'like', 'creator': '@mel_robbins', 'desc': 'The 5 Second Rule', 'followers': '8M'},
                {'type': 'save', 'creator': '@atomichabits', 'desc': 'Building better habits', 'followers': '2M'},
                {'type': 'not_interested', 'content': 'Dance challenges', 'desc': 'Content without educational value'},
            ],
            'wellness': [
                {'type': 'follow', 'creator': '@yogawithadriene', 'desc': 'Yoga, meditation', 'followers': '3M'},
                {'type': 'follow', 'creator': '@headspace', 'desc': 'Mindfulness, meditation', 'followers': '1M'},
                {'type': 'like', 'creator': '@drjulie', 'desc': 'Mental health tips', 'followers': '500K'},
                {'type': 'save', 'creator': '@nutritionist', 'desc': 'Healthy eating guide', 'followers': '800K'},
                {'type': 'not_interested', 'content': 'Extreme diet content', 'desc': 'Potentially harmful diet advice'},
            ],
        }

        data = seed_data.get(category, seed_data['personal_growth'])
        actions = []

        for item in data[:count]:
            if item['type'] == 'not_interested':
                action = SelectedAction(
                    type='not_interested',
                    video_id=None,
                    creator_username='',
                    creator_display_name='',
                    description=item['content'],
                    thumbnail_url=None,
                    tiktok_url=None,
                    reason=item['desc'],
                    metadata={'content_type': item['content']}
                )
            else:
                action = SelectedAction(
                    type=item['type'],
                    video_id=None,
                    creator_username=item['creator'],
                    creator_display_name=item['creator'].replace('@', '').title(),
                    description=item['desc'],
                    thumbnail_url=None,
                    tiktok_url=f"https://www.tiktok.com/{item['creator']}",
                    reason=f"Popular {category.replace('_', ' ')} creator with {item.get('followers', 'many')} followers",
                    metadata={'followers': item.get('followers')}
                )
            actions.append(action)

        return actions

    # =========================================================================
    # MOTIVATION GENERATION
    # =========================================================================

    def generate_motivation(
        self,
        context: UserContext,
        progress: Dict[str, int]
    ) -> str:
        """Generate motivation message using Ollama."""

        completed = progress.get('completed', 0)
        total = progress.get('total', 5)
        percentage = int((completed / total) * 100) if total > 0 else 0

        # Quick responses without AI for common cases
        if not self._is_available():
            return self._get_default_motivation(completed, total, context.time_of_day)

        prompt = MOTIVATION_PROMPT.format(
            completed=completed,
            total=total,
            percentage=percentage,
            streak_days=context.streak_days,
            time_of_day=context.time_of_day,
        )

        response = self._call_ollama(
            prompt=prompt,
            temperature=AI_TEMPERATURES['motivation'],
            timeout=AI_TIMEOUTS['motivation']
        )

        if response and len(response) < 100:
            return response.strip()

        return self._get_default_motivation(completed, total, context.time_of_day)

    def _get_default_motivation(self, completed: int, total: int, time_of_day: str) -> str:
        """Fallback motivation messages."""

        if completed == 0:
            messages = {
                'morning': "Good morning! Your personalized plan is ready!",
                'afternoon': "Afternoon boost: 5 quick actions await!",
                'evening': "Evening ritual: Curate your feed mindfully.",
            }
            return messages.get(time_of_day, "Your daily plan is ready!")

        percentage = int((completed / total) * 100) if total > 0 else 0

        if percentage == 100:
            return "INCREDIBLE! You completed today's plan!"
        elif percentage >= 80:
            return f"So close! Just {total - completed} more to go!"
        elif percentage >= 60:
            return f"More than halfway! {completed}/{total} done!"
        elif percentage >= 40:
            return f"Great progress! {completed}/{total} completed!"
        elif percentage >= 20:
            return f"Good start! Keep the momentum going!"
        else:
            return f"First step done! {total - completed} more to transform your feed!"


# =============================================================================
# TEST FUNCTION
# =============================================================================

def test_local_provider():
    """Quick test of LocalProvider functionality."""

    provider = LocalProvider()
    print(f"Provider: {provider.name}")
    print(f"Ollama available: {provider._is_available()}")

    # Test context
    context = UserContext(
        category='personal_growth',
        language='en',
        time_of_day='morning',
        streak_days=5,
        difficulty=5,
    )

    # Test criteria generation
    print("\n--- Testing Criteria Generation ---")
    criteria = provider.generate_criteria(context)
    print(f"Search queries: {criteria.search_queries}")
    print(f"Hashtags: {criteria.hashtags}")

    # Test action selection (with empty candidates)
    print("\n--- Testing Action Selection ---")
    actions = provider.select_actions([], context, count=5)
    print(f"Actions generated: {len(actions)}")
    for action in actions:
        print(f"  - {action.type}: {action.creator_username or action.description}")

    # Test motivation
    print("\n--- Testing Motivation ---")
    message = provider.generate_motivation(context, {'completed': 2, 'total': 5})
    print(f"Motivation: {message}")

    return True


if __name__ == '__main__':
    test_local_provider()

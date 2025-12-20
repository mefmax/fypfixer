"""
Seed creators data - fallback when AI/scraper unavailable.

This is curated content that matches our quality standards.
Update this file to change fallback recommendations.
"""

from typing import Dict, List, Any

SEED_CREATORS: Dict[str, List[Dict[str, Any]]] = {
    'personal_growth': [
        {
            'creator_username': '@jayshetty',
            'creator_display_name': 'Jay Shetty',
            'description': 'Motivation, mindfulness, purpose',
            'followers': 12000000,
            'verified': True,
            'tiktok_url': 'https://www.tiktok.com/@jayshetty'
        },
        {
            'creator_username': '@simonsinek',
            'creator_display_name': 'Simon Sinek',
            'description': 'Leadership, inspiration',
            'followers': 5000000,
            'verified': True,
            'tiktok_url': 'https://www.tiktok.com/@simonsinek'
        },
        {
            'creator_username': '@mel_robbins',
            'creator_display_name': 'Mel Robbins',
            'description': 'Confidence, productivity',
            'followers': 8000000,
            'verified': True,
            'tiktok_url': 'https://www.tiktok.com/@melrobbins'
        },
        {
            'creator_username': '@atomichabits',
            'creator_display_name': 'James Clear',
            'description': 'Building better habits',
            'followers': 2000000,
            'verified': True,
            'tiktok_url': 'https://www.tiktok.com/@atomichabits'
        },
        {
            'creator_username': '@garyvee',
            'creator_display_name': 'Gary Vaynerchuk',
            'description': 'Entrepreneurship, hustle',
            'followers': 15000000,
            'verified': True,
            'tiktok_url': 'https://www.tiktok.com/@garyvee'
        },
    ],
    'wellness': [
        {
            'creator_username': '@yogawithadriene',
            'creator_display_name': 'Yoga With Adriene',
            'description': 'Yoga, meditation',
            'followers': 3000000,
            'verified': True,
            'tiktok_url': 'https://www.tiktok.com/@yogawithadriene'
        },
        {
            'creator_username': '@headspace',
            'creator_display_name': 'Headspace',
            'description': 'Mindfulness, meditation',
            'followers': 1500000,
            'verified': True,
            'tiktok_url': 'https://www.tiktok.com/@headspace'
        },
        {
            'creator_username': '@drjulie',
            'creator_display_name': 'Dr Julie',
            'description': 'Mental health tips',
            'followers': 500000,
            'verified': False,
            'tiktok_url': 'https://www.tiktok.com/@drjulie'
        },
        {
            'creator_username': '@nutritionist',
            'creator_display_name': 'The Nutritionist',
            'description': 'Healthy eating guide',
            'followers': 800000,
            'verified': False,
            'tiktok_url': 'https://www.tiktok.com/@nutritionist'
        },
        {
            'creator_username': '@fitnesscoach',
            'creator_display_name': 'Fitness Coach',
            'description': 'Home workouts',
            'followers': 2000000,
            'verified': True,
            'tiktok_url': 'https://www.tiktok.com/@fitnesscoach'
        },
    ],
    'creative': [
        {
            'creator_username': '@drawwithjazza',
            'creator_display_name': 'Jazza',
            'description': 'Art tutorials, creative challenges',
            'followers': 1000000,
            'verified': True,
            'tiktok_url': 'https://www.tiktok.com/@drawwithjazza'
        },
    ],
    'learning': [
        {
            'creator_username': '@crashcourse',
            'creator_display_name': 'Crash Course',
            'description': 'Educational content',
            'followers': 500000,
            'verified': True,
            'tiktok_url': 'https://www.tiktok.com/@crashcourse'
        },
    ],
}

# Default category if requested one not found
DEFAULT_CATEGORY = 'personal_growth'


def get_seed_creators(category: str) -> List[Dict[str, Any]]:
    """Get seed creators for a category with fallback."""
    return SEED_CREATORS.get(category, SEED_CREATORS[DEFAULT_CATEGORY])

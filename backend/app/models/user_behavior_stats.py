"""User behavior statistics model for engagement tracking."""

from datetime import date
from app import db
from sqlalchemy import JSON
from sqlalchemy.sql import func
from app.config import LEVEL_THRESHOLDS


class UserBehaviorStats(db.Model):
    """
    Tracks user engagement metrics, streaks, and preferences.
    One row per user (1:1 relationship with User).

    Psychology basis:
    - Streaks leverage loss aversion (don't break the chain)
    - Adaptive difficulty maintains Flow State
    - Gamification provides variable rewards
    """
    __tablename__ = 'user_behavior_stats'

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)

    # Engagement metrics
    total_actions_completed = db.Column(db.Integer, default=0)
    total_days_active = db.Column(db.Integer, default=0)
    avg_completion_rate = db.Column(db.Numeric(5, 4), default=0)

    # Streak tracking (Psychology Stage 1)
    current_streak_days = db.Column(db.Integer, default=0)
    max_streak_days = db.Column(db.Integer, default=0)
    last_completed_date = db.Column(db.Date, nullable=True)

    # Adaptive difficulty (Flow State: 3-8 actions/day)
    current_difficulty = db.Column(db.Integer, default=5)

    # Learned preferences (JSON for flexibility)
    preferred_creators = db.Column(JSON, default=dict)  # {"@creator": score}
    preferred_topics = db.Column(JSON, default=dict)    # {"topic": score}

    # Gamification
    current_level = db.Column(db.String(20), default='Beginner')
    total_xp = db.Column(db.Integer, default=0)
    achievements = db.Column(JSON, default=list)  # ["streak_7", "first_plan", ...]

    # Timestamps
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        db.Index('idx_behavior_streak', current_streak_days.desc()),
    )

    # Relationship
    user = db.relationship('User', backref=db.backref('behavior_stats', uselist=False))

    def update_streak(self, completed_date: date = None):
        """Update streak based on completion date."""
        today = completed_date or date.today()

        if self.last_completed_date is None:
            # First completion ever
            self.current_streak_days = 1
        elif self.last_completed_date == today:
            # Already completed today, no change
            pass
        elif (today - self.last_completed_date).days == 1:
            # Consecutive day - increment streak
            self.current_streak_days += 1
        elif (today - self.last_completed_date).days > 1:
            # Streak broken - reset to 1
            self.current_streak_days = 1

        # Update max streak
        if self.current_streak_days > self.max_streak_days:
            self.max_streak_days = self.current_streak_days

        self.last_completed_date = today
        self.total_days_active += 1

    def get_days_since_last_activity(self) -> int:
        """Get days since last completed action (for lapse detection)."""
        if self.last_completed_date is None:
            return 999  # Never active
        return (date.today() - self.last_completed_date).days

    def add_xp(self, amount: int):
        """Add XP and check for level up."""
        self.total_xp += amount
        self._check_level_up()

    def _check_level_up(self):
        """Update level based on XP thresholds."""
        for threshold, level in reversed(LEVEL_THRESHOLDS):
            if self.total_xp >= threshold:
                self.current_level = level
                break

    def to_dict(self):
        return {
            'userId': self.user_id,
            'streak': {
                'current': self.current_streak_days,
                'max': self.max_streak_days,
                'lastCompleted': str(self.last_completed_date) if self.last_completed_date else None,
            },
            'engagement': {
                'totalActions': self.total_actions_completed,
                'totalDays': self.total_days_active,
                'avgCompletionRate': float(self.avg_completion_rate) if self.avg_completion_rate else 0,
            },
            'difficulty': self.current_difficulty,
            'gamification': {
                'level': self.current_level,
                'xp': self.total_xp,
                'achievements': self.achievements or [],
            },
        }

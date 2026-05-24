"""ContentFlow — Content calendar generator."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional

from .generator import ContentGenerator


@dataclass
class ScheduledPost:
    """A single scheduled content post."""

    day: str
    platform: str
    topic: str
    content: str
    scheduled_date: Optional[date] = None

    def __str__(self) -> str:
        return f"[{self.day} | {self.platform.upper()}] {self.content[:80]}..."


@dataclass
class ContentWeek:
    """A week of scheduled content."""

    topic: str
    posts: list[ScheduledPost] = field(default_factory=list)

    def to_dict(self) -> list[dict]:
        return [
            {
                "day": p.day,
                "platform": p.platform,
                "topic": p.topic,
                "content": p.content,
                "scheduled_date": str(p.scheduled_date) if p.scheduled_date else None,
            }
            for p in self.posts
        ]

    def __repr__(self) -> str:
        return f"ContentWeek(topic={self.topic!r}, posts={len(self.posts)})"


class ContentCalendar:
    """
    Generate structured weekly/monthly content calendars.

    Args:
        generator: ContentGenerator instance (creates one if not provided)
        brand_voice: Brand voice profile name

    Example::

        from contentflow import ContentCalendar

        cal = ContentCalendar()
        week = cal.generate_week("AI productivity", platforms=["linkedin", "twitter", "instagram"])
        for post in week.posts:
            print(post)
    """

    WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    DEFAULT_SCHEDULE = {
        "linkedin": ["Monday", "Wednesday", "Friday"],
        "instagram": ["Tuesday", "Thursday", "Saturday"],
        "twitter": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "tiktok": ["Wednesday", "Friday", "Sunday"],
        "email": ["Tuesday"],
    }

    def __init__(self, generator: Optional[ContentGenerator] = None, brand_voice: str = "friendly"):
        self.generator = generator or ContentGenerator(brand_voice=brand_voice)

    def generate_week(
        self,
        topic: str,
        platforms: Optional[list[str]] = None,
        start_date: Optional[date] = None,
        hashtag_category: str = "lifestyle",
    ) -> ContentWeek:
        """
        Generate one week of content for a topic across platforms.

        Args:
            topic: Main content topic
            platforms: List of platforms (default: linkedin, twitter, instagram)
            start_date: Week start date (default: next Monday)
            hashtag_category: Hashtag category for templates

        Returns:
            ContentWeek with scheduled posts
        """
        platforms = platforms or ["linkedin", "twitter", "instagram"]
        week = ContentWeek(topic=topic)

        if start_date is None:
            today = date.today()
            days_until_monday = (7 - today.weekday()) % 7 or 7
            start_date = today + timedelta(days=days_until_monday)

        day_map = {day: start_date + timedelta(days=i) for i, day in enumerate(self.WEEKDAYS)}

        for platform in platforms:
            posting_days = self.DEFAULT_SCHEDULE.get(platform, ["Monday", "Thursday"])
            tone_map = {
                "linkedin": "professional",
                "twitter": "casual",
                "instagram": "engaging",
                "tiktok": "playful",
                "email": "formal",
            }
            tone = tone_map.get(platform, "engaging")

            for day in posting_days:
                content = self.generator.generate(
                    topic=topic, platform=platform, tone=tone, hashtag_category=hashtag_category
                )
                post = ScheduledPost(
                    day=day,
                    platform=platform,
                    topic=topic,
                    content=content,
                    scheduled_date=day_map.get(day),
                )
                week.posts.append(post)

        week.posts.sort(key=lambda p: self.WEEKDAYS.index(p.day))
        return week

    def generate_month(
        self,
        topics: list[str],
        platforms: Optional[list[str]] = None,
        start_date: Optional[date] = None,
    ) -> list[ContentWeek]:
        """
        Generate four weeks of content from a list of topics.

        Args:
            topics: Topics to rotate through (min 1, max 4)
            platforms: Target platforms
            start_date: Month start date

        Returns:
            List of 4 ContentWeek objects
        """
        start = start_date or date.today()
        weeks = []
        for i in range(4):
            topic = topics[i % len(topics)]
            week_start = start + timedelta(weeks=i)
            weeks.append(self.generate_week(topic, platforms=platforms, start_date=week_start))
        return weeks

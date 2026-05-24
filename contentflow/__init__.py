"""
ContentFlow v1.0.0 — Multi-platform AI marketing content generator.
"""

__version__ = "1.0.0"

from .calendar import ContentCalendar, ContentWeek, ScheduledPost
from .generator import ContentGenerator, ContentScore
from .seo import MetaBundle, SEOOptimizer

__all__ = [
    "ContentGenerator",
    "ContentScore",
    "ContentCalendar",
    "ContentWeek",
    "ScheduledPost",
    "SEOOptimizer",
    "MetaBundle",
]

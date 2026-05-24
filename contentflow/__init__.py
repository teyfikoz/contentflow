"""
ContentFlow v1.0.0 — Multi-platform AI marketing content generator.
"""

__version__ = "1.0.0"

from .generator import ContentGenerator, ContentScore
from .calendar import ContentCalendar, ContentWeek, ScheduledPost
from .seo import SEOOptimizer, MetaBundle

__all__ = [
    "ContentGenerator",
    "ContentScore",
    "ContentCalendar",
    "ContentWeek",
    "ScheduledPost",
    "SEOOptimizer",
    "MetaBundle",
]

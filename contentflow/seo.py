"""ContentFlow — SEO content optimizer."""
from __future__ import annotations

import random
import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class MetaBundle:
    """SEO meta tags bundle."""

    title: str
    description: str
    keywords: list[str]
    og_title: str
    og_description: str
    slug: str

    def __str__(self) -> str:
        return (
            f"<title>{self.title}</title>\n"
            f'<meta name="description" content="{self.description}">\n'
            f'<meta name="keywords" content="{", ".join(self.keywords)}">\n'
        )


class SEOOptimizer:
    """
    SEO content optimizer — generates meta tags, titles, slugs, and blog outlines.

    Example::

        from contentflow import SEOOptimizer

        seo = SEOOptimizer()
        bundle = seo.generate_meta("Istanbul travel guide", keywords=["Istanbul", "Turkey"])
        print(bundle)

        outline = seo.generate_blog_outline("10 reasons to visit Istanbul")
        for section in outline:
            print(section)
    """

    TITLE_TEMPLATES = [
        "{topic} — Complete Guide for 2026",
        "The Ultimate {topic} Guide",
        "{topic}: Everything You Need to Know",
        "How to Master {topic} in 2026",
        "{topic} — Expert Tips & Insights",
        "Top 10 {topic} Strategies That Actually Work",
        "{topic} Explained: From Beginner to Expert",
    ]

    DESCRIPTION_TEMPLATES = [
        "Discover everything about {topic}. Expert insights, practical tips, and actionable strategies to help you succeed. Start reading now.",
        "Looking for the best {topic} guide? We cover all the essentials with real examples and proven strategies. Updated for 2026.",
        "Master {topic} with our comprehensive guide. Learn from experts, avoid common mistakes, and achieve your goals faster.",
    ]

    def generate_meta(
        self,
        topic: str,
        keywords: Optional[list[str]] = None,
        max_title_length: int = 60,
        max_desc_length: int = 160,
    ) -> MetaBundle:
        """
        Generate a complete SEO meta bundle.

        Args:
            topic: Page topic or main keyword phrase
            keywords: Additional target keywords (auto-extracted if None)
            max_title_length: Max title character length
            max_desc_length: Max description character length

        Returns:
            MetaBundle with title, description, keywords, OG tags, and slug
        """
        kws = keywords or self._extract_keywords(topic)
        title = random.choice(self.TITLE_TEMPLATES).format(topic=topic)[:max_title_length]
        description = random.choice(self.DESCRIPTION_TEMPLATES).format(topic=topic)[:max_desc_length]
        slug = re.sub(r"[^a-z0-9]+", "-", topic.lower().strip()).strip("-")
        og_title = f"{title} | Expert Guide"[:60]
        og_desc = description[:120]

        return MetaBundle(
            title=title,
            description=description,
            keywords=kws,
            og_title=og_title,
            og_description=og_desc,
            slug=slug,
        )

    def generate_blog_outline(self, title: str, sections: int = 6) -> list[str]:
        """
        Generate a structured blog post outline.

        Args:
            title: Blog post title
            sections: Number of sections to generate

        Returns:
            List of section headings
        """
        parts = title.lower().split()
        topic_words = [w for w in parts if len(w) > 4][:3]
        topic = " ".join(topic_words) if topic_words else title

        structure = [
            f"Introduction: Why {title} Matters in 2026",
            f"What Is {topic.title()}? A Clear Definition",
            f"The Top Benefits of {topic.title()}",
            f"Common Mistakes to Avoid with {topic.title()}",
            f"Step-by-Step Guide to {topic.title()}",
            f"Expert Tips for Advanced {topic.title()}",
            f"Tools and Resources for {topic.title()}",
            f"Real-World Examples of {topic.title()} Success",
            f"Future Trends in {topic.title()}",
            f"Conclusion: Your {topic.title()} Action Plan",
        ]
        return structure[:sections]

    def generate_title(self, topic: str, style: str = "guide") -> str:
        """
        Generate an SEO-optimized title.

        Args:
            topic: Page topic
            style: Title style (guide/how-to/list/question/comparison)

        Returns:
            SEO title string
        """
        styles = {
            "guide": f"{topic} — The Complete 2026 Guide",
            "how-to": f"How to {topic}: Step-by-Step for Beginners",
            "list": f"15 Best {topic} Tips You Need to Know in 2026",
            "question": f"What Is {topic} and Why Does It Matter?",
            "comparison": f"{topic} vs Alternatives: Which Is Best in 2026?",
        }
        return styles.get(style, styles["guide"])

    def _extract_keywords(self, text: str) -> list[str]:
        """Extract keywords from text (simple stopword-based approach)."""
        stopwords = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "is", "are", "was", "be", "this", "that",
        }
        words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
        return list(dict.fromkeys(w for w in words if w not in stopwords))[:10]

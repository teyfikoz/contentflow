"""
ContentFlow v1.0.0 — Multi-platform AI content generation.
"""
from __future__ import annotations

import os
import random
from dataclasses import dataclass
from typing import Optional

import requests

# ── Brand voice profiles ─────────────────────────────────────────────────────

BRAND_VOICES = {
    "startup": {"tone": "bold", "style": "punchy", "emoji": True},
    "enterprise": {"tone": "authoritative", "style": "formal", "emoji": False},
    "creative": {"tone": "playful", "style": "expressive", "emoji": True},
    "minimal": {"tone": "clean", "style": "direct", "emoji": False},
    "friendly": {"tone": "warm", "style": "conversational", "emoji": True},
}

# ── Platform templates ─────────────────────────────────────────────────────────

PLATFORM_TEMPLATES = {
    "instagram": [
        "{hook} ✨ {body} Drop a ❤️ if you agree! #{tag1} #{tag2} #{tag3}",
        "POV: You discover {topic}. 🔥 {body} Save this for later! #{tag1} #{tag2}",
        "{emoji} {hook} {body} Tag someone who needs this! #{tag1} #{tag2} #{tag3}",
    ],
    "linkedin": [
        "I've been thinking about {topic}.\n\n{body}\n\nHere's what I learned:\n→ {point1}\n→ {point2}\n→ {point3}\n\nWhat's your experience? #{tag1} #{tag2}",
        "{hook}\n\n{body}\n\nThe key insight: {insight}\n\nLike + share if this resonates. #{tag1} #{tag2} #{tag3}",
        "Unpopular opinion: {hook}\n\n{body}\n\nAgree or disagree? Let me know in the comments. #{tag1}",
    ],
    "twitter": [
        "{hook} {body} #{tag1} #{tag2}",
        "Hot take: {hook}\n\n{body}\n\n(thread 🧵)",
        "{body}\n\n— {hook}\n\n#{tag1} #{tag2}",
    ],
    "tiktok": [
        "Wait for it... 👀 {hook} {body} Follow for more! #{tag1} #{tag2} #fyp",
        "POV: {hook} 😱 {body} #{tag1} #{tag2} #viral",
        "{hook} (this one hits different) {body} #{tag1} #{tag2} #foryoupage",
    ],
    "email": [
        "Subject: {hook}\n\nHi {name},\n\n{body}\n\n{cta}\n\nBest,\nThe Team",
        "Subject: {hook} — Limited Time\n\nDear {name},\n\n{body}\n\n{cta}\n\nWarm regards,\nThe Team",
    ],
    "blog": [
        "# {hook}\n\n{body}\n\n## Key Takeaways\n- {point1}\n- {point2}\n- {point3}\n\n{cta}",
    ],
    "sms": [
        "{hook} {body} Reply STOP to opt out.",
        "🚨 {hook} {body} Click: {url}",
    ],
    "push": [
        "{hook}: {body}",
        "⚡ {hook} — {body}",
    ],
}

VIBES = {
    "exciting": {"adjectives": ["thrilling", "electrifying", "unforgettable"], "emoji": "🔥"},
    "romantic": {"adjectives": ["enchanting", "dreamy", "magical"], "emoji": "💫"},
    "luxurious": {"adjectives": ["exclusive", "premium", "world-class"], "emoji": "✨"},
    "adventurous": {"adjectives": ["bold", "breathtaking", "wild"], "emoji": "🌍"},
    "relaxing": {"adjectives": ["serene", "peaceful", "rejuvenating"], "emoji": "🌿"},
    "cultural": {"adjectives": ["rich", "authentic", "immersive"], "emoji": "🎭"},
    "family": {"adjectives": ["memorable", "joyful", "perfect"], "emoji": "👨‍👩‍👧‍👦"},
    "budget": {"adjectives": ["affordable", "smart", "unbeatable value"], "emoji": "💰"},
}

LANGUAGE_TEMPLATES = {
    "tr": {
        "instagram": "{hook} ✨ {body} Beğendiysen kaydet! #{tag1} #{tag2}",
        "linkedin": "{hook}\n\n{body}\n\nSizin deneyiminiz nedir? #{tag1} #{tag2}",
        "twitter": "{hook} {body} #{tag1} #{tag2}",
    },
    "de": {
        "instagram": "{hook} ✨ {body} Speichern für später! #{tag1} #{tag2}",
        "linkedin": "{hook}\n\n{body}\n\nWas meinen Sie dazu? #{tag1} #{tag2}",
    },
    "fr": {
        "instagram": "{hook} ✨ {body} Enregistrez pour plus tard! #{tag1} #{tag2}",
        "linkedin": "{hook}\n\n{body}\n\nVotre avis? #{tag1} #{tag2}",
    },
    "es": {
        "instagram": "{hook} ✨ {body} ¡Guárdalo para después! #{tag1} #{tag2}",
        "linkedin": "{hook}\n\n{body}\n\n¿Cuál es tu experiencia? #{tag1} #{tag2}",
    },
}

HASHTAG_SETS = {
    "travel": ["travel", "wanderlust", "explore", "vacation", "adventure", "travelgram"],
    "tech": ["technology", "innovation", "ai", "startup", "tech", "digital"],
    "business": ["business", "entrepreneur", "growth", "success", "marketing", "leadership"],
    "lifestyle": ["lifestyle", "motivation", "mindset", "wellness", "selfcare", "inspiration"],
    "food": ["food", "foodie", "instafood", "cooking", "recipe", "delicious"],
}

TRAVEL_QUOTES = {
    "Adventure": [
        '"Adventure is worthwhile in itself." — Amelia Earhart',
        '"Life is either a daring adventure or nothing at all." — Helen Keller',
        '"Not all those who wander are lost." — J.R.R. Tolkien',
        '"The biggest adventure you can take is to live the life of your dreams." — Oprah Winfrey',
    ],
    "Luxury": [
        '"Luxury is the ease of a t-shirt in a very expensive dress." — Karl Lagerfeld',
        '"The best things in life are free. The second best are very expensive." — Coco Chanel',
        '"Travel is the only thing you buy that makes you richer." — Anonymous',
    ],
    "Family": [
        '"The greatest legacy we can leave our children is happy memories." — Og Mandino',
        '"Family is not an important thing. It\'s everything." — Michael J. Fox',
        '"In family life, love is the oil that eases friction." — Friedrich Nietzsche',
    ],
    "Culture": [
        '"Travel makes one modest. You see what a tiny place you occupy in the world." — Gustave Flaubert',
        '"The world is a book, and those who do not travel read only one page." — Saint Augustine',
        '"Travel is fatal to prejudice, bigotry, and narrow-mindedness." — Mark Twain',
    ],
    "Mindset": [
        '"To travel is to live." — Hans Christian Andersen',
        '"We travel not to escape life, but for life not to escape us." — Anonymous',
        '"Travel far enough, you meet yourself." — David Mitchell',
    ],
}


@dataclass
class ContentScore:
    """Quality metrics for generated content."""

    readability: float      # 0-1: how easy to read
    engagement: float       # 0-1: predicted engagement potential
    hashtag_quality: float  # 0-1: hashtag relevance score
    length_fit: float       # 0-1: length fit for platform
    overall: float          # 0-1: weighted average

    def __str__(self) -> str:
        return (
            f"ContentScore(readability={self.readability:.2f}, "
            f"engagement={self.engagement:.2f}, "
            f"overall={self.overall:.2f})"
        )


class ContentGenerator:
    """
    Multi-platform AI marketing content generator.

    Supports Instagram, LinkedIn, Twitter, TikTok, Email, Blog, SMS, Push.
    Works offline with curated templates, or online with HuggingFace AI.

    Args:
        api_key: HuggingFace API token (optional, enables AI mode)
        brand_voice: One of 'startup', 'enterprise', 'creative', 'minimal', 'friendly'
        language: ISO 639-1 code — 'en', 'tr', 'de', 'fr', 'es' (default: 'en')
        model: HuggingFace model ID for AI mode
    """

    SUPPORTED_PLATFORMS = list(PLATFORM_TEMPLATES.keys())
    SUPPORTED_LANGUAGES = ["en", "tr", "de", "fr", "es"]
    SUPPORTED_VOICES = list(BRAND_VOICES.keys())

    def __init__(
        self,
        api_key: Optional[str] = None,
        brand_voice: str = "friendly",
        language: str = "en",
        model: str = "google/flan-t5-large",
    ):
        self.api_key = api_key or os.environ.get("HF_API_TOKEN")
        self.brand_voice = BRAND_VOICES.get(brand_voice, BRAND_VOICES["friendly"])
        self.language = language
        self.model = model
        self.api_url = f"https://api-inference.huggingface.co/models/{model}"
        self._voice_name = brand_voice

    # ── Core generate method ──────────────────────────────────────────────────

    def generate(
        self,
        topic: str,
        platform: str = "instagram",
        tone: str = "engaging",
        cta: str = "",
        hashtag_category: str = "travel",
    ) -> str:
        """
        Generate platform-optimized content for any topic.

        Args:
            topic: Main subject (e.g. "product launch", "Istanbul trip")
            platform: Target platform (instagram/linkedin/twitter/tiktok/email/blog/sms/push)
            tone: Tone override (engaging, professional, casual, urgent)
            cta: Custom call-to-action text
            hashtag_category: Category for hashtag suggestions

        Returns:
            Platform-optimized content string
        """
        if self.api_key:
            return self._ai_generate(topic, platform, tone)
        return self._template_generate(topic, platform, cta, hashtag_category)

    def _template_generate(self, topic: str, platform: str, cta: str, hashtag_category: str) -> str:
        platform = platform.lower()
        tags = random.sample(HASHTAG_SETS.get(hashtag_category, HASHTAG_SETS["lifestyle"]), 3)
        hook = f"{topic} is changing everything"
        body = f"Here's why {topic} matters more than ever in 2026."
        point1 = "It drives real results"
        point2 = "Everyone is talking about it"
        point3 = "You can start today"
        insight = f"{topic} creates lasting value"
        url = "bit.ly/link"
        emoji = "🚀" if self.brand_voice["emoji"] else ""

        if self.language != "en" and platform in LANGUAGE_TEMPLATES.get(self.language, {}):
            template = LANGUAGE_TEMPLATES[self.language][platform]
        elif platform in PLATFORM_TEMPLATES:
            template = random.choice(PLATFORM_TEMPLATES[platform])
        else:
            template = random.choice(PLATFORM_TEMPLATES["instagram"])

        return template.format(
            topic=topic, hook=hook, body=body, emoji=emoji,
            tag1=tags[0], tag2=tags[1], tag3=tags[2] if len(tags) > 2 else tags[0],
            point1=point1, point2=point2, point3=point3,
            insight=insight, name="there", cta=cta or f"Learn more about {topic}",
            url=url,
        )

    def _ai_generate(self, topic: str, platform: str, tone: str) -> str:
        prompt = (
            f"Write a {tone} {platform} post about {topic}. "
            f"Brand voice: {self._voice_name}. "
            f"Include relevant hashtags. Keep it concise and engaging."
        )
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.post(self.api_url, headers=headers, json={"inputs": prompt}, timeout=15)
            result = response.json()
            if isinstance(result, list) and result and "generated_text" in result[0]:
                return result[0]["generated_text"]
        except Exception:
            pass
        return self._template_generate(topic, platform, "", "lifestyle")

    # ── Ad copy (backward compat) ─────────────────────────────────────────────

    def generate_ad_copy(
        self,
        destination: str,
        vibe: str = "exciting",
        platform: str = "Instagram",
    ) -> str:
        """
        Generate travel ad copy for a destination.
        Backward compatible with v0.4.0.

        Args:
            destination: City or place name
            vibe: Travel vibe (exciting/romantic/luxurious/adventurous/relaxing/cultural)
            platform: Target social platform

        Returns:
            Ad copy string
        """
        vibe_data = VIBES.get(vibe.lower(), VIBES["exciting"])
        adj = random.choice(vibe_data["adjectives"])
        emoji = vibe_data["emoji"]
        tags = random.sample(HASHTAG_SETS["travel"], 3)

        if self.api_key:
            prompt = (
                f"Write a catchy {platform} marketing slogan for visiting {destination}. "
                f"The vibe should be {vibe}. Include 2-3 relevant hashtags."
            )
            headers = {"Authorization": f"Bearer {self.api_key}"}
            try:
                response = requests.post(
                    self.api_url, headers=headers, json={"inputs": prompt}, timeout=15
                )
                result = response.json()
                if isinstance(result, list) and result and "generated_text" in result[0]:
                    return result[0]["generated_text"]
            except Exception:
                pass

        templates = [
            f"{destination} is calling! Experience a {adj} adventure filled with history and flavor. ✈️ #{tags[0]} #{tags[1]} #{destination.lower().replace(' ', '')}",
            f"Discover the {adj} magic of {destination} {emoji} Your next {platform.lower()} story starts here! #{tags[0]} #{tags[1]}",
            f"Escape to {destination}. It's simply {adj}. {emoji} #{tags[0]} #{tags[1]} #{tags[2]}",
            f"{emoji} {destination} awaits. {adj.capitalize()}, unforgettable, yours. Book now! #{tags[0]} #{destination.lower().replace(' ', '')}",
        ]
        return random.choice(templates)

    # ── Batch generation ──────────────────────────────────────────────────────

    def batch_generate(
        self,
        topics: list[str],
        platform: str = "instagram",
        tone: str = "engaging",
    ) -> list[dict]:
        """
        Generate content for multiple topics at once.

        Args:
            topics: List of topics/destinations
            platform: Target platform
            tone: Content tone

        Returns:
            List of dicts with 'topic' and 'content' keys
        """
        return [
            {"topic": topic, "content": self.generate(topic, platform=platform, tone=tone)}
            for topic in topics
        ]

    # ── Content scoring ───────────────────────────────────────────────────────

    def score_content(self, content: str, platform: str = "instagram") -> ContentScore:
        """
        Score content quality across multiple dimensions.

        Args:
            content: The generated content string
            platform: Target platform (affects length scoring)

        Returns:
            ContentScore with readability, engagement, hashtag_quality, length_fit, overall
        """
        words = content.split()
        word_count = len(words)
        hashtag_count = content.count("#")
        has_emoji = any(ord(c) > 127 for c in content)
        has_cta = any(
            kw in content.lower()
            for kw in ["click", "save", "share", "follow", "learn", "book", "get"]
        )

        # Readability: shorter sentences score better
        sentences = content.split(".")
        avg_sentence_len = word_count / max(len(sentences), 1)
        readability = max(0.0, min(1.0, 1.0 - (avg_sentence_len - 10) / 30))

        # Engagement: emojis, hashtags, CTA boost score
        engagement = 0.5
        if has_emoji:
            engagement += 0.15
        if 2 <= hashtag_count <= 5:
            engagement += 0.15
        if has_cta:
            engagement += 0.15
        if "?" in content:
            engagement += 0.05
        engagement = min(1.0, engagement)

        # Hashtag quality
        hashtag_quality = min(1.0, hashtag_count / 3) if hashtag_count > 0 else 0.0

        # Length fit by platform
        ideal_lengths = {
            "instagram": (100, 300), "linkedin": (150, 600), "twitter": (40, 280),
            "tiktok": (50, 150), "email": (100, 500), "blog": (300, 2000),
        }
        lo, hi = ideal_lengths.get(platform, (50, 400))
        char_count = len(content)
        if lo <= char_count <= hi:
            length_fit = 1.0
        elif char_count < lo:
            length_fit = char_count / lo
        else:
            length_fit = max(0.0, 1.0 - (char_count - hi) / hi)

        overall = (
            readability * 0.25
            + engagement * 0.40
            + hashtag_quality * 0.15
            + length_fit * 0.20
        )

        return ContentScore(
            readability=round(readability, 2),
            engagement=round(engagement, 2),
            hashtag_quality=round(hashtag_quality, 2),
            length_fit=round(length_fit, 2),
            overall=round(overall, 2),
        )

    # ── Travel quotes (backward compat) ──────────────────────────────────────

    def get_travel_quote(self, category: str = "Adventure") -> str:
        """
        Get a famous travel quote by category.

        Args:
            category: Adventure/Luxury/Family/Culture/Mindset

        Returns:
            Quote string
        """
        category_quotes = TRAVEL_QUOTES.get(category, TRAVEL_QUOTES["Adventure"])
        return random.choice(category_quotes)

"""Tests for ContentFlow v1.0.0."""

import pytest


def test_version():
    import contentflow
    assert contentflow.__version__ == "1.0.0"


def test_all_exports():
    from contentflow import ContentGenerator, ContentCalendar, SEOOptimizer
    from contentflow import ContentScore, ContentWeek, ScheduledPost, MetaBundle
    assert all(cls is not None for cls in [ContentGenerator, ContentCalendar, SEOOptimizer])


# ── ContentGenerator ──────────────────────────────────────────────────────────

def test_generate_ad_copy_backward_compat():
    from contentflow import ContentGenerator
    gen = ContentGenerator()
    copy = gen.generate_ad_copy("Istanbul", vibe="exciting", platform="Instagram")
    assert isinstance(copy, str)
    assert "Istanbul" in copy


def test_generate_multi_platform():
    from contentflow import ContentGenerator
    gen = ContentGenerator()
    for platform in ["instagram", "linkedin", "twitter", "tiktok", "email", "blog"]:
        content = gen.generate("AI tools", platform=platform, tone="engaging")
        assert isinstance(content, str)
        assert len(content) > 10


def test_generate_brand_voices():
    from contentflow import ContentGenerator
    for voice in ["startup", "enterprise", "creative", "minimal", "friendly"]:
        gen = ContentGenerator(brand_voice=voice)
        content = gen.generate("product launch", platform="instagram")
        assert isinstance(content, str)


def test_batch_generate():
    from contentflow import ContentGenerator
    gen = ContentGenerator()
    results = gen.batch_generate(["Paris", "Tokyo", "Istanbul"], platform="instagram")
    assert len(results) == 3
    for r in results:
        assert "topic" in r
        assert "content" in r
        assert isinstance(r["content"], str)


def test_score_content():
    from contentflow import ContentGenerator
    gen = ContentGenerator()
    content = gen.generate("AI productivity", platform="linkedin")
    score = gen.score_content(content, platform="linkedin")
    assert 0.0 <= score.readability <= 1.0
    assert 0.0 <= score.engagement <= 1.0
    assert 0.0 <= score.overall <= 1.0


def test_get_travel_quote_all_categories():
    from contentflow import ContentGenerator
    gen = ContentGenerator()
    for cat in ["Adventure", "Luxury", "Family", "Culture", "Mindset"]:
        q = gen.get_travel_quote(cat)
        assert isinstance(q, str)
        assert len(q) > 10

    # Unknown category → fallback
    q = gen.get_travel_quote("Unknown")
    assert isinstance(q, str)


def test_multilanguage():
    from contentflow import ContentGenerator
    for lang in ["en", "tr", "de", "fr", "es"]:
        gen = ContentGenerator(language=lang)
        content = gen.generate("digital marketing", platform="instagram")
        assert isinstance(content, str)
        assert len(content) > 5


# ── ContentCalendar ────────────────────────────────────────────────────────────

def test_content_calendar_generate_week():
    from contentflow import ContentCalendar
    cal = ContentCalendar()
    week = cal.generate_week("machine learning", platforms=["linkedin", "twitter"])
    assert len(week.posts) > 0
    for post in week.posts:
        assert post.platform in ("linkedin", "twitter")
        assert isinstance(post.content, str)
        assert len(post.content) > 5


def test_content_calendar_to_dict():
    from contentflow import ContentCalendar
    cal = ContentCalendar()
    week = cal.generate_week("startup", platforms=["instagram"])
    data = week.to_dict()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "content" in data[0]


def test_content_calendar_generate_month():
    from contentflow import ContentCalendar
    cal = ContentCalendar()
    weeks = cal.generate_month(["AI", "marketing"], platforms=["twitter"])
    assert len(weeks) == 4


# ── SEOOptimizer ──────────────────────────────────────────────────────────────

def test_seo_generate_meta():
    from contentflow import SEOOptimizer
    seo = SEOOptimizer()
    bundle = seo.generate_meta("Istanbul travel guide 2026")
    assert isinstance(bundle.title, str)
    assert len(bundle.title) <= 60
    assert len(bundle.description) <= 160
    assert isinstance(bundle.keywords, list)
    assert len(bundle.slug) > 0


def test_seo_generate_blog_outline():
    from contentflow import SEOOptimizer
    seo = SEOOptimizer()
    outline = seo.generate_blog_outline("Top AI tools for small business", sections=5)
    assert len(outline) == 5
    for section in outline:
        assert isinstance(section, str)
        assert len(section) > 5


def test_seo_generate_title_styles():
    from contentflow import SEOOptimizer
    seo = SEOOptimizer()
    for style in ["guide", "how-to", "list", "question", "comparison"]:
        title = seo.generate_title("Python testing", style=style)
        assert isinstance(title, str)
        assert "Python" in title

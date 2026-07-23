"""Tests for ContentFlow v1.2.0."""

import pytest


def test_version():
    import contentflow
    assert contentflow.__version__ == "1.2.0"


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


# ── ContentScore __str__ ──────────��────────────────────────────────────────────

def test_content_score_str():
    from contentflow import ContentGenerator
    gen = ContentGenerator()
    content = gen.generate("AI tools", platform="instagram")
    score = gen.score_content(content, platform="instagram")
    s = str(score)
    assert "ContentScore" in s
    assert "readability" in s


# ── generate() extra platforms ───���──────────────────────────────��──────────────

def test_generate_sms_push():
    from contentflow import ContentGenerator
    gen = ContentGenerator()
    for platform in ["sms", "push"]:
        content = gen.generate("flash sale", platform=platform)
        assert isinstance(content, str)
        assert len(content) > 5


# ── score_content edge cases ───────────────────────────────────��──────────────

def test_score_content_all_platforms():
    from contentflow import ContentGenerator
    gen = ContentGenerator()
    for platform in ["instagram", "linkedin", "twitter", "tiktok", "email", "blog"]:
        content = gen.generate("news", platform=platform)
        score = gen.score_content(content, platform=platform)
        assert 0.0 <= score.overall <= 1.0


def test_score_content_short_long():
    from contentflow import ContentGenerator
    gen = ContentGenerator()
    score_short = gen.score_content("Hi!", platform="twitter")
    score_long = gen.score_content("x " * 500, platform="twitter")
    assert 0.0 <= score_short.length_fit <= 1.0
    assert 0.0 <= score_long.length_fit <= 1.0


# ── ContentCalendar __str__ ────────────────────��──────────────────────────────

def test_scheduled_post_str():
    from contentflow import ContentCalendar
    cal = ContentCalendar()
    week = cal.generate_week("cooking", platforms=["instagram"])
    post = week.posts[0]
    s = str(post)
    assert "instagram" in s.lower() or "INSTAGRAM" in s


# ── SEO meta unknown style ──────────────────────────────────────���─────────────

def test_seo_generate_title_unknown_style():
    from contentflow import SEOOptimizer
    seo = SEOOptimizer()
    title = seo.generate_title("python", style="unknown")
    assert isinstance(title, str)


# ── ContentWeek __repr__ ───────────────────────────────────────────────────────

def test_content_week_repr():
    from contentflow import ContentCalendar
    cal = ContentCalendar()
    week = cal.generate_week("travel", platforms=["instagram"])
    r = repr(week)
    assert "ContentWeek" in r


# ── ContentGenerator language templates (non-en) ──────────────────────────────

def test_generate_language_template_tr():
    """Hit the language-template branch in _template_generate."""
    from contentflow import ContentGenerator
    gen = ContentGenerator(language="tr")
    content = gen.generate("dijital pazarlama", platform="instagram")
    assert isinstance(content, str)
    assert len(content) > 5


# ── _ai_generate fallback (bad API key) ───────────────────────────────────────

def test_ai_generate_fallback_on_bad_key():
    """_ai_generate falls back to template when API errors."""
    from contentflow import ContentGenerator
    gen = ContentGenerator(api_key="bad_test_key_xxx")
    content = gen.generate("AI tools", platform="linkedin", tone="professional")
    assert isinstance(content, str)
    assert len(content) > 5


# ── A/B Variant Generator ─────────────────────────────────────────────────────

def test_generate_ab_variants_returns_two_variants():
    from contentflow import ContentGenerator
    cg = ContentGenerator(brand_voice="startup")
    result = cg.generate_ab_variants("AI automation", platform="instagram", hashtag_category="tech")
    assert "variant_a" in result
    assert "variant_b" in result
    assert "scores" in result
    assert len(result["variant_a"]) > 10
    assert len(result["variant_b"]) > 10


def test_generate_ab_variants_scores():
    from contentflow import ContentGenerator
    cg = ContentGenerator(brand_voice="friendly")
    result = cg.generate_ab_variants("startup growth", platform="linkedin")
    scores = result["scores"]
    assert 0.0 <= scores["a"].overall <= 1.0
    assert 0.0 <= scores["b"].overall <= 1.0


def test_generate_ab_variants_differ():
    from contentflow import ContentGenerator
    cg = ContentGenerator(brand_voice="minimal")
    result = cg.generate_ab_variants("machine learning", platform="twitter")
    assert result["variant_a"] != result["variant_b"]

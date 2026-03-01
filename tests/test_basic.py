"""Basic tests for ContentFlow package."""

import pytest


def test_import():
    """Test that contentflow can be imported."""
    import contentflow
    assert hasattr(contentflow, "__version__")
    assert contentflow.__version__ == "0.4.0"


def test_content_generator_import():
    """Test ContentGenerator class import."""
    from contentflow import ContentGenerator
    gen = ContentGenerator()
    assert gen is not None


def test_generate_ad_copy_template():
    """Test template-based ad copy generation."""
    from contentflow import ContentGenerator

    gen = ContentGenerator()  # No API key = template mode
    copy = gen.generate_ad_copy("Istanbul", vibe="exciting", platform="Instagram")
    assert isinstance(copy, str)
    assert len(copy) > 0
    assert "Istanbul" in copy


def test_get_travel_quote():
    """Test travel quote retrieval."""
    from contentflow import ContentGenerator

    gen = ContentGenerator()
    quote = gen.get_travel_quote("Adventure")
    assert isinstance(quote, str)
    assert len(quote) > 0


def test_get_travel_quote_fallback():
    """Test travel quote with unknown category falls back to Adventure."""
    from contentflow import ContentGenerator

    gen = ContentGenerator()
    quote = gen.get_travel_quote("Unknown")
    assert isinstance(quote, str)
    assert len(quote) > 0

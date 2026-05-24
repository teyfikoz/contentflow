# ContentFlow

**Multi-platform AI marketing content generator** — Instagram, LinkedIn, Twitter, TikTok, Email, Blog, SEO. Works offline with curated templates or online with HuggingFace AI.

[![PyPI version](https://badge.fury.io/py/contentflow.svg)](https://pypi.org/project/contentflow/)
[![CI](https://github.com/teyfikoz/contentflow/actions/workflows/ci.yml/badge.svg)](https://github.com/teyfikoz/contentflow/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

```bash
pip install contentflow
```

## Quick Start

```python
from contentflow import ContentGenerator

gen = ContentGenerator()

# Generate platform-specific content
post = gen.generate("AI productivity tools", platform="linkedin", tone="professional")
print(post)

# Instagram ad copy for travel
copy = gen.generate_ad_copy("Istanbul", vibe="romantic", platform="Instagram")
print(copy)
```

---

## Features at a Glance

| Feature | Description |
|---------|-------------|
| `ContentGenerator` | Multi-platform content — 8 platforms, 5 brand voices, 5 languages |
| `ContentCalendar` | Weekly + monthly content calendars with auto-scheduling |
| `SEOOptimizer` | Meta tags, titles, blog outlines, keyword extraction |
| `score_content()` | Readability, engagement, hashtag quality, length fit scoring |
| `batch_generate()` | Generate content for multiple topics at once |
| **AI mode** | Optional HuggingFace Inference API (flan-t5-large) |
| **Offline mode** | 100% offline with 50+ curated templates |

---

## ContentGenerator — 8 Platforms

```python
from contentflow import ContentGenerator

gen = ContentGenerator(brand_voice="startup")

platforms = ["instagram", "linkedin", "twitter", "tiktok", "email", "blog", "sms", "push"]
for platform in platforms:
    content = gen.generate("product launch", platform=platform, tone="exciting")
    print(f"[{platform.upper()}]", content[:80], "\n")
```

### Brand Voices

```python
# Available: startup | enterprise | creative | minimal | friendly
gen_corp   = ContentGenerator(brand_voice="enterprise")
gen_fun    = ContentGenerator(brand_voice="creative")
gen_clean  = ContentGenerator(brand_voice="minimal")

post = gen_corp.generate("quarterly results", platform="linkedin", tone="professional")
```

### Multi-language Support

```python
gen_tr = ContentGenerator(language="tr")
gen_de = ContentGenerator(language="de")
gen_fr = ContentGenerator(language="fr")
gen_es = ContentGenerator(language="es")

tr_post = gen_tr.generate("dijital pazarlama", platform="instagram")
de_post = gen_de.generate("Digitales Marketing", platform="linkedin")
```

### Batch Generation

```python
results = gen.batch_generate(
    topics=["Paris", "Tokyo", "Istanbul", "New York"],
    platform="instagram",
    tone="adventurous",
)
for r in results:
    print(f"{r['topic']}: {r['content'][:60]}...")
```

### Content Scoring

```python
content = gen.generate("AI startup funding", platform="linkedin")
score = gen.score_content(content, platform="linkedin")

print(f"Readability:  {score.readability:.0%}")
print(f"Engagement:   {score.engagement:.0%}")
print(f"Hashtags:     {score.hashtag_quality:.0%}")
print(f"Length fit:   {score.length_fit:.0%}")
print(f"Overall:      {score.overall:.0%}")
```

### AI Mode (HuggingFace)

```python
import os
os.environ["HF_API_TOKEN"] = "hf_your_token_here"

gen = ContentGenerator()  # auto-reads HF_API_TOKEN
ai_copy = gen.generate("sustainable fashion brand", platform="instagram", tone="authentic")
```

---

## ContentCalendar — Weekly & Monthly Scheduling

```python
from contentflow import ContentCalendar

cal = ContentCalendar()

# One week of content across platforms
week = cal.generate_week(
    topic="machine learning for marketers",
    platforms=["linkedin", "twitter", "instagram"],
)

print(f"Generated {len(week.posts)} posts")
for post in week.posts:
    print(f"  {post.day:10s} | {post.platform:10s} | {post.content[:60]}...")

# Export to dict (e.g. for a CMS or Notion API)
data = week.to_dict()
```

### Monthly Calendar

```python
weeks = cal.generate_month(
    topics=["AI tools", "productivity hacks", "startup lessons", "remote work"],
    platforms=["linkedin", "twitter"],
)

for i, week in enumerate(weeks, 1):
    print(f"Week {i}: {len(week.posts)} posts scheduled")
```

---

## SEOOptimizer — Meta Tags & Blog Outlines

```python
from contentflow import SEOOptimizer

seo = SEOOptimizer()

# Full meta bundle
bundle = seo.generate_meta(
    "Istanbul travel guide 2026",
    keywords=["Istanbul", "Turkey travel", "things to do in Istanbul"],
)
print(bundle)
# <title>Istanbul travel guide 2026 — Complete Guide for 2026</title>
# <meta name="description" content="...">
# <meta name="keywords" content="...">

# SEO title variants
print(seo.generate_title("Istanbul travel guide", style="how-to"))
print(seo.generate_title("Istanbul travel guide", style="list"))
print(seo.generate_title("Istanbul travel guide", style="question"))

# Blog post outline
outline = seo.generate_blog_outline("Top 10 AI tools for small businesses", sections=6)
for i, section in enumerate(outline, 1):
    print(f"{i}. {section}")
```

---

## Full Pipeline Example

```python
from contentflow import ContentGenerator, ContentCalendar, SEOOptimizer

brand = "TechStartup AI"
topic = "AI-powered customer service"

gen = ContentGenerator(brand_voice="startup", language="en")
cal = ContentCalendar(generator=gen)
seo = SEOOptimizer()

# Generate & score a LinkedIn post
post = gen.generate(topic, platform="linkedin", tone="professional")
score = gen.score_content(post, platform="linkedin")
print(f"Post score: {score.overall:.0%}\n{post}\n")

# Generate one week of content
week = cal.generate_week(topic, platforms=["linkedin", "twitter", "instagram"])
print(f"Scheduled {len(week.posts)} posts\n")

# SEO bundle for blog
bundle = seo.generate_meta(topic, keywords=["AI", "customer service", "automation"])
outline = seo.generate_blog_outline(f"How {topic} is changing business in 2026")
print(bundle.title)
for section in outline:
    print(" →", section)
```

---

## Travel Quotes (Backward Compat)

```python
gen = ContentGenerator()
print(gen.get_travel_quote("Adventure"))   # Amelia Earhart, Tolkien, Oprah...
print(gen.get_travel_quote("Culture"))     # Mark Twain, Saint Augustine...
print(gen.get_travel_quote("Mindset"))     # Hans Christian Andersen...
```

---

## License

MIT — [Teyfik Öz](https://github.com/teyfikoz)

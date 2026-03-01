# ContentFlow

AI Marketing Content Generator.

[![PyPI version](https://badge.fury.io/py/contentflow.svg)](https://pypi.org/project/contentflow/)
[![CI](https://github.com/teyfikoz/contentflow/actions/workflows/ci.yml/badge.svg)](https://github.com/teyfikoz/contentflow/actions/workflows/ci.yml)

## Installation

```bash
pip install contentflow
```

## Quick Start

```python
from contentflow import ContentGenerator

gen = ContentGenerator()

# Generate ad copy (template-based, no API key needed)
copy = gen.generate_ad_copy("Istanbul", vibe="exciting", platform="Instagram")
print(copy)

# Get a travel quote
quote = gen.get_travel_quote("Adventure")
print(quote)

# With HuggingFace API (optional)
gen = ContentGenerator(api_key="hf_...")
copy = gen.generate_ad_copy("Paris", vibe="romantic")
```

## Features

- **Template-based content** - Works offline with curated templates
- **AI-powered generation** - Optional HuggingFace Inference API integration
- **Travel quotes** - Categorized famous travel quotes

## License

MIT

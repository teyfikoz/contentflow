import os
import random
from typing import Optional

import requests


class ContentGenerator:
    """
    Generates marketing copy using AI or templates.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("HF_API_TOKEN")
        self.api_url = "https://api-inference.huggingface.co/models/google/flan-t5-large"

    def generate_ad_copy(self, destination: str, vibe: str = "exciting", platform: str = "Instagram") -> str:
        """
        Generate a short ad copy for a destination.
        """
        if self.api_key:
            return self._generate_ai(destination, vibe, platform)
        return self._generate_template(destination, vibe, platform)

    def _generate_template(self, destination: str, vibe: str, platform: str) -> str:
        templates = [
            f"{destination} is calling! Experience a {vibe} adventure filled with history and flavor. Book your dream trip today! ✈️ #{destination} #Travel",
            f"Discover the {vibe} magic of {destination} for your next {platform} story! 🌟",
            f"Escape to {destination}. It's simply {vibe}. Check our bio for deals! 🌴",
        ]
        return random.choice(templates)

    def _generate_ai(self, destination: str, vibe: str, platform: str) -> str:
        prompt = f"Write a catchy {platform} marketing slogan for visiting {destination}. The vibe should be {vibe}."
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.post(self.api_url, headers=headers, json={"inputs": prompt})
            result = response.json()
            if isinstance(result, list) and 'generated_text' in result[0]:
                return result[0]['generated_text']
            return self._generate_template(destination, vibe, platform)
        except Exception:
            return self._generate_template(destination, vibe, platform)

    def get_travel_quote(self, category: str = "Adventure") -> str:
        """
        Get a famous travel quote based on category.
        """
        quotes = {
            "Adventure": [
                "\"Adventure is worthwhile in itself.\" - Amelia Earhart",
                "\"Life is either a daring adventure or nothing at all.\" - Helen Keller"
            ],
            "Luxury": [
                "\"Luxury is the ease of a t-shirt in a very expensive dress.\" - Karl Lagerfeld",
                "\"The best things in life are free. The second best are very expensive.\" - Coco Chanel"
            ],
            "Family": [
                "\"The greatest legacy we can leave our children is happy memories.\" - Og Mandino"
            ]
        }
        category_quotes = quotes.get(category, quotes["Adventure"])
        return random.choice(category_quotes)

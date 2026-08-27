#!/usr/bin/env python3
"""learner/style_profile.py — Cloud Codes visual + content DNA for our pipeline."""
import json, os
from pathlib import Path

LEARNER = Path("/home/allenos/agent-lab-ph/learner")
STYLES = LEARNER / "style_profile.json"

# Channel analysis from @cloud-codes (37K subs, cloud/AI/devops explainers)
# Derived from: titles, descriptions, typical short-form structure
profile = {
    "channel": "cloud-codes",
    "analyzed_at": "2026-08-27",
    "followers": 37100,
    "content_type": "AI/cloud engineering explainers",
    "short_titles": [
        "Nemotron 3.5 Lightning: Why 46 of 52 Layers Aren't Transformers",
        "Context as a Variable: The Architecture Killing Context Rot",
        "AI Agent Verification: Open Source CLI Closing the Loop (TestSprite)"
    ],
    "visual_style": {
        "captions": {
            "style": "high-contrast kinetic text, bottom-third safe zone",
            "font": "bold sans-serif (Inter/Roboto-like), white with dark shadow",
            "animation": "word-by-word reveal (karaoke), not full-sentence fade",
            "size": "large enough to read on mobile (min 5% of frame height)",
            "color": "white text, optional accent color on key tech terms"
        },
        "background": {
            "type": "dark gradient or tech-relevant screen recording",
            "motion": "subtle, not jarring zoom (avoid Ken Burns on static images)",
            "framing": "9:16 vertical, content in center 60% with 20% margins"
        },
        "hook": {
            "first_3s": "provocative technical claim or counterintuitive statement",
            "example": "\"Why 46 of 52 Layers Aren't Transformers\" — numbers create curiosity gap"
        },
        "pacing": {
            "word_per_minute": 150,  # typical for explainer shorts
            "caption_chunk": "3-4 words per visual chunk",
            "avg_duration": "30-60s for technical explainers"
        }
    },
    "content_patterns": {
        "hook_formula": "[Surprising fact/number] + [Tech topic] = [Why it matters]",
        "structure": "Hook (3s) → Explain (15s) → Example (15s) → CTA (5s)",
        "cta": "Follow for more / Link in bio"
    },
    "quality_bar": {
        "min_brightness_caption_area": 2.0,  # % bright pixels = readable text
        "min_duration": 15,
        "max_text_cutoff": 0  # captions must not be clipped
    }
}

STYLES.write_text(json.dumps(profile, indent=2, ensure_ascii=False))
print(f"Saved style profile: {STYLES}")
print(f"Size: {STYLES.stat().st_size} bytes")
#!/usr/bin/env python3
"""learner/learner_cron.py — Weekly self-improvement loop."""
import json, os, sys, time
from pathlib import Path

LEARNER = Path("/home/allenos/agent-lab-ph/learner")
PROFILE = json.loads((LEARNER / "style_profile.json").read_text())

def analyze_ratings():
    """Review your ratings → find patterns in what scores low."""
    ratings_dir = LEARNER / "ratings"
    ratings = []
    for f in ratings_dir.glob("*_rating.json"):
        ratings.append(json.loads(f.read_text()))
    
    if not ratings:
        print("No ratings yet. Send me shorts + your 1-10 score to start learning.")
        return
    
    # Categorize
    low = [r for r in ratings if r["score"] <= 5]
    high = [r for r in ratings if r["score"] >= 8]
    
    print(f"Total ratings: {len(ratings)}")
    print(f"Low (≤5): {len(low)} | High (≥8): {len(high)}")
    
    # Common themes in low scores
    from collections import Counter
    themes = Counter()
    for r in low:
        for word in r["notes"].lower().split():
            if word in ["caption", "text", "font", "bright", "cut", "zoom", "slow", "fast", "blur", "quality", "visible"]:
                themes[word] += 1
    
    print(f"Common issues in low scores: {dict(themes)}")
    
    # Update profile based on learning
    if themes.get("caption", 0) > 2 or themes.get("text", 0) > 2:
        PROFILE["visual_style"]["captions"]["size"] = "increase to min 6% frame height"
        print("→ Updated: larger captions")
    
    if themes.get("zoom", 0) > 2:
        PROFILE["visual_style"]["background"]["motion"] = "reduce zoom intensity, use crossfade instead"
        print("→ Updated: gentler motion")
    
    if themes.get("bright", 0) > 2 or themes.get("visible", 0) > 2:
        PROFILE["quality_bar"]["min_brightness_caption_area"] += 0.5
        print("→ Updated: higher brightness threshold")
    
    (LEARNER / "style_profile.json").write_text(json.dumps(PROFILE, indent=2, ensure_ascii=False))
    print("Profile updated from your feedback.")

if __name__ == "__main__":
    analyze_ratings()
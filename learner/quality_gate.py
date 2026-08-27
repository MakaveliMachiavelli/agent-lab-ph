#!/usr/bin/env python3
"""learner/quality_gate.py — Self-healing quality checker + improvement loop."""
import json, os, subprocess, sys
from pathlib import Path

LEARNER = Path("/home/allenos/agent-lab-ph/learner")
PROFILE = json.loads((LEARNER / "style_profile.json").read_text())
RATINGS_DIR = LEARNER / "ratings"

def check_brightness(video_path: str) -> float:
    """Check % bright pixels in caption area (proxy for readable text)."""
    try:
        result = subprocess.run([
            "python3", "-c",
            f"""
from PIL import Image
import subprocess
f = "{video_path}"
# Extract middle frame
subprocess.run(["ffmpeg", "-y", "-i", f, "-vf", "select=eq(n\\\\,30)", "-vframes", "1", "/tmp/_q.jpg"], stderr=subprocess.DEVNULL)
a = Image.open("/tmp/_q.jpg").convert("L")
bright = sum(1 for p in a.getdata() if p > 200)
print(round(bright / len(list(a.getdata())) * 100, 2))
"""
        ], capture_output=True, text=True, timeout=30)
        return float(result.stdout.strip())
    except Exception:
        return 0.0

def check_duration(video_path: str) -> float:
    """Get video duration in seconds."""
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", video_path
        ], capture_output=True, text=True, timeout=30)
        return float(result.stdout.strip())
    except Exception:
        return 0.0

def self_heal(video_path: str) -> dict:
    """Analyze video quality against learned profile. Return issues + fixes."""
    issues = []
    fixes = []
    
    brightness = check_brightness(video_path)
    min_bright = PROFILE["quality_bar"]["min_brightness_caption_area"]
    
    if brightness < min_bright:
        issues.append(f"Caption brightness {brightness}% < {min_bright}% threshold")
        fixes.append("Increase font size or add stronger text shadow")
    
    duration = check_duration(video_path)
    if duration < PROFILE["quality_bar"]["min_duration"]:
        issues.append(f"Duration {duration}s < {PROFILE['quality_bar']['min_duration']}s")
        fixes.append("Slow TTS or add more content")
    
    return {
        "video": video_path,
        "brightness": brightness,
        "duration": duration,
        "issues": issues,
        "fixes": fixes,
        "passed": len(issues) == 0
    }

def save_rating(video_path: str, score: int, notes: str):
    """Save Allen's rating for continuous learning."""
    RATINGS_DIR.mkdir(exist_ok=True)
    rating_file = RATINGS_DIR / f"{Path(video_path).stem}_rating.json"
    rating = {
        "video": video_path,
        "score": score,  # 1-10
        "notes": notes,
        "timestamp": time.time()
    }
    rating_file.write_text(json.dumps(rating, indent=2))
    print(f"Saved rating: {rating_file}")

def improve_from_ratings():
    """Aggregate ratings → update style_profile.json."""
    ratings = []
    for f in RATINGS_DIR.glob("*_rating.json"):
        ratings.append(json.loads(f.read_text()))
    
    if not ratings:
        return
    
    avg = sum(r["score"] for r in ratings) / len(ratings)
    
    # If avg < 7, tighten quality bar
    if avg < 7:
        PROFILE["quality_bar"]["min_brightness_caption_area"] += 0.5
        PROFILE["quality_bar"]["min_duration"] += 3
        (LEARNER / "style_profile.json").write_text(json.dumps(PROFILE, indent=2))
        print(f"Improved quality bar based on avg rating {avg:.1f}")

if __name__ == "__main__":
    import time
    if len(sys.argv) > 1:
        if sys.argv[1] == "check":
            result = self_heal(sys.argv[2])
            print(json.dumps(result, indent=2))
        elif sys.argv[1] == "rate":
            save_rating(sys.argv[2], int(sys.argv[3]), " ".join(sys.argv[4:]))
        elif sys.argv[1] == "improve":
            improve_from_ratings()
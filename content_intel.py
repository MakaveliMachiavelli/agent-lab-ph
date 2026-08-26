#!/usr/bin/env python3
"""content_intel.py — AI Content Intelligence Agent
Monitors competitor channels, analyzes top content, generates fresh scripts,
produces via pipeline, auto-posts via Composio.
"""
import json, subprocess, os, re, time
from datetime import datetime, timedelta
from pathlib import Path

# Config
NICHE_KEYWORDS = [
    "Oracle Cloud Free Tier", "AI automation Philippines", "freelance Philippines",
    "work from home PH", "BPO career", "virtual assistant PH", "online jobs PH",
    "make money online Philippines", "passive income PH", "side hustle PH"
]

COMPETITOR_CHANNELS = [
    # These would be real channels - for now using search-based approach
]

OUTPUT_DIR = Path("/home/allenos/agent-lab-ph/scripts_in")
ARCHIVE_DIR = Path("/home/allenos/agent-lab-ph/content_intel_archive")
ARCHIVE_DIR.mkdir(exist_ok=True)

def search_youtube(keyword, max_results=5):
    """Search YouTube for recent videos on keyword."""
    cmd = [
        "yt-dlp", "--flat-playlist", "--print-json",
        f"ytsearch{max_results}:{keyword} Philippines 2024",
        "--skip-download"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    v = json.loads(line)
                    videos.append({
                        'title': v.get('title', ''),
                        'url': v.get('url', ''),
                        'view_count': v.get('view_count', 0),
                        'duration': v.get('duration', 0),
                        'uploader': v.get('uploader', ''),
                        'upload_date': v.get('upload_date', ''),
                    })
                except:
                    pass
        return videos
    except Exception as e:
        print(f"Search error for {keyword}: {e}")
        return []

def get_video_transcript(url):
    """Get transcript via yt-dlp."""
    cmd = ["yt-dlp", "--write-auto-sub", "--sub-lang", "en", 
           "--skip-download", "--sub-format", "vtt", "-o", "/tmp/%(id)s.%(ext)s", url]
    try:
        subprocess.run(cmd, capture_output=True, timeout=60)
        # Find the vtt file
        for f in Path("/tmp").glob("*.vtt"):
            text = f.read_text()
            f.unlink()
            # Parse VTT to plain text
            lines = text.split('\n')
            content = []
            for l in lines:
                if '-->' not in l and l.strip() and not l.startswith('WEBVTT'):
                    content.append(l.strip())
            return ' '.join(content)
    except Exception as e:
        print(f"Transcript error: {e}")
    return ""

def analyze_content_gaps(videos, keyword):
    """Use AI to analyze what's missing / fresh angles."""
    # For now, generate structured angles based on keyword
    angles = {
        "Oracle Cloud Free Tier": [
            "The hidden 7-day rule that kills your free instance",
            "Why Ashburn region is a trap — use Osaka instead",
            "Real credit card vs GCash: why virtual cards fail",
            "My 6-month Oracle Free Tier survival log",
        ],
        "AI automation Philippines": [
            "How I automated my OnlineJobs.ph applications",
            "Building a ₱0 AI agent stack on free Oracle cloud",
            "From BPO agent to AI automation builder — the roadmap",
        ],
        "freelance Philippines": [
            "How I charge $50/hr from PH — real client proof",
            "The Upwork profile hack that got me 3 clients in 1 week",
            "Filipino freelancer tax guide 2024 — simple version",
        ],
        "BPO career": [
            "Why I returned to WNS after 2 years — the real story",
            "Accenture vs WNS vs Concentrix — where to apply in 2024",
            "BPO to freelance transition: my exact 90-day plan",
        ],
    }
    return angles.get(keyword, [f"Fresh take on {keyword} for Filipinos"])

def generate_script(keyword, angle, competitor_insights):
    """Generate a script for the watch_daemon pipeline."""
    templates = {
        "hook": f"Stop doing {keyword.lower()} the wrong way. ",
        "body": f"Here's what {len(competitor_insights)} top videos missed: ",
        "cta": "Follow for more Philippines tech/freelance reality checks."
    }
    
    # Mix hook + angle + body + cta
    script = f"{templates['hook']}{angle}. {templates['body']}Most creators show the happy path. I show the traps. {templates['cta']}"
    return script

def save_script(script, keyword, angle):
    """Save as .txt for watch_daemon to process."""
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', f"{keyword}_{angle}")[:80]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{safe_name}_{timestamp}.txt"
    filepath = OUTPUT_DIR / filename
    filepath.write_text(script)
    print(f"Created: {filepath}")
    return filepath

def run_intel_cycle():
    """Main intelligence cycle."""
    print(f"[{datetime.now()}] Starting content intel cycle...")
    
    all_scripts = []
    for keyword in NICHE_KEYWORDS:
        print(f"  Researching: {keyword}")
        videos = search_youtube(keyword, max_results=3)
        if not videos:
            continue
            
        angles = analyze_content_gaps(videos, keyword)
        for angle in angles[:2]:  # Top 2 angles per keyword
            script = generate_script(keyword, angle, videos)
            filepath = save_script(script, keyword, angle)
            all_scripts.append({
                'file': str(filepath),
                'keyword': keyword,
                'angle': angle,
                'script': script[:100] + "..."
            })
    
    # Archive this cycle
    archive_file = ARCHIVE_DIR / f"intel_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    archive_file.write_text(json.dumps(all_scripts, indent=2))
    print(f"Cycle complete. {len(all_scripts)} scripts queued.")
    return all_scripts

if __name__ == "__main__":
    run_intel_cycle()
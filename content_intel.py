#!/usr/bin/env python3
"""content_intel.py v2 — Research only, no auto-production. Flags for human review."""
import subprocess, os, json, re, time
from pathlib import Path

BASE = Path("/home/allenos/agent-lab-ph")
SCRIPTS_DIR = BASE / "scripts_review"
SCRIPTS_DIR.mkdir(exist_ok=True)

NICHES = [
    ("Oracle Cloud Free Tier", "Oracle Cloud free tier tutorial Philippines site:youtube.com"),
    ("AI automation Philippines", "AI automation Philippines freelance site:youtube.com"),
    ("freelance Philippines", "freelance Philippines Upwork tips site:youtube.com"),
    ("work from home PH", "work from home Philippines 2024 site:youtube.com"),
    ("BPO career", "BPO career Philippines Accenture WNS site:youtube.com"),
    ("virtual assistant PH", "virtual assistant Philippines salary site:youtube.com"),
    ("online jobs PH", "online jobs Philippines legit site:youtube.com"),
    ("make money online Philippines", "make money online Philippines legitimate site:youtube.com"),
    ("passive income PH", "passive income Philippines 2024 site:youtube.com"),
    ("side hustle PH", "side hustle Philippines students site:youtube.com"),
]

def research_niche(topic, query):
    try:
        result = subprocess.run([
            "/home/allenos/.local/bin/yt-dlp",
            "--flat-playlist",
            "--dump-json",
            f"ytsearch5:{query}",
        ], capture_output=True, text=True, timeout=60)
        
        videos = []
        for line in result.stdout.strip().split("\n"):
            if line:
                try:
                    v = json.loads(line)
                    videos.append({
                        "title": v.get("title", ""),
                        "url": v.get("url", ""),
                        "views": v.get("view_count", 0),
                        "duration": v.get("duration", 0),
                    })
                except:
                    pass
        return videos
    except Exception as e:
        print(f"  Error researching {topic}: {e}")
        return []

def generate_script_idea(topic, videos):
    angles = {
        "Oracle Cloud Free Tier": [
            "The hidden 7-day rule that kills your free instance",
            "Why Ashburn region is a trap — use Osaka instead",
            "How I got 2 OCPU + 12GB RAM free (not 24GB)"
        ],
        "AI automation Philippines": [
            "How I automated my OnlineJobs.ph applications",
            "Building a zero-peso AI agent stack on free Oracle cloud",
            "Replacing Upwork proposals with AI agents"
        ],
        "freelance Philippines": [
            "How I charge 50 dollars/hr from PH — real client proof",
            "The Upwork profile hack that got me 3 clients in 1 week",
            "From BPO to 5k per month freelance — exact roadmap"
        ],
        "BPO career": [
            "Why I returned to WNS after 2 years — the real story",
            "Accenture vs WNS vs Concentrix — where to apply in 2024",
            "How to explain your BPO gap in tech interviews"
        ],
    }
    
    topic_angles = angles.get(topic, [f"Fresh take on {topic} for Filipinos"])
    return topic_angles[0]

def main():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting content intel cycle...")
    print("Mode: RESEARCH ONLY -> saves to scripts_review/ for manual approval")
    
    for topic, query in NICHES:
        print(f"  Researching: {topic}")
        videos = research_niche(topic, query)
        if not videos:
            continue
        
        angle = generate_script_idea(topic, videos)
        
        safe_topic = re.sub(r'[^a-zA-Z0-9]+', '_', topic)
        safe_angle = re.sub(r'[^a-zA-Z0-9]+', '_', angle)
        filename = f"{safe_topic}_{safe_angle}_{time.strftime('%Y%m%d_%H%M')}.txt"
        
        content = f"""TOPIC: {topic}
ANGLE: {angle}
COMPETITOR COUNT: {len(videos)}
TOP COMPETITORS:
{chr(10).join(f"- {v['title'][:80]} ({v['views']} views)" for v in videos[:3])}

SCRIPT OUTLINE:
[Hook] {angle}
[Body] Your unique experience/process
[CTA] Follow for more free PH tech tips

NOTES: 
- Write in Taglish, conversational tone
- Target 45-60 seconds spoken
- Include specific numbers/steps
- End with clear CTA
"""
        (SCRIPTS_DIR / filename).write_text(content)
        print(f"    Wrote review script: {filename}")
    
    print(f"\nCycle complete. Review scripts in {SCRIPTS_DIR}")
    print("When ready: copy to scripts_in/ for production")

if __name__ == "__main__":
    main()
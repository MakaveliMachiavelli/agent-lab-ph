#!/usr/bin/env python3
"""auto_poster.py v3 — Correct schemas for TikTok + Facebook."""
import subprocess, os, json, glob, time
from pathlib import Path

COMPOSIO = os.path.expanduser("~/.local/bin/composio")
GITHUB_RAW = "https://raw.githubusercontent.com/MakaveliMachiavelli/agent-lab-ph/master/shorts/"
SHORTS_DIR = Path("/home/allenos/agent-lab-ph/shorts")
POSTED_LOG = Path("/home/allenos/agent-lab-ph/.posted_videos.json")
FB_PAGE_ID = "1238353069365061"

def load_posted():
    if POSTED_LOG.exists():
        return set(json.loads(POSTED_LOG.read_text()).get("posted", []))
    return set()

def save_posted(posted):
    POSTED_LOG.write_text(json.dumps({"posted": list(posted)}, indent=2))

def run_composio(args):
    env = dict(os.environ)
    env["PATH"] = os.path.expanduser("~/.composio/bin") + ":" + env["PATH"]
    result = subprocess.run(
        [COMPOSIO] + args, capture_output=True, text=True, timeout=120, env=env
    )
    return result.stdout + result.stderr

def generate_caption(filename):
    name = filename.replace(".mp4", "").rsplit("_", 1)[0]
    text = name.replace("_", " ").title()
    return f"{text} | Free PH tech & freelance tips 🇵🇭 #AIautomation #freelancePH #OracleCloud #BPO #WorkFromHomePH"

def auto_post_cycle():
    posted = load_posted()
    new_videos = [v for v in glob.glob(str(SHORTS_DIR / "*.mp4")) 
                  if Path(v).name not in posted 
                  and not v.endswith("remotion.mp4")]
    
    results = []
    for video in new_videos[:3]:
        name = Path(video).name
        raw_url = GITHUB_RAW + name
        caption = generate_caption(name)
        
        # Facebook Page video post (correct schema: title, video, page_id, published)
        try:
            fb_args = ["execute", "FACEBOOK_CREATE_VIDEO_POST", "-d", json.dumps({
                "page_id": FB_PAGE_ID,
                "title": caption[:100],
                "video": raw_url,
                "published": True
            })]
            result = run_composio(fb_args)
            print(f"  FB: {name} -> {result[:80]}")
        except Exception as e:
            print(f"  FB error: {e}")
        
        # TikTok needs active connection - check and skip if not available
        try:
            tiktok_args = ["execute", "TIKTOK_PUBLISH_VIDEO", "-d", json.dumps({
                "video_url": raw_url,
                "privacy_level": "SELF_ONLY",
                "caption": caption
            })]
            result = run_composio(tiktok_args)
            if "No active connection" in result:
                print(f"  TikTok: SKIPPED (no connection)")
            else:
                print(f"  TikTok: {name} -> {result[:80]}")
        except Exception as e:
            print(f"  TikTok error: {e}")
        
        posted.add(name)
        results.append(name)
        time.sleep(5)
    
    save_posted(posted)
    print(f"Posted {len(results)} videos to Facebook.")
    return results

if __name__ == "__main__":
    auto_post_cycle()
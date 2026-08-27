#!/usr/bin/env python3
"""auto_poster.py v4 — MANUAL APPROVAL REQUIRED. No auto-posting."""
import subprocess, os, json, glob, time
from pathlib import Path

COMPOSIO = os.path.expanduser("~/.local/bin/composio")
GITHUB_RAW = "https://raw.githubusercontent.com/MakaveliMachiavelli/agent-lab-ph/master/shorts/"
SHORTS_DIR = Path("/home/allenos/agent-lab-ph/shorts")
PENDING_DIR = Path("/home/allenos/agent-lab-ph/pending_approval")
POSTED_LOG = Path("/home/allenos/agent-lab-ph/.posted_videos.json")
FB_PAGE_ID = "1238353069365061"

PENDING_DIR.mkdir(exist_ok=True)

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

def create_approval_file(name, raw_url, caption):
    """Create approval file for manual review."""
    approval = {
        "filename": name,
        "video_url": raw_url,
        "caption": caption,
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "pending",
        "platforms": ["facebook", "tiktok"]
    }
    approval_file = PENDING_DIR / f"{name}.json"
    approval_file.write_text(json.dumps(approval, indent=2))
    return approval_file

def auto_approve_cycle():
    """Find new videos and create approval files (NOT posting)."""
    posted = load_posted()
    new_videos = [v for v in glob.glob(str(SHORTS_DIR / "*.mp4")) 
                  if Path(v).name not in posted 
                  and not v.endswith("remotion.mp4")]
    
    results = []
    for video in new_videos[:10]:  # Queue up to 10 for approval
        name = Path(video).name
        raw_url = GITHUB_RAW + name
        caption = generate_caption(name)
        
        approval_file = create_approval_file(name, raw_url, caption)
        print(f"  📋 Queued for approval: {name}")
        results.append(name)
    
    if results:
        print(f"\n✅ {len(results)} videos queued for manual approval in {PENDING_DIR}")
        print("Run with --approve <filename> to post, or review files manually.")
    else:
        print("No new videos to queue.")
    return results

def approve_and_post(filename):
    """Post a specific approved video."""
    approval_file = PENDING_DIR / f"{filename}.json"
    if not approval_file.exists():
        print(f"❌ No approval file for {filename}")
        return False
    
    approval = json.loads(approval_file.read_text())
    if approval["status"] != "pending":
        print(f"❌ Already {approval['status']}: {filename}")
        return False
    
    raw_url = approval["video_url"]
    caption = approval["caption"]
    success = True
    
    # Facebook
    try:
        fb_args = ["execute", "FACEBOOK_CREATE_VIDEO_POST", "-d", json.dumps({
            "page_id": FB_PAGE_ID,
            "title": caption[:100],
            "video": raw_url,
            "published": True
        })]
        result = run_composio(fb_args)
        if "successful" in result and "true" in result.lower():
            print(f"  ✅ Facebook: {filename}")
        else:
            print(f"  ❌ Facebook: {result[:100]}")
            success = False
    except Exception as e:
        print(f"  ❌ Facebook error: {e}")
        success = False
    
    # TikTok (if connected)
    try:
        tiktok_args = ["execute", "TIKTOK_PUBLISH_VIDEO", "-d", json.dumps({
            "video_url": raw_url,
            "privacy_level": "SELF_ONLY",
            "caption": caption
        })]
        result = run_composio(tiktok_args)
        if "No active connection" not in result:
            print(f"  ✅ TikTok: {filename}")
        else:
            print(f"  ⏭️ TikTok: not connected")
    except Exception as e:
        print(f"  TikTok error: {e}")
    
    if success:
        approval["status"] = "posted"
        approval["posted_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        approval_file.write_text(json.dumps(approval, indent=2))
        posted = load_posted()
        posted.add(filename)
        save_posted(posted)
        print(f"✅ Posted and archived: {filename}")
        return True
    return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--approve":
        if len(sys.argv) > 2:
            approve_and_post(sys.argv[2])
        else:
            print("Usage: python3 auto_poster.py --approve <filename>")
    else:
        auto_approve_cycle()
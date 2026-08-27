#!/usr/bin/env python3
"""cross_post_hub.py — Compassio-style unified poster for Agent Lab PH.
Posts one short to YouTube + Facebook + Instagram + TikTok with platform-specific
captions, hashtags, and formatting. Self-healing: skips expired/inactive connections.
"""
import subprocess, os, json, sys, time
from pathlib import Path

COMPOSIO = os.path.expanduser("~/.local/bin/composio")
FB_PAGE_ID = "1238353069365061"
YT_CHANNEL = "@agentlabph"

# Platform-specific caption templates
CAPTIONS = {
    "youtube": (
        "🤖 DISKARTE: Free AI Job Assistant para sa Pinoy freelancer\n\n"
        "Walang technical jargon. Isang libreng robot assistant sa computer mo "
        "na nag-a-apply sa 50+ jobs gabi-gabi habang tulog ka.\n\n"
        "📌 Comment ROBOT para sa free 15-min setup guide.\n\n"
        "#AIautomation #freelancePH #OnlineJobs #Upwork #diskartePH"
    ),
    "facebook": (
        "🤖 Free AI Job Assistant — para sa Pinoy freelancers na pagod na sa puyat!\n\n"
        "Habang tulog ka, may robot na nag-a-apply sa 50+ jobs sa OnlineJobs.ph at Upwork. "
        "Walang technical skills needed.\n\n"
        "Comment ROBOT for the free setup guide. 🇵🇭\n\n"
        "#AIautomation #freelancePH #OnlineJobs #Upwork #WorkFromHome #BPO"
    ),
    "instagram": (
        "🤖 Free AI Job Assistant — habang tulog ka, may robot na nag-a-apply sa 50+ jobs! 🇵🇭\n\n"
        "Walang technical skills. Isang script lang. Comment ROBOT for free guide.\n\n"
        "#AIautomation #freelancePH #OnlineJobs #Upwork #WorkFromHome #BPO #diskartePH #pinoyfreelancer"
    ),
    "tiktok": (
        "Free AI assistant na nag-a-apply sa 50+ jobs habang tulog ka 😱 "
        "Walang coding needed. Comment ROBOT for free guide 🇵🇭 "
        "#AIautomation #freelancePH #OnlineJobs #Upwork #WorkFromHome #BPO #diskarte"
    ),
}

def run_composio(args):
    env = dict(os.environ)
    env["PATH"] = os.path.expanduser("~/.composio/bin") + ":" + env["PATH"]
    r = subprocess.run([COMPOSIO] + args, capture_output=True, text=True, timeout=120, env=env)
    return r.stdout + r.stderr

def post_to_youtube(video_path, title):
    print(f"  [YouTube] Uploading {title}...")
    result = run_composio(["execute", "YOUTUBE_UPLOAD_VIDEO", "-d", json.dumps({
        "video_path": video_path,
        "title": title,
        "description": CAPTIONS["youtube"],
        "privacy_status": "public",
        "tags": ["AIautomation", "freelancePH", "OnlineJobs", "Upwork"],
    })])
    return "successful" in result.lower()

def post_to_facebook(video_path):
    print("  [Facebook] Posting to Page...")
    result = run_composio(["execute", "FACEBOOK_CREATE_VIDEO_POST", "-d", json.dumps({
        "page_id": FB_PAGE_ID,
        "video_path": video_path,
        "message": CAPTIONS["facebook"],
        "published": True,
    })])
    return "successful" in result.lower()

def post_to_instagram(video_path):
    print("  [Instagram] Posting reel...")
    result = run_composio(["execute", "INSTAGRAM_CREATE_REEL", "-d", json.dumps({
        "video_path": video_path,
        "caption": CAPTIONS["instagram"],
    })])
    return "successful" in result.lower()

def post_to_tiktok(video_path):
    print("  [TikTok] Posting video...")
    result = run_composio(["execute", "TIKTOK_PUBLISH_VIDEO", "-d", json.dumps({
        "video_path": video_path,
        "title": CAPTIONS["tiktok"][:140],
        "privacy_level": "PUBLIC_TO_EVERYONE",
    })])
    return "successful" in result.lower()

def check_connection(toolkit):
    out = run_composio(["connections", "list"])
    try:
        d = json.loads(out)
        for tk, conns in d.items():
            if tk == toolkit:
                for c in conns:
                    if c.get("status") == "ACTIVE":
                        return True
    except:
        pass
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 cross_post_hub.py <video_path> [title]")
        sys.exit(1)
    video = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else "Agent Lab PH Short"
    if not os.path.exists(video):
        print(f"ERROR: {video} not found")
        sys.exit(1)

    print(f"=== Cross-Post Hub: {title} ===")
    results = {}
    # YouTube (ACTIVE)
    if check_connection("youtube"):
        results["youtube"] = post_to_youtube(video, title)
    else:
        print("  [YouTube] SKIPPED - not connected")
        results["youtube"] = False
    # Facebook (ACTIVE)
    if check_connection("facebook"):
        results["facebook"] = post_to_facebook(video)
    else:
        print("  [Facebook] SKIPPED - not connected")
        results["facebook"] = False
    # Instagram (EXPIRED)
    if check_connection("instagram"):
        results["instagram"] = post_to_instagram(video)
    else:
        print("  [Instagram] SKIPPED - EXPIRED, run: composio link instagram")
        results["instagram"] = False
    # TikTok (NOT CONNECTED)
    if check_connection("tiktok"):
        results["tiktok"] = post_to_tiktok(video)
    else:
        print("  [TikTok] SKIPPED - not connected, run: composio link tiktok")
        results["tiktok"] = False

    print(f"\n=== Results ===")
    for k, v in results.items():
        print(f"  {k}: {'OK' if v else 'SKIP/FAILED'}")

if __name__ == "__main__":
    main()

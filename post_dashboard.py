#!/usr/bin/env python3
"""
post_dashboard.py — Compassio-style unified view of all Agent Lab PH posts.
Pulls from Facebook Page, YouTube channel, and local log to show everything in one place.
"""
import subprocess, os, json, time
from pathlib import Path
from datetime import datetime

COMPOSIO = os.path.expanduser("~/.local/bin/composio")
FB_PAGE_ID = "1238353069365061"
BASE = Path("/home/allenos/agent-lab-ph")

def run_composio(args):
    env = dict(os.environ)
    env["PATH"] = os.path.expanduser("~/.composio/bin") + ":" + env["PATH"]
    r = subprocess.run([COMPOSIO] + args, capture_output=True, text=True, timeout=120, env=env)
    return r.stdout + r.stderr

def get_facebook_posts():
    out = run_composio(["proxy", f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/videos?fields=id,title,created_time,permalink_url&limit=10", "--toolkit", "facebook"])
    try:
        d = json.loads(out)
        return [{"platform": "Facebook", "title": v.get("title", "N/A")[:60], "url": f"https://facebook.com{v.get('permalink_url','')}", "created": v.get("created_time", "")} for v in d.get("data", [])]
    except:
        return []

def get_youtube_posts():
    out = run_composio(["execute", "YOUTUBE_GET_CHANNEL_VIDEOS", "-d", json.dumps({"channel_id": "@agentlabph", "max_results": 10})])
    try:
        d = json.loads(out)
        return [{"platform": "YouTube", "title": v.get("title", "N/A")[:60], "url": v.get("url", ""), "created": v.get("published_at", "")} for v in d.get("items", [])]
    except:
        return []

def get_local_log():
    log = BASE / "post_log.json"
    if log.exists():
        try:
            return json.loads(log.read_text())
        except:
            return []
    return []

def main():
    print("=== Agent Lab PH — Unified Post Dashboard ===\n")
    fb = get_facebook_posts()
    yt = get_youtube_posts()
    local = get_local_log()
    all_posts = fb + yt + local
    if not all_posts:
        print("No posts found. Connect platforms and post to see them here.")
        return
    # Sort by created time if available
    def sort_key(p):
        try:
            return p.get("created", "")
        except:
            return ""
    all_posts.sort(key=sort_key, reverse=True)
    print(f"{'PLATFORM':<12} | {'TITLE':<60} | {'CREATED':<20}")
    print("-" * 100)
    for p in all_posts:
        print(f"{p['platform']:<12} | {p['title']:<60} | {p.get('created','')[:19]:<20}")
    print(f"\nTotal: {len(all_posts)} posts across {len(set(p['platform'] for p in all_posts))} platforms")
    print(f"Facebook: {len(fb)} | YouTube: {len(yt)} | Local: {len(local)}")

if __name__ == "__main__":
    main()

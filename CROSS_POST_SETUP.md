# 🔗 Agent Lab PH — Cross-Platform Hub (Compassio-style)

## What This Does
One script posts your short to **all 4 platforms** with platform-specific captions:
- ✅ YouTube (ACTIVE)
- ✅ Facebook Page (ACTIVE)
- ⚠️ Instagram (EXPIRED — needs re-link)
- ⚠️ TikTok (not connected — needs link)

## Files
| File | Purpose |
|---|---|
| `cross_post_hub.py` | Posts 1 video to YT + FB + IG + TikTok |
| `post_dashboard.py` | Unified view of all posts across platforms |
| `CAPTIONS` dict in `cross_post_hub.py` | Platform-specific text + hashtags |

## How to Use
```bash
cd /home/allenos/agent-lab-ph
python3 cross_post_hub.py shorts/jobbot_v4.mp4 "Your Title Here"
```

## Reconnect Expired/Unconnected Platforms
Run these on your **local machine** (needs browser for OAuth):

```bash
# Instagram (currently EXPIRED)
composio link instagram --no-browser

# TikTok (not connected)
composio link tiktok --no-browser
```

After linking, re-run `cross_post_hub.py` — it auto-detects ACTIVE connections.

## Dashboard
```bash
python3 post_dashboard.py
```
Shows all posts: Facebook + YouTube + local log, sorted by date.

## Notes
- Instagram requires **Business/Creator account** linked to a Facebook Page
- TikTok requires **TikTok for Business** account
- All captions are Taglish (Filipino + English) for PH audience
- No auto-posting without your explicit command (per your instruction)

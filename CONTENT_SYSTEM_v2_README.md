# 📋 Content Intelligence System v2.0

## System Overview
The Agent Lab PH content factory has 3 stages:

| Stage | Tool | Frequency | Output |
|---|---|---|---|
| **1. Research** | `content_intel.py` | Every 6h (cron) | Script IDEAS to `scripts_review/` |
| **2. Review** | **HUMAN** ← you | As needed | Approved scripts moved to `scripts_in/` |
| **3. Production** | `watch_daemon.py` | Every 15m (cron) | `.mp4` shorts in `shorts/` |

## ⚠️ MANUAL INTERVENTION REQUIRED

### Before Production
1. **Review scripts** in `/home/allenos/agent-lab-ph/scripts_review/`
2. **Edit** script content (add your personal stories/experiences)
3. **Copy approved scripts** from `scripts_review/` to `scripts_in/`
4. Daemon will automatically produce TTS + SRT + short

### Before Posting
1. **Review final shorts** in `/home/allenos/agent-lab-ph/shorts/`
2. **Run**: `python3 auto_poster.py` — this queues videos for approval (does NOT auto-post)
3. **Approve**: `python3 auto_poster.py --approve <filename>` for each video
4. **TikTok**: You must manually connect TikTok (`composio link tiktok`)

## What Changed

### Previously (broken):
- Auto-research → auto-produce → auto-post with NO human review
- Low quality ffmpeg shorts with burned captions
- Posted without approval

### Now (safe):
- Research only — scripts require YOUR edit + move to production
- Remotion-ready template (`ProfessionalTemplate.tsx`) for proper captions
- Auto-poster requires `--approve` flag to publish anything
- All posts require explicit manual approval

## Key Files
- `content_intel.py` — research agent (saves script ideas)
- `watch_daemon.py` — production pipeline (txt → short)
- `auto_poster.py` — approval-gated distribution (FB + TikTok)
- `post_transparency.py` — transparency message already posted
- `remotion-lab/` — professional template for next-gen shorts

## Post the Transparency Message
Already posted to Facebook:
> "You may have noticed some posts... I'm building an AI automation system... I stopped auto-posting, switching to Remotion for quality, every post gets my approval now."

---
**Philosophy: Quality over quantity. Your word over AI output. Control over convenience.**
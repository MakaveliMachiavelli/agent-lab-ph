# 🤖 Content Intelligence System

Automated content factory for Agent Lab PH.

## Pipeline
1. **content_intel.py** — Searches YouTube for competitor content in PH tech/freelance niches, generates fresh script angles, saves as .txt
2. **watch_daemon.py** — Processes .txt → VO + SRT + short (1080x1920)
3. **auto_poster.py** — Distributes finished shorts to Facebook Pages via Composio

## Directories
- `scripts_in/` — new scripts to process
- `scripts_done/` — processed scripts
- `shorts/` — finished videos
- `vo/` — voiceovers
- `captions/` — SRT files
- `content_intel_archive/` — research logs

## Cron Schedule
- `content_intel.py` — every 6 hours (generates 14 scripts)
- `watch_daemon.py` — every 15 min (keeps alive, processes scripts)
- `auto_poster.py` — every 2 hours (posts to Facebook)

## Connections Needed
- ✅ Facebook Page (Agent Lab ph) — ACTIVE, posting works
- ⏳ TikTok — needs `composio link tiktok` (run manually)
- ⏳ YouTube — available, not yet wired

## Stats (2026-08-26)
- 14 scripts generated in first cycle
- 3 pillar shorts + 14 content-intel shorts rendered
- Facebook auto-posting verified (video IDs returned)

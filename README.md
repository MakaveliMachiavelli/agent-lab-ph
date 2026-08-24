# Agent Lab PH 🇵🇭 — ₱0 Empire

Taglish tutorials on **free-tier cloud + automation** for Pinoy freelancers and small businesses.
Proof, not theory: this repo's assets were produced on a **₱0 stack**.

## The ₱0 Stack (live right now)
| Layer | Tool | Cost |
|-------|------|------|
| Compute | Oracle Cloud Free Tier (this box: 16 vCPU / 62GB / 193GB) | ₱0 forever |
| Ingress | Cloudflare Tunnel (no port-forward, beats CGNAT) | ₱0 |
| Automation | n8n self-hosted (Pillar 4 product) | ₱0 |
| Voiceover | edge-tts — BlessicaNeural (Taglish) | ₱0 |
| Captions | agent-reach transcribe (Groq Whisper) | ₱0 |
| Render | ffmpeg | ₱0 |
| Landing | GitHub Pages | ₱0 |

Live public URL (tunnel → n8n): **https://capital-stored-bonus-attempt.trycloudflare.com**

## Production Pipeline
`./production_pipeline.sh <task>` — tasks: `capture | tts | caption | assemble | publish-check | vertical`
All headless, terminal-native, ₱0.

## Content Packages
- `packages/p1_package.md` — Pillar 1: Fail-First Oracle (the 3-rejection story)
- `packages/p2_package.md` — Pillar 2: Hardened Server (fail2ban, SSH keys, UFW)
- `packages/p3_5_package.md` — Pillars 3-5: Loophole Roundup / n8n Agency / Ship-in-Public Funnel

## Shipped proof assets
- `shorts/empire_hero.mp4` — 9:16 hero short, burned Taglish captions, real proof B-roll
- `captions/empire_caps.srt` — caption track
- `vo/empire_vo.mp3` — BlessicaNeural VO

## Repo
github.com/MakaveliMachiavelli/agent-lab-ph

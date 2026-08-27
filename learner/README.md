# 🧠 Learner System — Agent Lab PH Self-Improving Video Pipeline

## What This Is
A **self-learning, self-healing, self-improving** video pipeline that studies successful channels (starting with @cloud-codes) and continuously upgrades our quality bar based on **your ratings**.

## Architecture
```
YouTube channels → [research] → style_profile.json → [production] → watch_daemon
                                                  ↓
                                           quality_gate.py (self-heal)
                                                  ↓
                                           your ratings (1-10)
                                                  ↓
                                           learner_cron.py (improve)
                                                  ↓
                                           updated style_profile.json
```

## Files
| File | Purpose |
|---|---|
| `learner/style_profile.py` | Generates visual + content DNA from analyzed channels |
| `learner/style_profile.json` | The learned style (captions, motion, hooks, quality bar) |
| `learner/remotion_template_v2.tsx` | Improved Remotion template using learned style |
| `learner/quality_gate.py` | Self-healing: checks brightness/duration, suggests fixes |
| `learner/learner_cron.py` | Weekly: aggregates your ratings → updates profile |
| `learner/ratings/` | Your 1-10 scores + notes per video |

## How You Train Me
1. I create a short → send you the file
2. You review → give **1-10 score + what to fix**
3. I run: `python3 learner/quality_gate.py rate <video> <score> "<notes>"`
4. Weekly: `python3 learner/learner_cron.py` updates the style profile
5. Next shorts automatically use improved settings

## Current Learned Style (@cloud-codes DNA)
- **Captions**: high-contrast kinetic text, bottom-third safe zone, word-by-word reveal
- **Hook**: provocative technical claim or counterintuitive number in first 3s
- **Pacing**: 150 WPM, 3-4 word chunks, 30-60s duration
- **Quality bar**: brightness ≥ 2.0%, duration ≥ 15s, zero text cutoff

## Next Channels to Study
Send me more @handles and I'll expand the profile.

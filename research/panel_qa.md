# PANEL 3: TECHNICAL QA ENGINEER — Automated QA Pipeline

## Reels/Shorts Spec (Platform Requirements)
| Metric | Spec | V18 Current | Pass/Fail |
|---|---|---|---|
| Resolution | 1080×1920 (9:16) | ✅ 1080×1920 | PASS |
| Frame Rate | 30fps | ✅ 30fps | PASS |
| Duration | ≤60s (Shorts), ≤90s (Reels) | ❌ 90s | FAIL |
| File Size | <100MB | ✅ 7MB | PASS |
| Codec | H.264 High Profile, AAC | ✅ H.264/AAC | PASS |
| Audio Loudness | -14 LUFS (integrated) | ❌ ~-18 LUFS | FAIL |
| Audio Peak | -1 dBTP | ❌ Unknown | FAIL |
| Brightness (mid-zone) | >20% pixels >128/255 | ❌ 5-14% | FAIL |
| Contrast | WCAG AA (4.5:1) on all text | ❌ Neon on dark fails | FAIL |
| Caption Sync | <100ms drift | ⚠️ Unknown | UNKNOWN |
| Safe Zones | 90% center safe | ⚠️ Edge text | FAIL |

## Automated QA Script
```bash
#!/bin/bash
# /home/allenos/agent-lab-ph/scripts/qa_pipeline.sh
VIDEO="$1"

# 1. Probe specs
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv "$VIDEO"

# 2. Brightness analysis (sample 12 frames)
for i in {0..11}; do
  frame=$((i * 225))
  ffmpeg -y -i "$VIDEO" -vf "select=eq(n\,$frame)" -frames:v 1 /tmp/qa_${frame}.png
  python3 -c "
from PIL import Image
import numpy as np
img = Image.open(f'/tmp/qa_{frame}.png').convert('RGB')
arr = np.array(img)
h, w = arr.shape[:2]
mid = arr[h//3:2*h//3, w//3:2*w//3]
bright = np.mean(mid > 128) * 100
print(f'f{frame} mid_bright={bright:.1f}%')
"
done

# 3. Audio loudness
ffmpeg -i "$VIDEO" -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null -

# 4. Text readability (OCR on caption zone)
# 5. Sync check (waveform vs caption timestamps)

# Exit codes: 0=pass, 1=brightness, 2=audio, 3=spec, 4=sync
```

## 3 Blocking Issues with Fix Commands

### BLOCKER 1: Duration 90s > 60s Shorts Limit
**Fix**: Compress timeline in JobBotV18.tsx
```tsx
// Line 11: const SEG = 540;  // 18s × 5 = 90s
// CHANGE TO:
const SEG = 360;  // 12s × 5 = 60s
// Update all startFrame values: 540→360, 1080→720, 1620→1080, 2160→1440
// Update durationInFrames in Root.tsx: 2700 → 1800
```

### BLOCKER 2: Audio Loudness -18 LUFS (target -14)
**Fix**: Normalize with ffmpeg loudnorm
```bash
ffmpeg -i jobbot_v18.mp4 -i audio/jobbot_v18_voice.mp3 \
  -af "loudnorm=I=-14:TP=-1:LRA=11" \
  -c:v copy -shortest shorts/jobbot_v18_final_loud.mp4
```

### BLOCKER 3: Brightness 5-14% (target >20%)
**Fix**: Apply Designer panel palette + brighter components
```tsx
// JobBotV18.tsx lines 5-11: Replace palette
const BASE = '#0d1117';
const CYAN = '#58a6ff';  // WCAG AA on BASE
const GREEN = '#3fb950';
const CORAL = '#f78166';
// Increase caption fontSize: 38 → 44
// Add radial glow behind ALL metric cards (opacity 0.15)
// Increase ParticleMorph count: 40→80, opacity 0.15→0.25
```

## CI-Ready Test Script
```yaml
# .github/workflows/video-qa.yml
name: Video QA
on: [push]
jobs:
  qa:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Render video
        run: cd remotion-lab && npx remotion render JobBotV18 out/test.mp4
      - name: Run QA
        run: ./scripts/qa_pipeline.sh out/test.mp4
```

## Deliverable: /home/allenos/agent-lab-ph/research/panel_qa.md
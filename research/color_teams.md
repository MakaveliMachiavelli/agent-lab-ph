# COLOR TEAM GATES — Finalization Protocol

## 🔴 RED TEAM (Security/Compliance/Platform Risk)
**Mandate**: Zero platform violations, legal safety, brand protection

| Gate | Check | V18 Status | Fix Required |
|---|---|---|---|
| R1 | No copyrighted assets (music, footage, logos) | ✅ All custom | PASS |
| R2 | No PII in terminal/demo (real emails, keys) | ⚠️ Browser mockup shows "user@example.com" | Sanitize demo data |
| R3 | Platform TOS compliant (no spam claims, no guaranteed income) | ❌ "$3,200/month" = income claim | Change to "up to $3,200/month possible" |
| R4 | Medical/health claims none | ✅ None | PASS |
| R5 | Affiliate disclosure if links | ⚠️ "Comment ROBOT" = engagement bait | Add "Not financial advice" disclaimer |

**Red Team Verdict**: CONDITIONAL PASS — Fix R2, R3, R5

---

## 🔵 BLUE TEAM (Technical Quality/Standards)
**Mandate**: Spec compliance, reproducibility, maintainability

| Gate | Check | V18 Status | Fix Required |
|---|---|---|---|
| B1 | Reels spec: ≤60s, 1080×1920, 30fps, H.264 | ❌ 90s duration | Compress to 60s (SEG=360) |
| B2 | Audio: -14 LUFS, -1 dBTP, AAC 128kbps | ❌ -18 LUFS | loudnorm filter |
| B3 | Brightness: mid-zone >20% | ❌ 5-14% | Palette + component brightness |
| B4 | Contrast: WCAG AA all text | ❌ Neon fails | Cloud Codes palette |
| B5 | Caption sync <100ms drift | ⚠️ Unknown | Add sync verification |
| B6 | Safe zones 90% center | ⚠️ Edge text | Increase padding 32→48px |
| B7 | Deterministic render (same seed = same output) | ✅ Remotion deterministic | PASS |
| B8 | CI/CD pipeline exists | ❌ No workflow | Add .github/workflows/video-qa.yml |

**Blue Team Verdict**: FAIL — 5 blocking issues (B1, B2, B3, B4, B8)

---

## 🟢 GREEN TEAM (Creative Excellence/Brand Alignment)
**Mandate**: Cloud Codes quality bar, Agent Lab PH brand voice, audience resonance

| Gate | Check | V18 Status | Fix Required |
|---|---|---|---|
| G1 | Hook: Technical curiosity gap + visual proof in 3s | ❌ Generic pain hook | Designer Panel Fix 1 |
| G2 | Pacing: 60s total, retention curve match | ❌ 90s, slow segments | Creator Panel Fix 2 |
| G3 | Voice: fil-PH-BlessicaNeural, natural Taglish | ✅ Good | PASS |
| G4 | Visual fidelity: Cloud Codes diagram/terminal quality | ❌ Simplified mockups | Designer Panel Fix 2 |
| G5 | Motion polish: Spring physics, stagger, micro-interactions | ❌ Linear, no stagger | Designer Panel Fix 3 |
| G6 | CTA: Testable, immediate, scarce | ❌ Vague "Comment ROBOT" | Creator Panel Fix 3 |
| G7 | Brand: "Agent Lab PH • Dice" consistent | ✅ Watermark present | PASS |
| G8 | Audience: Pinoy freelancer/BPO beginner relatable | ⚠️ Generic | More specific pain points |

**Green Team Verdict**: FAIL — 4 blocking issues (G1, G2, G4, G5, G6)

---

## 🎯 UNIFIED FIX LIST (All Teams Combined)

### P0 — Must Fix Before Any Release
1. **Duration**: 90s → 60s (SEG=360, durationInFrames=1800)
2. **Audio Loudness**: -18 → -14 LUFS (loudnorm)
3. **Palette**: Neon → Cloud Codes (#0d1117, #58a6ff, #3fb950)
4. **Brightness**: 5-14% → >20% (glows, particle count, component bg)
5. **Contrast**: WCAG AA on all text
6. **Hook**: Technical curiosity + metric proof in 3s
7. **Pacing**: 12s/segment, terminal at 12s not 24s
8. **CTA**: Testable mechanism (GitHub link + commands)
9. **Motion**: Spring physics, 80ms stagger, 530ms cursor blink
10. **Terminal**: Syntax highlighting, real keystroke timing
11. **Legal**: Sanitize demo data, income claim disclaimer
12. **CI**: Add qa_pipeline.sh + GitHub workflow

### P1 — Quality Polish
13. Caption font: 38→44px, padding 32→48px
14. ParticleMorph: count 80, opacity 0.25
15. FlowStages stagger: 50→80ms
16. AppCard3D: spring(300,30), hover lift

---

## QA LOOP PROTOCOL
```
while true:
  1. Apply next P0 fix
  2. Render: npx remotion render JobBotV18 out/test.mp4
  3. Run QA: ./scripts/qa_pipeline.sh out/test.mp4
  4. If ALL Blue gates PASS → continue
  5. If ANY Red gate FAIL → block release
  6. If Green gates PASS → GREEN LIGHT
  7. Commit, tag, deliver
```

## Deliverable: /home/allenos/agent-lab-ph/research/color_teams.md
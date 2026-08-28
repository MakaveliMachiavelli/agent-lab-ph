# PANEL 1: SENIOR MOTION DESIGNER — Cloud Codes vs JobBot V18

## Cloud Codes Visual DNA (from channel analysis)
- **Palette**: `#0d1117` base, `#58a6ff` cyan accent, `#3fb950` green success, `#f78166` coral alert
- **Typography**: JetBrains Mono (code), Inter (UI), 14-18px body, 24-32px headlines on mobile
- **Motion**: 60fps, `cubic-bezier(0.25, 0.46, 0.45, 0.94)` easing, 150-300ms transitions
- **Components**: Syntax-highlighted code blocks, animated architecture diagrams (nodes + edges), terminal with real keystrokes, metric cards with glow rings
- **Layout**: 9:16 safe zones, zero text overlap, persistent bottom caption bar, 16:9 diagrams in portrait via letterboxing
- **Lighting**: Subtle vignette, radial glows behind key metrics, scanline overlay on terminal

## V18 Gaps vs Cloud Codes

### GAP 1: Color Authority & Contrast
**V18**: `#050812` base, `#00FFC8` mint, `#FF5E3A` coral — neon, ungrounded, low contrast
**Cloud Codes**: `#0d1117` base, `#58a6ff` cyan (WCAG AA on dark), `#3fb950` green — technical, trusted
**Fix**: Replace palette in JobBotV18.tsx lines 5-11
```tsx
const BASE = '#0d1117';
const CYAN = '#58a6ff';
const GREEN = '#3fb950';
const CORAL = '#f78166';
const TEXT = '#e6edf3';
const MUTED = '#8b949e';
```
**Pass Criteria**: Mid-zone brightness ≥20% on all segments, WCAG AA contrast on all text

### GAP 2: Diagram Fidelity (Browser Mockup)
**V18**: Simplified browser chrome, placeholder text, no syntax highlighting
**Cloud Codes**: Real URL bar, tab strip, DevTools-accurate code with Monokai highlighting, live cursor
**Fix**: Replace BrowserMockup component (lines 134-182) with:
- Real Chrome tab bar (3 tabs: OnlineJobs, Upwork, Agent)
- Address bar with `https://onlinejobs.ph`
- Code block with syntax highlighting (Prism.js colors via CSS)
- Animated typing cursor at 60fps
**Pass Criteria**: Frame-accurate terminal keystrokes, syntax colors match Monokai

### GAP 3: Motion Polish — Micro-interactions
**V18**: Linear interpolations, no stagger, particles feel random
**Cloud Codes**: Staggered entrance (50ms/item), physics-based spring (stiffness 300, damping 30), hover lift on cards, focus rings
**Fix**: 
1. Add `spring` helper using `interpolate` with `Easing.spring(300, 30)`
2. Stagger FlowStages cards: `delay = i * 80` (not 50)
3. Add `hover` scale(1.02) on AppCard3D via `frame` parity
4. Terminal cursor: blink at 530ms (real terminal rate)
**Pass Criteria**: All entrances staggered 50-100ms, spring physics on 100% of animated values, cursor blink 530ms

## Deliverable: /home/allenos/agent-lab-ph/research/panel_designer.md
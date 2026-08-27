#!/usr/bin/env python3
"""V12 Creative Director Notes — What makes Reels viral (from studying cloud-codes, akmofficial, top creators)."""

CREATIVE_DNA = {
    # Visual hooks that stop scroll in first 0.5s
    "hooks": [
        "Big number count-up from 0 → shocking value (50+ APPS/NIGHT)",
        "Split screen: Before (tired scrolling) → After (auto apply)",
        "Fast-cut: 3 problems → 1 solution reveal",
        "POV screen recording: 'Watch this script work'",
        "Bold statement on solid color: 'Stop applying manually'",
    ],
    
    # Motion patterns that feel premium
    "motion": {
        "particles": "Ambient floating dots with subtle glow, not distracting",
        "glitch": "Text glitch on key words (ROBOT, FREE, 50+) — 2 frames",
        "morph": "Shape morph between segments (circle → square → arrow)",
        "reveal": "Text writes itself (typewriter) + word-by-word pop",
        "camera": "Subtle 3D tilt on cards, parallax on background",
        "transitions": "Match cuts (same position, different content), not fades",
    },
    
    # Color palette (Reels/Shorts optimized)
    "colors": {
        "bg": "#080C16",           # Deep navy (not pure black)
        "accent": "#00D4AA",       # Neon mint (viral on Reels)
        "accent2": "#FF6B35",      # Coral orange (CTA pop)
        "text_primary": "#F0F4FA", # Off-white (easier on eyes)
        "text_muted": "#7D8AA5",   # Muted blue-gray
        "card": "rgba(14,20,32,0.95)", # Glassmorphism
        "border": "rgba(0,212,170,0.3)",
        "glow": "rgba(0,212,170,0.4)",
    },
    
    # Typography (Reels-safe: large, bold, centered)
    "typography": {
        "hook": {"size": 56, "weight": 800, "lineHeight": 1.1},
        "subhook": {"size": 36, "weight": 600, "lineHeight": 1.3},
        "body": {"size": 28, "weight": 500, "lineHeight": 1.5},
        "caption": {"size": 22, "weight": 400, "lineHeight": 1.6},
        "cta": {"size": 40, "weight": 800, "lineHeight": 1.2},
        "font": "Inter, system-ui, sans-serif",
    },
    
    # Segment structure (60s = 4 × 15s beats)
    "segments": [
        {"time": "0-3s", "beat": "HOOK", "visual": "Big number + split screen"},
        {"time": "3-15s", "beat": "PAIN", "visual": "Relatable struggle animation"},
        {"time": "15-30s", "beat": "REVEAL", "visual": "3-step flow with morphing cards"},
        {"time": "30-45s", "beat": "PROOF", "visual": "Live screen recording style"},
        {"time": "45-55s", "beat": "CTA", "visual": "Guide preview + comment ROBOT"},
        {"time": "55-60s", "beat": "BRAND", "visual": "Dice logo + Agent Lab PH"},
    ],
}

print("Creative DNA loaded. Building V12...")
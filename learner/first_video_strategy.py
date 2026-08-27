#!/usr/bin/env python3
"""First proper video strategy — beginner-friendly, high-value, shareable."""

FIRST_VIDEO_STRATEGY = {
    # Audience: Filipino freelancers, BPO workers, junior devs
    # Pain: "AI is overwhelming / I don't know where to start / I'm stuck in low-pay work"
    # Promise: "One free tool + 15 min setup = AI that works for you while you sleep"
    
    "concept": "FREE AI Agent That Applies to Jobs For You (OnlineJobs.ph + Upwork)",
    
    "why_this_wins": [
        "Immediate pain point: job applications take hours, low response rate",
        "Beginner-friendly: no code, free tools, 15-min setup",
        "Proof-based: show real applications sent, real responses",
        "Filipino-specific: OnlineJobs.ph is THE platform here",
        "Shareable: 'Send this to your tambay ka-trabaho'",
        "Establishes Dice as 'your agent that does the work'",
    ],
    
    "structure_4_segments": {
        "hook_0_3s": "What if an AI applied to 50 jobs while you ate lunch? I built it free.",
        "problem_3_15s": "You: copy-paste cover letters, 20 applications, 0 replies. Me: agent writes custom cover letters, applies, tracks replies. Same afternoon.",
        "demo_15_45s": "Live terminal: 1) Clone repo 2) Add your profile 3) Run. Shows actual browser applying to OnlineJobs.ph.",
        "result_45_55s": "Dashboard: 47 applied, 12 viewed, 3 replies, 1 interview booked. All while I slept.",
        "cta_55_60s": "Repo in description. Fork it. Your agent starts tonight. Follow Dice for the next build.",
    },
    
    "beginner_guardrails": [
        "No API keys needed (uses local browser automation)",
        "Free tools: Playwright + Python (pre-installed on Mac/Linux, 1-click Windows)",
        "Copy-paste config — no coding",
        "Runs on any laptop, even 8GB RAM",
    ],
    
    "dice_persona_beats": [
        "Opens with terminal prompt: dice@agent-lab:~$",
        "Types commands live (code window)",
        "Shows browser window actually clicking 'Apply'",
        "Ends with dashboard — proof, not promise",
    ],
}

print("First video concept locked. Ready to script + render.")
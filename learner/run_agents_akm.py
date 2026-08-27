#!/usr/bin/env python3
"""Use agy + cmdc to deeply analyze @akmofficial and sync learnings to Agent Lab PH."""
import subprocess, os, json, time
from pathlib import Path

LEARNER = Path("/home/allenos/agent-lab-ph/learner")
STUDY = LEARNER / "reference" / "akm_study.json"
study = json.loads(STUDY.read_text())

# Get titles from analysis
video_titles = [f["title"] for f in study["analysis"]["formats"][:20]]
short_titles = [f["title"] for f in study["analysis"]["formats"][20:]]

AGY_PROMPT = f"""You are a YouTube content strategy analyst. Analyze channel @akmofficial.

VIDEO TITLES:
{chr(10).join('- ' + t for t in video_titles)}

SHORT TITLES:
{chr(10).join('- ' + t for t in short_titles)}

Analyze their content strategy. Output JSON with keys:
- hook_formulas: [templates like "How to X that Y", "Why nobody is talking about Z"]
- title_patterns: [patterns observed]
- content_structure: [typical explainer steps]
- visual_style: [from titles/descriptions]
- shareability_factors: [why content spreads]
- actionable_tactics_for_agent_lab: [specific for our faceless AI channel, host=Dice]

Be specific, no fluff. Return only valid JSON."""

CMDC_PROMPT = f"""Build a Remotion .tsx template for YouTube Shorts matching @akmofficial style:
- Text hook in first 3s (title overlay)
- Native captions word-by-word reveal via @remotion/captions
- Clean dark professional background
- Bottom progress bar
Props: {{ title: string; srtPath: string; bgPath: string }}
Output complete TypeScript file only."""

# Write prompts
(LEARNER / "_prompt_agy.txt").write_text(AGY_PROMPT)
(LEARNER / "_prompt_cmdc.txt").write_text(CMDC_PROMPT)

def run_cli(tool, prompt_file, out_file):
    env = dict(os.environ)
    env["PATH"] = "/home/allenos/.local/bin:" + env["PATH"]
    prompt = open(prompt_file).read()
    try:
        r = subprocess.run([tool, "-p", prompt], capture_output=True, text=True, timeout=280, env=env)
        out = r.stdout + r.stderr
        (LEARNER / "reference" / out_file).write_text(out)
        return out
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {e}"

print("Running agy (strategy)...")
agy_out = run_cli("agy", LEARNER / "_prompt_agy.txt", "akm_strategy_agy.txt")
print(agy_out[:300])

print("\nRunning cmdc (template)...")
cmdc_out = run_cli("cmdc", LEARNER / "_prompt_cmdc.txt", "akm_template_cmdc.txt")
print(cmdc_out[:300])
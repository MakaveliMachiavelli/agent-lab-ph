#!/usr/bin/env python3
"""text2srt.py — split plain transcript into timed SRT chunks.
Timing: proportional to word count across total audio duration (via ffprobe)."""
import sys, subprocess, re

def dur(path):
    out = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries",
                          "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout.strip()
    return float(out or 0)

def ts(sec):
    ms = int(round(sec * 1000))
    h, r = divmod(ms, 3600000); m, r = divmod(r, 60000); s, ms = divmod(r, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def main(mp3, textfile, out):
    duration = dur(mp3)
    words = re...[truncated]
#!/usr/bin/env python3
"""watch_daemon.py — txt -> VO + SRT + short (fixed)"""
import os, re, subprocess, shutil, time

BASE = "/home/allenos/agent-lab-ph"
IN_DIR = os.path.join(BASE, "scripts_in")
DONE_DIR = os.path.join(BASE, "scripts_done")
VO_DIR = os.path.join(BASE, "vo")
CAP_DIR = os.path.join(BASE, "captions")
SHORT_DIR = os.path.join(BASE, "shorts")

EDGE = "/home/allenos/.hermes/hermes-agent/venv/bin/edge-tts"
TRANSCRIBE = "/home/allenos/.agent-reach-venv/bin/agent-reach"
POLL = 10

for d in (IN_DIR, DONE_DIR, VO_DIR, CAP_DIR, SHORT_DIR):
    os.makedirs(d, exist_ok=True)

def safe(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

def text_to_srt(text_path, srt_path, audio_path):
    """Convert plain transcript to timed SRT using ffprobe audio duration."""
    raw = open(text_path).read().strip()
    if not raw:
        return False
    if '-->' in open(text_path).read():
        shutil.copy(text_path, srt_path)
        return True
    try:
        dur = float(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", audio_path
        ]).decode().strip())
    except Exception:
        dur = 30.0
    words = raw.split()
    chunks = []
    cur = []
    for w in words:
        cur.append(w)
        if len(cur) >= 4:
            chunks.append(" ".join(cur))
            cur = []
    if cur:
        chunks.append(" ".join(cur))
    per = dur / max(len(chunks), 1)
    def ts(sec):
        return f"{int(sec//3600):02d}:{int(sec%3600//60):02d}:{int(sec%60):02d},{int(sec%1*1000):03d}"
    lines = []
    for i, c in enumerate(chunks):
        st = i * per
        en = min((i + 1) * per, dur)
        lines += [str(i + 1), f"{ts(st)} --> {ts(en)}", c, ""]
    open(srt_path, "w").write("\n".join(lines))
    return True

def process(txt_path):
    name = safe(os.path.splitext(os.path.basename(txt_path))[0])
    print(f"[watch] processing {name}", flush=True)
    mp3 = os.path.join(VO_DIR, f"{name}.mp3")
    srt = os.path.join(CAP_DIR, f"{name}.srt")
    out = os.path.join(SHORT_DIR, f"{name}.mp4")
    # 1. TTS
    subprocess.run([EDGE, "--voice", "fil-PH-BlessicaNeural",
                    "--file", txt_path, "--write-media", mp3], check=True)
    # 2. Transcribe
    with open(srt, "w") as f:
        subprocess.run([TRANSCRIBE, "transcribe", mp3], stdout=f,
                       stderr=subprocess.DEVNULL)

    text_to_srt(txt_path, srt, mp3)  # rebuild valid SRT from transcript

    # 3. Assemble vertical short (bg.png as B-roll background, captions burned)
    proof = "/tmp/proof.png"
    if os.path.exists(proof):
        bg = proof
    else:
        # make a solid background if proof missing
        bg = os.path.join(BASE, "bg.png")
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i",
                        "color=c=0x0a0e1a:s=1080x1920", "-frames", "1", bg],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       env={**os.environ, "FONTCONFIG_FILE": "/tmp/fonts.conf"})
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", bg, "-i", mp3,
        "-filter_complex",
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "format=yuv420p,zoompan=z='min(zoom+0.0008,1.18)':d=750:"
        "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,"
        f"subtitles={srt}:force_style='FontSize=30,PrimaryColour=&Hffffff&,"
        "OutlineColour=&H000000&,Outline=4'[v]",
        "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "medium",
        "-crf", "21", "-c:a", "aac", "-b:a", "128k", "-shortest", out],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       env={**os.environ, "FONTCONFIG_FILE": "/tmp/fonts.conf"})
    # 4. Archive
    shutil.move(txt_path, os.path.join(DONE_DIR, os.path.basename(txt_path)))
    print(f"[watch] DONE -> {out}", flush=True)

def main():
    print(f"[watch] monitoring {IN_DIR} every {POLL}s", flush=True)
    while True:
        for f in os.listdir(IN_DIR):
            if f.endswith(".txt"):
                process(os.path.join(IN_DIR, f))
        time.sleep(POLL)

if __name__ == "__main__":
    main()
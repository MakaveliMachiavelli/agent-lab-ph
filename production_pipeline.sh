#!/usr/bin/env bash
# Agent Lab PH — Production Pipeline (FFmpeg-Only, Headless, Terminal-Native)
# Usage: ./production_pipeline.sh <task>
# Tasks: capture | tts | caption | assemble | publish-check

set -euo pipefail

WORKDIR="/home/allenos/agent-lab-ph"
CAPTURE_DIR="$WORKDIR/captures"
VO_DIR="$WORKDIR/vo"
CAPS_DIR="$WORKDIR/captions"
FINAL_DIR="$WORKDIR/final"
mkdir -p "$CAPTURE_DIR" "$VO_DIR" "$CAPS_DIR" "$FINAL_DIR"

log() { echo "[$(date +'%H:%M:%S')] $1"; }

case "${1:-help}" in
  capture)
    # Capture terminal screen (headless VPS via VNC/X11)
    log "Starting capture... Ctrl+C to stop"
    # Use Xvfb :99 (the running display) - adjust resolution to match
    ffmpeg -f x11grab -s 1280x800 -framerate 30 -i :99 \
      -c:v libx264 -preset ultrafast -crf 18 \
      "$CAPTURE_DIR/cap_$(date +%Y%m%d_%H%M%S).mp4"
    ;;
  tts)
    # Generate Taglish voiceover
    [ -z "${2:-}" ] && { echo "Usage: $0 tts <text_file>"; exit 1; }
    log "Generating TTS from $2"
    edge-tts --voice fil-PH-BlessicaNeural \
      --file "$2" --write-media "$VO_DIR/vo_$(date +%Y%m%d_%H%M%S).mp3"
    ;;
  caption)
    # Transcribe VO to SRT via Groq Whisper (requires GROQ_API_KEY)
    [ -z "${2:-}" ] && { echo "Usage: $0 caption <audio_file>"; exit 1; }
    log "Transcribing $2"
    curl -s https://api.groq.com/openai/v1/audio/transcriptions \
      -H "Authorization: Bearer $GROQ_API_KEY" \
      -F file="@$2" -F model="whisper-large-v3" \
      -F response_format="srt" -o "$CAPS_DIR/caps_$(date +%Y%m%d_%H%M%S).srt"
    ;;
  assemble)
    # Burn captions into video
    [ -z "${2:-}" ] || [ -z "${3:-}" ] && { echo "Usage: $0 assemble <video> <srt>"; exit 1; }
    log "Assembling $2 + $3"
    ffmpeg -i "$2" -vf "subtitles=$3:force_style='FontSize=24,PrimaryColour=&Hffffff&'" \
      -c:a copy "$FINAL_DIR/final_$(date +%Y%m%d_%H%M%S).mp4"
    ;;
  publish-check)
    log "Pre-publish checklist:"
    [ -f "$VO_DIR"/*.mp3 ] && echo "  ✅ VO ready" || echo "  ❌ No VO"
    [ -f "$CAPS_DIR"/*.srt ] && echo "  ✅ Captions ready" || echo "  ❌ No captions"
    [ -f "$FINAL_DIR"/*.mp4 ] && echo "  ✅ Final video ready" || echo "  ❌ No final"
    ;;
  *)
    echo "Agent Lab PH Production Pipeline"
    echo "Tasks: capture | tts <txt> | caption <audio> | assemble <vid> <srt> | publish-check"
    ;;
esac

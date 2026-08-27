#!/usr/bin/env python3
"""learner/remotion_template_v2.tsx — Improved Remotion short from Cloud Codes DNA."""
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, Easing, staticFile } from "remotion";
import { z } from "zod";
import { parseSrt } from "@remotion/captions";

// Schema for input props
const schema = z.object({
  srtPath: z.string(),
  bgPath: z.string(),
  title: z.string(),
});

export const RemotionShortV2: React.FC<{ srtPath: string; bgPath: string; title: string }> = ({
  srtPath,
  bgPath,
  title,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // Load SRT
  const srtContent = useMemo(() => {
    const raw = fetch(staticFile(srtPath)).then((r) => r.text());
    return raw;
  }, [srtPath]);

  const captions = useMemo(() => {
    if (!srtContent) return [];
    const { captions } = parseSrt({ input: srtContent });
    return captions;
  }, [srtContent]);

  // Find active caption
  const currentTime = frame / fps;
  const active = captions.find(
    (c) => currentTime >= c.startMs / 1000 && currentTime <= c.endMs / 1000
  );

  // Hide captions briefly (200ms) for breathing room
  const captionVisible = active && frame % 8 !== 0;

  // Hook: title appears in first 2 seconds
  const titleOpacity = interpolate(frame, [0, 15, fps * 2, fps * 2 + 15], [0, 1, 1, 0], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e1a" }}>
      {/* Background */}
      <AbsoluteFill>
        <img
          src={staticFile(bgPath)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
        />
        {/* Dark overlay for text contrast */}
        <AbsoluteFill
          style={{ backgroundColor: "rgba(10, 14, 26, 0.65)" }}
        />
      </AbsoluteFill>

      {/* Title (hook) */}
      {titleOpacity > 0 && (
        <div
          style={{
            position: "absolute",
            top: "8%",
            left: "6%",
            right: "6%",
            color: "white",
            fontSize: 48,
            fontWeight: 800,
            fontFamily: "Inter, sans-serif",
            textShadow: "0 2px 12px rgba(0,0,0,0.9)",
            opacity: titleOpacity,
            lineHeight: 1.1,
          }}
        >
          {title}
        </div>
      )}

      {/* Captions (bottom safe zone) */}
      {captionVisible && active && (
        <div
          style={{
            position: "absolute",
            bottom: "12%",
            left: "5%",
            right: "5%",
            color: "white",
            fontSize: 52,
            fontWeight: 700,
            fontFamily: "Inter, sans-serif",
            textShadow: "0 2px 8px rgba(0,0,0,0.9), 0 0 2px rgba(0,0,0,1)",
            textAlign: "center",
            lineHeight: 1.15,
          }}
        >
          {active.text}
        </div>
      )}

      {/* Progress bar at bottom */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          height: 6,
          backgroundColor: "#1e90ff",
          transform: `scaleX(${frame / (useVideoConfig().durationInFrames - 1)})`,
          transformOrigin: "left",
        }}
      />
    </AbsoluteFill>
  );
};
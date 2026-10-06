import { ImageResponse } from "next/og";

// The preview shown when a Perry link is shared on WhatsApp, Telegram, etc.
export const alt = "Perry: see every route from Class 10 to a career";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

const LINES = ["#75aef5", "#f0b44c", "#68c4b8", "#f29676", "#c39cf5"];

export default function Image() {
  return new ImageResponse(
    (
      <div style={{ width: "100%", height: "100%", display: "flex", flexDirection: "column", justifyContent: "space-between", padding: 72, background: "radial-gradient(70% 60% at 50% -10%, #1e3a5f 0%, #0e1320 70%)", color: "#eef1f6" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
          <div style={{ width: 64, height: 64, borderRadius: 32, display: "flex", alignItems: "center", justifyContent: "center", background: "linear-gradient(135deg,#60a5fa,#a78bfa)", color: "#111827", fontSize: 34, fontWeight: 800 }}>P</div>
          <div style={{ fontSize: 40, fontWeight: 800, letterSpacing: 4, color: "#a5b4fc" }}>PERRY</div>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
          <div style={{ fontSize: 72, fontWeight: 800, lineHeight: 1.05, letterSpacing: -1 }}>See every career path before you choose one</div>
          <div style={{ fontSize: 30, color: "#9aa3b2" }}>Class 10 to career · exams · second chances · Andhra Pradesh &amp; Telangana</div>
        </div>
        <div style={{ display: "flex", gap: 14 }}>
          {LINES.map((c) => (
            <div key={c} style={{ height: 12, flex: 1, borderRadius: 6, background: c }} />
          ))}
        </div>
      </div>
    ),
    size,
  );
}

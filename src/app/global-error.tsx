"use client";

// Replaces the whole page (navbar included) if the root layout itself fails,
// so it carries its own document and dark styling.
export default function GlobalError({ retry }: { error: Error & { digest?: string }; retry: () => void }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, minHeight: "100vh", display: "grid", placeItems: "center", background: "#111827", color: "#f3f4f6", fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif", textAlign: "center", padding: 16 }}>
        <title>Something went wrong — Perry</title>
        <div>
          <h1 style={{ fontSize: 24, margin: 0 }}>Something went wrong</h1>
          <p style={{ color: "#9ca3af", marginTop: 12 }}>Perry couldn&apos;t load just now. Please try again in a moment.</p>
          <button type="button" onClick={() => retry()} style={{ marginTop: 24, padding: "12px 24px", borderRadius: 12, border: 0, background: "linear-gradient(90deg,#3b82f6,#8b5cf6)", color: "#fff", fontSize: 16, fontWeight: 600, cursor: "pointer" }}>
            Try again
          </button>
        </div>
      </body>
    </html>
  );
}

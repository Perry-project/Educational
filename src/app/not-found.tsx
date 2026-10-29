import Link from "next/link";

export const metadata = { title: "Page not found — Perry" };

export default function NotFound() {
  return (
    <section className="wrap flex min-h-[calc(100svh-var(--nav-h)-var(--tabbar-h))] flex-col items-start justify-center gap-5 py-16">
      <h1 className="fade-in m-0 text-[30px] font-bold tracking-tight lg:text-[40px]">Page not found</h1>
      <p className="fade-in m-0 max-w-[48ch] text-[17px] leading-relaxed" style={{ "--d": "120ms" } as React.CSSProperties}>
        This link may be old or mistyped. Every route from Class 10 is still on the career map.
      </p>
      <div className="fade-in flex flex-wrap gap-3" style={{ "--d": "220ms" } as React.CSSProperties}>
        <Link href="/flowchart" className="btn">Open the career map</Link>
        <Link href="/" className="btn btn-secondary">Go home</Link>
      </div>
    </section>
  );
}

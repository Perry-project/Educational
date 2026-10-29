"use client";

import Link from "next/link";

// Shown when a page fails, usually because the database couldn't be reached.
export default function Error({ retry }: { error: Error & { digest?: string }; retry: () => void }) {
  return (
    <section className="wrap flex min-h-[calc(100svh-var(--nav-h)-var(--tabbar-h))] flex-col items-start justify-center gap-5 py-16">
      <h1 className="m-0 text-[30px] font-bold tracking-tight lg:text-[40px]">Something went wrong</h1>
      <p className="m-0 max-w-[48ch] text-[17px] leading-relaxed" style={{ color: "var(--muted)" }}>This page couldn&apos;t load just now. Please try again in a moment.</p>
      <div className="flex flex-wrap gap-3">
        <button type="button" onClick={() => retry()} className="btn cursor-pointer border-0">Try again</button>
        <Link href="/" className="btn btn-secondary">Go home</Link>
      </div>
    </section>
  );
}

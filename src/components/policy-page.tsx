import type { ReactNode } from "react";

// Shared layout for the short policy pages (Disclaimer, Privacy).
export default function PolicyPage({
  title, updated, intro, sections,
}: {
  title: string;
  updated: string;
  intro: ReactNode;
  sections: { heading: string; body: ReactNode }[];
}) {
  return (
    <div className="mx-auto max-w-3xl px-4 py-14 sm:px-6 lg:px-8">
      <header className="site-fade-up">
        <h1 className="text-4xl font-bold tracking-tight">{title}</h1>
        <p className="mt-2 text-sm text-gray-500">Last updated {updated}</p>
        <div className="mt-6 text-lg leading-relaxed text-gray-300">{intro}</div>
      </header>
      <div className="mt-12 space-y-10">
        {sections.map((s) => (
          <section key={s.heading}>
            <h2 className="mb-3 text-xl font-semibold text-[var(--site-heading)]">{s.heading}</h2>
            <div className="space-y-3 leading-relaxed text-gray-300">{s.body}</div>
          </section>
        ))}
      </div>
    </div>
  );
}

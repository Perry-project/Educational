import type { ReactNode } from "react";
import PageHead from "./page-head";

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
    <>
      <PageHead title={title}>Last updated {updated}</PageHead>
      <div className="mx-auto max-w-[760px] px-4 pt-10 pb-20 sm:px-6 lg:px-8">
        <div className="text-[17px] leading-relaxed">{intro}</div>
        <div className="mt-12 flex flex-col gap-10">
          {sections.map((s) => (
            <section key={s.heading}>
              <h2 className="m-0 mb-3 text-[20px] font-bold">{s.heading}</h2>
              <div className="flex flex-col gap-3 text-[16px] leading-relaxed" style={{ color: "var(--soft)" }}>{s.body}</div>
            </section>
          ))}
        </div>
      </div>
    </>
  );
}

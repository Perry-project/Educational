import type { ReactNode } from "react";

// The top of each tool page: a clear title and one line on what it's for,
// on a white band with a hairline under it.
export default function PageHead({
  title, children, width = 1100, extra,
}: {
  title: string; children: ReactNode; width?: number; extra?: ReactNode;
}) {
  return (
    <header style={{ background: "#fff", borderBottom: "1px solid var(--line, #e2e8f0)" }}>
      <div className="mx-auto flex flex-col gap-2 px-4 pt-7 pb-6 sm:px-6 lg:px-8 lg:pt-10 lg:pb-8" style={{ maxWidth: width }}>
        <h1 className="m-0 text-[28px] leading-tight font-bold tracking-tight lg:text-[36px]" style={{ color: "var(--ink)" }}>{title}</h1>
        <p className="m-0 max-w-[60ch] text-[15px] leading-relaxed lg:text-[17px]" style={{ color: "var(--muted)" }}>{children}</p>
        {extra}
      </div>
    </header>
  );
}

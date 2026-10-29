import Link from "next/link";
import { Logo } from "./site-nav";

const COLUMNS = [
  { title: "Explore", links: [{ href: "/flowchart", label: "Career map" }, { href: "/exams", label: "Exams" }, { href: "/second-chance", label: "Second chance" }] },
  { title: "Guidance", links: [{ href: "/pathfinder", label: "Find my path" }, { href: "/current-affairs", label: "News" }, { href: "/about", label: "About Perry" }] },
  { title: "Legal", links: [{ href: "/disclaimer", label: "Disclaimer" }, { href: "/privacy", label: "Privacy" }] },
];

export default function Footer() {
  return (
    <footer style={{ background: "#fff", borderTop: "1px solid var(--border)" }}>
      <div className="wrap grid gap-10 py-12 lg:grid-cols-[1.2fr_2fr] lg:py-14">
        <div className="flex max-w-[34ch] flex-col gap-3">
          <Logo />
          <p className="m-0 text-[14px] leading-relaxed" style={{ color: "var(--muted)" }}>
            Free career guidance for students and parents in Andhra Pradesh and Telangana. No sign-up, no ads.
          </p>
        </div>
        <nav aria-label="Footer" className="grid grid-cols-2 gap-8 sm:grid-cols-3">
          {COLUMNS.map((c) => (
            <div key={c.title} className="flex flex-col gap-1">
              <p className="m-0 mb-1 text-[13px] font-semibold" style={{ color: "var(--ink)" }}>{c.title}</p>
              {c.links.map((l) => (
                <Link key={l.href} href={l.href} className="inline-flex min-h-9 items-center text-[14px] no-underline hover:underline" style={{ color: "var(--muted)" }}>
                  {l.label}
                </Link>
              ))}
            </div>
          ))}
        </nav>
      </div>
      <div style={{ borderTop: "1px solid var(--border)" }}>
        <div className="wrap flex flex-col gap-1 py-5 text-[13px] sm:flex-row sm:justify-between" style={{ color: "var(--muted)" }}>
          <span>Not a government website. Always confirm dates and rules on the official notice.</span>
          <span>© 2026 Perry</span>
        </div>
      </div>
    </footer>
  );
}

"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import Icon from "./icon";

// Desktop: one white bar with the logo, the main pages and one action.
// Phones: the logo on top and a tab bar at the bottom, within thumb reach.

const LINKS = [
  { href: "/flowchart", label: "Career map", short: "Map", icon: "map" },
  { href: "/exams", label: "Exams", short: "Exams", icon: "file" },
  { href: "/second-chance", label: "Second chance", short: "Way back", icon: "rotate" },
  { href: "/pathfinder", label: "Find my path", short: "My path", icon: "compass" },
  { href: "/current-affairs", label: "News", short: "News", icon: "news" },
];

const isActive = (pathname: string, href: string) => pathname === href || pathname.startsWith(href + "/");

export function Logo() {
  return (
    <span className="flex items-center gap-2">
      <span aria-hidden className="grid h-7 w-7 place-items-center rounded-lg text-white" style={{ background: "var(--indigo)" }}>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="6" cy="6" r="2.2" /><circle cx="18" cy="18" r="2.2" /><path d="M8.2 6H14a4 4 0 0 1 0 8h-4a4 4 0 0 0 0 8h5.8" />
        </svg>
      </span>
      <span className="text-[19px] font-bold tracking-tight" style={{ color: "var(--ink)" }}>Perry</span>
    </span>
  );
}

export default function SiteNav() {
  const pathname = usePathname();

  return (
    <>
      <header className="sticky top-0 z-[100]" style={{ background: "rgba(255,255,255,0.97)", borderBottom: "1px solid var(--border)" }}>
        <nav aria-label="Main" className="wrap flex h-[var(--nav-h)] items-center justify-between gap-6">
          <Link href="/" aria-label="Perry home" className="flex min-h-11 items-center no-underline">
            <Logo />
          </Link>

          <ul className="m-0 hidden list-none items-center gap-1 p-0 lg:flex">
            {[...LINKS.filter((l) => l.href !== "/pathfinder"), { href: "/about", label: "About" }].map(({ href, label }) => {
              const active = isActive(pathname, href);
              return (
                <li key={href}>
                  <Link
                    href={href}
                    aria-current={active ? "page" : undefined}
                    className="inline-flex min-h-10 items-center rounded-md px-3 text-[15px] font-medium no-underline transition-colors hover:bg-[var(--subtle)]"
                    style={{ color: active ? "var(--ink)" : "var(--soft)", background: active ? "var(--subtle)" : undefined }}
                  >
                    {label}
                  </Link>
                </li>
              );
            })}
          </ul>

          <Link href="/pathfinder" className="btn hidden lg:inline-flex">Find my path</Link>
          <Link href="/about" className="inline-flex min-h-11 items-center text-[15px] font-medium no-underline lg:hidden" style={{ color: "var(--soft)" }}>About</Link>
        </nav>
      </header>

      <nav
        aria-label="Main"
        className="fixed inset-x-0 bottom-0 z-[110] lg:hidden"
        style={{ background: "#fff", borderTop: "1px solid var(--border)", paddingBottom: "env(safe-area-inset-bottom)" }}
      >
        <ul className="m-0 grid list-none grid-cols-5 p-0">
          {LINKS.map(({ href, short, icon }) => {
            const active = isActive(pathname, href);
            return (
              <li key={href}>
                <Link
                  href={href}
                  aria-current={active ? "page" : undefined}
                  className="flex h-[60px] flex-col items-center justify-center gap-1 text-[12px] font-medium no-underline active:opacity-70"
                  style={{ color: active ? "var(--indigo)" : "var(--muted)" }}
                >
                  <Icon name={icon} size={22} strokeWidth={active ? 2.2 : 1.8} />
                  {short}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
    </>
  );
}

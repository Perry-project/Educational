"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

const LINKS = [
  { href: "/", label: "Home" },
  { href: "/about", label: "About Us" },
  { href: "/flowchart", label: "Flowchart" },
  { href: "/exams", label: "Exams" },
  { href: "/second-chance", label: "Second Chance" },
  { href: "/pathfinder", label: "Pathfinder" },
];

const isActive = (pathname: string, href: string) =>
  href === "/" ? pathname === "/" : pathname === href || pathname.startsWith(href + "/");

export default function SiteNav() {
  const pathname = usePathname();
  // The phone menu is open only on the page it was opened from, so it closes
  // by itself after navigating. Escape closes it too.
  const [openOn, setOpenOn] = useState<string | null>(null);
  const open = openOn === pathname;
  const setOpen = (o: boolean | ((o: boolean) => boolean)) =>
    setOpenOn((prev) => ((typeof o === "function" ? o(prev === pathname) : o) ? pathname : null));

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setOpenOn(null);
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return (
    <nav className="sticky top-0 z-[100] border-b border-gray-800 bg-gray-900/90 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between gap-4 px-4 sm:px-6 lg:px-8">
        <Link href="/" className="group flex min-h-10 items-center gap-2" aria-label="Perry home">
          <span className="grid h-8 w-8 place-items-center rounded-full bg-gradient-to-br from-blue-400 to-violet-400 text-sm font-extrabold text-gray-900 transition-transform duration-200 group-hover:scale-110">
            P
          </span>
          <span className="brand-gradient text-xl font-bold tracking-wide">PERRY</span>
        </Link>

        <ul className="hidden items-center gap-1 md:flex">
          {LINKS.map(({ href, label }) => {
            const active = isActive(pathname, href);
            return (
              <li key={href}>
                <Link
                  href={href}
                  aria-current={active ? "page" : undefined}
                  className={`whitespace-nowrap rounded-full px-3 py-2 text-sm font-medium transition-colors lg:px-4 ${
                    active ? "bg-white text-gray-900" : "text-gray-300 hover:bg-white/10 hover:text-white"
                  }`}
                >
                  {label}
                </Link>
              </li>
            );
          })}
        </ul>

        <Link
          href="/flowchart"
          className="hidden whitespace-nowrap rounded-lg bg-gradient-to-r from-blue-500 to-violet-500 px-4 py-2 text-sm font-semibold text-white shadow-lg transition hover:from-blue-600 hover:to-violet-600 lg:inline-flex"
        >
          Explore paths
        </Link>

        <button
          type="button"
          onClick={() => setOpen((o) => !o)}
          aria-expanded={open}
          aria-controls="site-nav-menu"
          aria-label={open ? "Close menu" : "Open menu"}
          className="grid h-10 w-10 place-items-center rounded-lg text-white hover:bg-white/10 md:hidden"
        >
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden>
            {open ? <path d="M6 6l12 12M18 6L6 18" /> : <path d="M4 7h16M4 12h16M4 17h16" />}
          </svg>
        </button>
      </div>

      {open && (
        <ul id="site-nav-menu" className="flex flex-col gap-1 border-t border-gray-800 px-4 py-3 md:hidden">
          {LINKS.map(({ href, label }) => {
            const active = isActive(pathname, href);
            return (
              <li key={href}>
                <Link
                  href={href}
                  aria-current={active ? "page" : undefined}
                  className={`block rounded-lg px-4 py-3 text-base font-medium ${
                    active ? "bg-white text-gray-900" : "text-gray-200 hover:bg-white/10"
                  }`}
                >
                  {label}
                </Link>
              </li>
            );
          })}
        </ul>
      )}
    </nav>
  );
}

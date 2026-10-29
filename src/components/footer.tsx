import Link from "next/link";

const LINKS = [
  { href: "/about", label: "About" },
  { href: "/flowchart", label: "Flowchart" },
  { href: "/exams", label: "Exams" },
  { href: "/second-chance", label: "Second Chance" },
  { href: "/pathfinder", label: "Pathfinder" },
  { href: "/disclaimer", label: "Disclaimer" },
  { href: "/privacy", label: "Privacy" },
];

export default function Footer() {
  return (
    <footer className="relative border-t border-gray-800">
      <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-8 text-sm text-gray-400 sm:px-6 lg:flex-row lg:items-start lg:justify-between lg:px-8">
        <div className="flex flex-col gap-1.5">
          <p>
            <span className="brand-gradient font-bold">PERRY</span> · Career guidance for students in Andhra Pradesh and Telangana.
          </p>
          <p className="text-xs text-gray-500">Not a government website. Always confirm dates and rules on the official notice.</p>
        </div>
        <nav aria-label="Footer" className="-my-2 flex flex-wrap gap-x-5">
          {LINKS.map((l) => (
            <Link key={l.href} href={l.href} className="inline-flex min-h-10 items-center hover:text-white">{l.label}</Link>
          ))}
        </nav>
      </div>
    </footer>
  );
}

import Link from "next/link";

export default function Header() {
  return (
    <header className="border-b border-black/10 dark:border-white/15">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        <Link href="/" className="text-lg font-semibold tracking-tight">
          Perry
        </Link>
        <nav className="flex gap-6 text-sm text-black/60 dark:text-white/60">
          <Link href="/flow" className="hover:text-black dark:hover:text-white">
            Flow Explorer
          </Link>
        </nav>
      </div>
    </header>
  );
}

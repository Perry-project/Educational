import Link from "next/link";

export default function Footer() {
  return (
    <footer className="relative border-t border-gray-800">
      <div className="mx-auto flex max-w-7xl flex-col gap-3 px-4 py-8 text-sm text-gray-400 sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
        <p>
          <span className="brand-gradient font-bold">PERRY</span> · Career guidance for students in Andhra Pradesh.
        </p>
        <nav className="flex gap-5">
          <Link href="/about" className="hover:text-white">About</Link>
          <Link href="/flowchart" className="hover:text-white">Flowchart</Link>
          <Link href="/pathfinder" className="hover:text-white">Pathfinder</Link>
        </nav>
      </div>
    </footer>
  );
}

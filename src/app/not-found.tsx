import Link from "next/link";

export const metadata = { title: "Page not found — Perry" };

export default function NotFound() {
  return (
    <div className="site-fade-up mx-auto flex min-h-[calc(100svh-var(--nav-h)-120px)] max-w-xl flex-col items-center justify-center px-4 py-16 text-center">
      <p className="brand-gradient text-6xl font-extrabold">404</p>
      <h1 className="mt-4 text-2xl font-bold tracking-tight">This page isn&apos;t on the map</h1>
      <p className="mt-3 text-gray-400">The link may be old or mistyped. Every route from Class 10 is still on the flowchart.</p>
      <div className="mt-8 flex flex-col gap-3 sm:flex-row">
        <Link href="/flowchart" className="rounded-xl bg-gradient-to-r from-blue-500 to-violet-500 px-6 py-3 font-semibold text-white transition hover:from-blue-600 hover:to-violet-600">
          Open the flowchart
        </Link>
        <Link href="/" className="rounded-xl border border-gray-600 px-6 py-3 font-semibold text-gray-200 transition hover:bg-gray-800 hover:text-white">
          Go home
        </Link>
      </div>
    </div>
  );
}

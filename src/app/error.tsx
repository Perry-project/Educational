"use client";

import Link from "next/link";

// Shown when a page fails, usually because the database couldn't be reached.
export default function Error({ retry }: { error: Error & { digest?: string }; retry: () => void }) {
  return (
    <div className="mx-auto flex min-h-[calc(100svh-var(--nav-h)-120px)] max-w-xl flex-col items-center justify-center px-4 py-16 text-center">
      <h1 className="text-2xl font-bold tracking-tight">Something went wrong</h1>
      <p className="mt-3 text-gray-400">This page couldn&apos;t load just now. Please try again in a moment.</p>
      <div className="mt-8 flex flex-col gap-3 sm:flex-row">
        <button type="button" onClick={() => retry()} className="cursor-pointer rounded-xl bg-gradient-to-r from-blue-500 to-violet-500 px-6 py-3 font-semibold text-white transition hover:from-blue-600 hover:to-violet-600">
          Try again
        </button>
        <Link href="/" className="rounded-xl border border-gray-600 px-6 py-3 font-semibold text-gray-200 transition hover:bg-gray-800 hover:text-white">
          Go home
        </Link>
      </div>
    </div>
  );
}

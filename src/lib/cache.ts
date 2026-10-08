import { unstable_cache } from "next/cache";

// The database changes once a night (the delta import), so page data is
// cached for an hour instead of being read from Neon on every visit. Pages
// still render per request (they read ?career=, ?exam= and so on); only the
// queries are cached. Everything shares one tag, so revalidateTag(DATA_TAG)
// clears it all at once.
export const DATA_TAG = "perry-data";

export const cached = <A extends unknown[], R>(fn: (...args: A) => Promise<R>, key: string) =>
  unstable_cache(fn, [key], { tags: [DATA_TAG], revalidate: 3600 });

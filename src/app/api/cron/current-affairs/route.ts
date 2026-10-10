import { revalidateTag } from "next/cache";
import { pool } from "@/lib/db";
import { fetchAllFeeds } from "@/lib/current-affairs-feeds";
import { NEWS_TAG } from "@/lib/current-affairs-db";

// Vercel Cron calls this at midnight and 6 AM IST (see vercel.json) with
// "Authorization: Bearer $CRON_SECRET". It reads every feed, stores the new
// articles, drops ones older than 60 days and refreshes the page cache.
// Re-running it is harmless: articles are keyed by their URL.

export const dynamic = "force-dynamic";
export const maxDuration = 60;

export async function GET(request: Request) {
  const secret = process.env.CRON_SECRET;
  if (!secret || request.headers.get("authorization") !== `Bearer ${secret}`) {
    return new Response("Unauthorized", { status: 401 });
  }

  const { items, failed } = await fetchAllFeeds();
  // Old articles that are still in a feed would come back after the prune.
  const cutoff = Date.now() - 60 * 24 * 3600 * 1000;
  const fresh = items.filter((i) => i.publishedAt.getTime() > cutoff);

  const { rowCount: added } = await pool.query(
    `INSERT INTO current_affairs (topic, title, summary, url, source_name, published_at, data_tier)
     SELECT * FROM unnest($1::text[], $2::text[], $3::text[], $4::text[], $5::text[], $6::timestamptz[], $7::text[])
     ON CONFLICT (url) DO NOTHING`,
    [
      fresh.map((i) => i.topic),
      fresh.map((i) => i.title),
      fresh.map((i) => i.summary),
      fresh.map((i) => i.url),
      fresh.map((i) => i.source),
      fresh.map((i) => i.publishedAt.toISOString()),
      fresh.map((i) => (i.official ? "tier_1_official" : "tier_2_reported")),
    ],
  );
  const { rowCount: pruned } = await pool.query(
    `DELETE FROM current_affairs WHERE published_at < now() - interval '60 days'`,
  );

  revalidateTag(NEWS_TAG, { expire: 0 });
  return Response.json({ fetched: items.length, added, pruned, failed });
}

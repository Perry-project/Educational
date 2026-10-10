import { unstable_cache } from "next/cache";
import { pool } from "./db";
import { DATA_TAG } from "./cache";
import type { TopicId } from "./current-affairs-feeds";

// What the /current-affairs page shows: the last week of the current_affairs
// table, newest first. The cron route clears NEWS_TAG after each fetch, so
// new articles show up straight away rather than after the hour-long cache.

export const NEWS_TAG = "perry-news";
export const NEWS_DAYS = 7;

export type NewsItem = {
  id: number;
  topic: TopicId;
  title: string;
  summary: string | null;
  url: string;
  source: string;
  official: boolean;
  publishedAt: string; // ISO
};

export type NewsFeed = { items: NewsItem[]; updatedAt: string | null };

async function readNews(): Promise<NewsFeed> {
  const [{ rows }, { rows: last }] = await Promise.all([
    pool.query(
      `SELECT id, topic, title, summary, url, source_name, data_tier, published_at
       FROM current_affairs
       WHERE published_at > now() - make_interval(days => $1)
       ORDER BY published_at DESC
       LIMIT 1500`,
      [NEWS_DAYS],
    ),
    pool.query(`SELECT max(fetched_at) AS at FROM current_affairs`),
  ]);
  return {
    items: rows.map((r) => ({
      id: r.id,
      topic: r.topic,
      title: r.title,
      summary: r.summary,
      url: r.url,
      source: r.source_name,
      official: r.data_tier === "tier_1_official",
      publishedAt: new Date(r.published_at).toISOString(),
    })),
    updatedAt: last[0]?.at ? new Date(last[0].at).toISOString() : null,
  };
}

export const getNews = unstable_cache(readNews, ["current-affairs"], { tags: [NEWS_TAG, DATA_TAG], revalidate: 3600 });

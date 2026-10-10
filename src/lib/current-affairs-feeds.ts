// The feeds behind the /current-affairs tab, and the code that reads them.
// The cron route (app/api/cron/current-affairs) calls fetchAllFeeds() every
// night and morning and stores what comes back in the current_affairs table.
//
// Every item is a headline, a short summary and a link to the original. The
// RBI's own press releases are official (tier_1_official); everything from a
// news outlet is tier_2_reported and the page names the outlet on each item.
//
// Feeds are read in order and an article keeps the topic of the first feed
// it appears in, so the narrower feeds (Andhra Pradesh, Economy) come before
// the broad ones (National, Business).

export const TOPICS = [
  { id: "exams", label: "Exams & Education" },
  { id: "jobs", label: "Jobs & Careers" },
  { id: "states", label: "AP & Telangana" },
  { id: "india", label: "India & Politics" },
  { id: "economy", label: "Economy & Business" },
  { id: "environment", label: "Environment" },
  { id: "science", label: "Science & Tech" },
  { id: "world", label: "World" },
  { id: "sports", label: "Sports" },
] as const;

export type TopicId = (typeof TOPICS)[number]["id"];

type Feed = { url: string; topic: TopicId; source: string; official?: boolean };

const HINDU = (section: string) => `https://www.thehindu.com/${section}/feeder/default.rss`;

export const FEEDS: Feed[] = [
  { url: "https://indianexpress.com/section/education/feed/", topic: "exams", source: "The Indian Express" },
  { url: HINDU("education"), topic: "exams", source: "The Hindu" },
  { url: "https://www.hindustantimes.com/feeds/rss/education/rssfeed.xml", topic: "exams", source: "Hindustan Times" },
  { url: HINDU("education/careers"), topic: "jobs", source: "The Hindu" },
  { url: HINDU("news/national/andhra-pradesh"), topic: "states", source: "The Hindu" },
  { url: HINDU("news/national/telangana"), topic: "states", source: "The Hindu" },
  { url: "https://www.rbi.org.in/pressreleases_rss.xml", topic: "economy", source: "Reserve Bank of India", official: true },
  { url: HINDU("business/Economy"), topic: "economy", source: "The Hindu" },
  { url: HINDU("sci-tech/energy-and-environment"), topic: "environment", source: "The Hindu" },
  { url: HINDU("sci-tech/science"), topic: "science", source: "The Hindu" },
  { url: HINDU("sci-tech/technology"), topic: "science", source: "The Hindu" },
  { url: HINDU("news/national"), topic: "india", source: "The Hindu" },
  { url: HINDU("business"), topic: "economy", source: "The Hindu" },
  { url: HINDU("news/international"), topic: "world", source: "The Hindu" },
  { url: HINDU("sport"), topic: "sports", source: "The Hindu" },
];

// Recruitment news turns up in the education and state feeds too; it belongs
// under Jobs wherever it was found.
const JOBS = /\b(recruitment|vacanc(y|ies)|hiring|job notification|posts? (notified|filled)|walk-in)\b/i;

export type FeedItem = {
  topic: TopicId;
  title: string;
  summary: string | null;
  url: string;
  source: string;
  publishedAt: Date;
  official: boolean;
};

const ENTITIES: Record<string, string> = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " " };

const decode = (s: string) =>
  s.replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (m, e: string) =>
    e[0] === "#"
      ? String.fromCodePoint(e[1] === "x" || e[1] === "X" ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10))
      : ENTITIES[e.toLowerCase()] ?? m,
  );

const tag = (item: string, name: string) => {
  const m = item.match(new RegExp(`<${name}(?:\\s[^>]*)?>([\\s\\S]*?)</${name}>`, "i"));
  if (!m) return null;
  return m[1].replace(/^\s*<!\[CDATA\[([\s\S]*?)\]\]>\s*$/, "$1").trim();
};

// Descriptions can be HTML (the RBI sends the whole release); keep the first
// couple of sentences as plain text.
const plain = (html: string | null, max = 280) => {
  if (!html) return null;
  const t = decode(decode(html).replace(/<[^>]+>/g, " ")).replace(/\s+/g, " ").trim();
  if (!t) return null;
  if (t.length <= max) return t;
  const cut = t.slice(0, max);
  const end = Math.max(cut.lastIndexOf(". "), cut.lastIndexOf("? "));
  return end > max * 0.5 ? cut.slice(0, end + 1) : cut.replace(/\s+\S*$/, "") + "…";
};

// RFC 822 dates; the RBI leaves out the zone, and its times are IST.
const parseDate = (s: string | null) => {
  if (!s) return null;
  const withZone = /[+-]\d{4}$|GMT$|Z$|[A-Z]{3}$/.test(s.trim()) ? s : `${s} +0530`;
  const d = new Date(withZone);
  return isNaN(d.getTime()) ? null : d;
};

export function parseFeed(xml: string, feed: Feed, now = new Date()): FeedItem[] {
  const items: FeedItem[] = [];
  for (const [, body] of xml.matchAll(/<item[\s>]([\s\S]*?)<\/item>/gi)) {
    const title = plain(tag(body, "title"), 300);
    const url = decode(tag(body, "link") ?? "").trim();
    if (!title || !/^https?:\/\//.test(url)) continue;
    const summary = plain(tag(body, "description"));
    items.push({
      topic: JOBS.test(title) ? "jobs" : feed.topic,
      title,
      // Some feeds repeat the headline as the description.
      summary: summary && summary !== title ? summary : null,
      url,
      source: feed.source,
      publishedAt: parseDate(tag(body, "pubDate")) ?? now,
      official: !!feed.official,
    });
  }
  return items;
}

const UA = "Mozilla/5.0 (compatible; PerryBot/1.0; +https://perry-inky.vercel.app)";

export async function fetchAllFeeds(): Promise<{ items: FeedItem[]; failed: string[] }> {
  const failed: string[] = [];
  const results = await Promise.all(
    FEEDS.map(async (feed) => {
      try {
        const res = await fetch(feed.url, {
          headers: { "User-Agent": UA, Accept: "application/rss+xml, application/xml, text/xml" },
          signal: AbortSignal.timeout(15000),
          cache: "no-store",
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return parseFeed(await res.text(), feed);
      } catch (e) {
        failed.push(`${feed.url}: ${e instanceof Error ? e.message : e}`);
        return [];
      }
    }),
  );
  // Results stay in FEEDS order, so the first feed to carry an article wins.
  const seen = new Set<string>();
  const items = results.flat().filter((i) => !seen.has(i.url) && !!seen.add(i.url));
  return { items, failed };
}

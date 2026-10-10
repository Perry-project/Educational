"use client";

import { useEffect, useMemo, useState, type CSSProperties } from "react";
import "./metro-flow.css";
import { TOPICS, type TopicId } from "@/lib/current-affairs-feeds";
import type { NewsItem } from "@/lib/current-affairs-db";

// The /current-affairs page: the last week's news for exam aspirants, sorted
// into topics. Pick a day, then a topic; "All topics" shows the top few
// stories of each. Search looks across the whole week. Every story links to
// its original and names who reported it.
//
// The URL keeps ?day= and ?topic= so a view can be shared.

const COLOR: Record<TopicId, string> = {
  exams: "#75aef5",
  jobs: "#68c4b8",
  states: "#f0b44c",
  india: "#f29676",
  economy: "#c39cf5",
  environment: "#7fcf86",
  science: "#5fc8e8",
  world: "#e88fb8",
  sports: "#d9c769",
};
const LABEL = Object.fromEntries(TOPICS.map((t) => [t.id, t.label])) as Record<TopicId, string>;
const PER_TOPIC = 5; // stories per topic in the "All topics" view
const PAGE = 30; // stories before "Show more" in one topic

const display = "var(--metro-display), var(--metro-body), system-ui, sans-serif";
const IST = "Asia/Kolkata";
const dayKey = (iso: string) => new Intl.DateTimeFormat("en-CA", { timeZone: IST }).format(new Date(iso));
const time = (iso: string) =>
  new Intl.DateTimeFormat("en-IN", { timeZone: IST, hour: "numeric", minute: "2-digit", hour12: true }).format(new Date(iso));
const dayLabel = (key: string, today: string) => {
  const diff = Math.round((Date.parse(today) - Date.parse(key)) / 86400000);
  if (diff === 0) return "Today";
  if (diff === 1) return "Yesterday";
  return new Intl.DateTimeFormat("en-IN", { timeZone: "UTC", weekday: "short", day: "numeric", month: "short" }).format(new Date(key));
};

export type CurrentAffairsView = { day: string | null; topic: string | null };

export default function CurrentAffairs({
  items, updatedAt, today, initial, bodyFont, displayFont,
}: {
  items: NewsItem[];
  updatedAt: string | null;
  today: string; // YYYY-MM-DD in IST, from the server so both renders agree
  initial: CurrentAffairsView;
  bodyFont: string;
  displayFont: string;
}) {
  const days = useMemo(() => {
    const keys = [...new Set(items.map((i) => dayKey(i.publishedAt)))].sort().reverse();
    return keys.includes(today) ? keys : [today, ...keys];
  }, [items, today]);

  const [day, setDay] = useState(days.includes(initial.day ?? "") ? initial.day! : days[0]);
  const [topic, setTopic] = useState<TopicId | null>(TOPICS.find((t) => t.id === initial.topic)?.id ?? null);
  const [query, setQuery] = useState("");
  const [limit, setLimit] = useState(PAGE);

  useEffect(() => {
    const url = new URL(window.location.href);
    const set = (k: string, v: string | null) => (v ? url.searchParams.set(k, v) : url.searchParams.delete(k));
    set("day", day === days[0] ? null : day);
    set("topic", topic);
    window.history.replaceState(window.history.state, "", url);
  }, [day, topic, days]);

  const q = query.trim().toLowerCase();
  const onDay = useMemo(() => items.filter((i) => dayKey(i.publishedAt) === day), [items, day]);
  const counts = useMemo(() => {
    const c: Partial<Record<TopicId, number>> = {};
    for (const i of onDay) c[i.topic] = (c[i.topic] ?? 0) + 1;
    return c;
  }, [onDay]);
  const results = useMemo(
    () => (q ? items.filter((i) => `${i.title} ${i.summary ?? ""}`.toLowerCase().includes(q) && (!topic || i.topic === topic)) : []),
    [items, q, topic],
  );

  const pickTopic = (t: TopicId | null) => {
    setTopic(t);
    setLimit(PAGE);
    if (t) requestAnimationFrame(() => document.getElementById("news-h")?.scrollIntoView({ behavior: "smooth", block: "start" }));
  };

  const rootStyle = { "--metro-body": bodyFont, "--metro-display": displayFont, fontFamily: bodyFont } as CSSProperties;
  const chip = (on: boolean): CSSProperties => ({
    background: on ? "var(--surface)" : "transparent", color: on ? "var(--ink)" : "var(--muted)", fontFamily: "inherit",
  });
  const topicList = topic ? onDay.filter((i) => i.topic === topic) : [];

  return (
    <div className="metro min-h-[calc(100vh-var(--nav-h))]" style={rootStyle}>
      <div className="mx-auto flex max-w-[1100px] flex-col gap-8 px-5 pt-8 pb-16 lg:px-12">
        <header className="flex flex-col gap-3">
          <h1 className="m-0 text-[34px] leading-[1.08] font-extrabold tracking-tight lg:text-[44px]" style={{ fontFamily: display }}>
            Current Affairs
          </h1>
          <p className="m-0 max-w-2xl text-base leading-relaxed lg:text-lg" style={{ color: "var(--muted)" }}>
            The day’s news for exam preparation, sorted by topic: exams, jobs, Andhra Pradesh and Telangana, India, the economy, environment, science, world and sports. Refreshed every night and morning.
          </p>
          {updatedAt && (
            <p className="m-0 text-[13px]" style={{ color: "var(--muted)" }}>
              Last updated {dayLabel(dayKey(updatedAt), today).replace(/^(Today|Yesterday)$/, (d) => d.toLowerCase())}, {time(updatedAt)} IST
            </p>
          )}
        </header>

        <section className="flex flex-col gap-4" aria-label="Choose news">
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search this week’s news, e.g. APPSC, repo rate, monsoon"
            aria-label="Search this week’s news"
            className="c10-search h-12 w-full rounded-xl border px-4 text-[15px]"
            style={{ background: "var(--panel)", borderColor: "var(--line)", color: "var(--ink)", fontFamily: "inherit" }}
          />
          {!q && (
            <div role="group" aria-label="Day" className="-mx-5 flex gap-1 overflow-x-auto px-5 lg:mx-0 lg:px-0">
              {days.map((d) => (
                <button key={d} onClick={() => { setDay(d); setLimit(PAGE); }} aria-pressed={day === d}
                  className="metro-chip h-11 shrink-0 cursor-pointer rounded-full border-0 px-4 text-sm font-semibold" style={chip(day === d)}>
                  {dayLabel(d, today)}
                </button>
              ))}
            </div>
          )}
          <div role="group" aria-label="Topic" className="flex flex-wrap gap-2">
            <TopicChip on={!topic} color="var(--accent)" label="All topics" count={q ? undefined : onDay.length} onClick={() => pickTopic(null)} />
            {TOPICS.map((t) => (
              <TopicChip key={t.id} on={topic === t.id} color={COLOR[t.id]} label={t.label} count={q ? undefined : counts[t.id] ?? 0}
                onClick={() => pickTopic(topic === t.id ? null : t.id)} />
            ))}
          </div>
        </section>

        {q ? (
          <section className="flex flex-col gap-3" aria-labelledby="news-h">
            <h2 id="news-h" className="m-0 text-xl font-extrabold" style={{ fontFamily: display }}>
              {results.length} {results.length === 1 ? "story" : "stories"} this week{topic && ` in ${LABEL[topic]}`}
            </h2>
            <StoryList items={results.slice(0, limit)} today={today} showDay showTopic={!topic} />
            {results.length > limit && <MoreButton onClick={() => setLimit(limit + PAGE)} left={results.length - limit} />}
          </section>
        ) : topic ? (
          <section className="flex flex-col gap-3" aria-labelledby="news-h">
            <h2 id="news-h" className="m-0 flex items-center gap-2.5 text-2xl font-extrabold" style={{ fontFamily: display, scrollMarginTop: "calc(var(--nav-h) + 16px)" }}>
              <span className="h-3 w-3 rounded-full" style={{ background: COLOR[topic] }} />
              {LABEL[topic]}
            </h2>
            {topicList.length === 0 ? (
              <Empty day={dayLabel(day, today)} />
            ) : (
              <>
                <StoryList items={topicList.slice(0, limit)} today={today} />
                {topicList.length > limit && <MoreButton onClick={() => setLimit(limit + PAGE)} left={topicList.length - limit} />}
              </>
            )}
          </section>
        ) : onDay.length === 0 ? (
          <Empty day={dayLabel(day, today)} />
        ) : (
          <div className="grid gap-x-10 gap-y-9 lg:grid-cols-2">
            {TOPICS.filter((t) => counts[t.id]).map((t) => {
              const list = onDay.filter((i) => i.topic === t.id);
              return (
                <section key={t.id} className="flex min-w-0 flex-col gap-2" aria-labelledby={`t-${t.id}`}>
                  <h2 id={`t-${t.id}`} className="m-0 flex items-center gap-2.5 border-b pb-2 text-lg font-extrabold" style={{ fontFamily: display, borderColor: "var(--rule)" }}>
                    <span className="h-2.5 w-2.5 rounded-full" style={{ background: COLOR[t.id] }} />
                    {t.label}
                  </h2>
                  <StoryList items={list.slice(0, PER_TOPIC)} today={today} compact />
                  {list.length > PER_TOPIC && (
                    <button onClick={() => pickTopic(t.id)} className="metro-row cursor-pointer self-start rounded-lg border-0 px-3 py-2 text-sm font-semibold"
                      style={{ background: "transparent", color: COLOR[t.id], fontFamily: "inherit" }}>
                      All {list.length} in {t.label} →
                    </button>
                  )}
                </section>
              );
            })}
          </div>
        )}

        <p className="m-0 text-[13px] leading-relaxed" style={{ color: "var(--muted)" }}>
          Headlines and summaries come from each source’s public news feed: official releases (marked Official) and named newspapers. Tap a story to read it in full at the source. For exam and job dates, always confirm on the official notification.
        </p>
      </div>
    </div>
  );
}

function TopicChip({ on, color, label, count, onClick }: { on: boolean; color: string; label: string; count?: number; onClick: () => void }) {
  return (
    <button onClick={onClick} aria-pressed={on}
      className="metro-row flex h-11 cursor-pointer items-center gap-2 rounded-full px-4 text-sm font-semibold"
      style={{ background: on ? "var(--surface)" : "transparent", color: on ? "var(--ink)" : "var(--muted)", border: `1px solid ${on ? color : "var(--line)"}`, fontFamily: "inherit" }}>
      <span className="h-2 w-2 rounded-full" style={{ background: color }} />
      {label}
      {count !== undefined && <span className="tabular-nums" style={{ color: "var(--muted)" }}>{count}</span>}
    </button>
  );
}

function StoryList({ items, today, compact, showDay, showTopic }: { items: NewsItem[]; today: string; compact?: boolean; showDay?: boolean; showTopic?: boolean }) {
  return (
    <ul className="m-0 flex list-none flex-col p-0">
      {items.map((i) => (
        <li key={i.id}>
          <a href={i.url} target="_blank" rel="noopener noreferrer"
            className="metro-row -mx-3 flex flex-col gap-1 rounded-xl px-3 py-3 no-underline" style={{ color: "var(--ink)" }}>
            <span className={`${compact ? "text-[15px]" : "text-[16px]"} leading-snug font-bold`}>{i.title}</span>
            {!compact && i.summary && (
              <span className="text-[14px] leading-relaxed" style={{ color: "#c9d0dc" }}>{i.summary}</span>
            )}
            <span className="flex flex-wrap items-center gap-x-2 text-[12.5px]" style={{ color: "var(--muted)" }}>
              {i.official ? (
                <span className="rounded px-1.5 py-px font-semibold" style={{ background: "#1f3a2c", color: "#8fe0a8" }}>Official · {i.source}</span>
              ) : (
                <span>Reported by {i.source}</span>
              )}
              {showTopic && <span style={{ color: COLOR[i.topic] }}>{LABEL[i.topic]}</span>}
              <span>{showDay ? `${dayLabel(dayKey(i.publishedAt), today)}, ` : ""}{time(i.publishedAt)}</span>
            </span>
          </a>
        </li>
      ))}
    </ul>
  );
}

function MoreButton({ onClick, left }: { onClick: () => void; left: number }) {
  return (
    <button onClick={onClick} className="metro-chip h-11 cursor-pointer self-start rounded-full border px-5 text-sm font-semibold"
      style={{ background: "transparent", borderColor: "var(--line)", color: "var(--ink)", fontFamily: "inherit" }}>
      Show more ({left} left)
    </button>
  );
}

function Empty({ day }: { day: string }) {
  return (
    <p className="m-0 text-[15px]" style={{ color: "var(--muted)" }}>
      No stories here for {day.replace(/^(Today|Yesterday)$/, (d) => d.toLowerCase())} yet. The next update runs at midnight and 6 AM IST.
    </p>
  );
}

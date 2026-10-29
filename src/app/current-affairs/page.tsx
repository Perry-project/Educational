import { SYSTEM_FONT } from "@/lib/fonts";
import CurrentAffairs from "@/components/current-affairs";
import { getNews } from "@/lib/current-affairs-db";


export const metadata = {
  title: "Current Affairs — Perry",
  description: "Daily current affairs for APPSC, UPSC, SSC and bank exam preparation: exams, jobs, Andhra Pradesh and Telangana, India, economy, environment, science, world and sports.",
};

// Rendered per request; the news read is cached and cleared by each cron run.
export const dynamic = "force-dynamic";

const param = (v: string | string[] | undefined) => (typeof v === "string" && v ? v : null);

export default async function CurrentAffairsPage({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const sp = await searchParams;
  const { items, updatedAt } = await getNews();
  const today = new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Kolkata" }).format(new Date());
  return (
    <CurrentAffairs
      items={items} updatedAt={updatedAt} today={today}
      initial={{ day: param(sp.day), topic: param(sp.topic) }}
      bodyFont={SYSTEM_FONT} displayFont={SYSTEM_FONT}
    />
  );
}

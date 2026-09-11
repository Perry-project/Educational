import type { DataTier, NodeTier } from "@/lib/flow-data";

const TIER_STYLE: Record<DataTier, { label: string; className: string }> = {
  tier_1_official: {
    label: "Official — verified",
    className: "bg-emerald-600/15 text-emerald-700 dark:text-emerald-400",
  },
  tier_2_reported: {
    label: "Reported — range only",
    className: "bg-amber-500/15 text-amber-700 dark:text-amber-400",
  },
  tier_3_advisory: {
    label: "AI-assisted — advisory",
    className: "bg-sky-500/15 text-sky-700 dark:text-sky-400",
  },
  pending_review: {
    label: "Unverified — confirm before relying on this",
    className: "bg-black/10 text-black/60 dark:bg-white/10 dark:text-white/60",
  },
};

export function TierBadge({ tier }: { tier: NodeTier | undefined }) {
  if (!tier) return null;
  const style = TIER_STYLE[tier.dataTier];

  return (
    <div className="flex flex-col gap-1">
      <span
        className={`inline-flex w-fit items-center rounded-full px-2 py-0.5 text-[11px] font-semibold ${style.className}`}
      >
        {style.label}
      </span>
      {tier.dataTier === "tier_1_official" && tier.verifiedDate && (
        <span className="text-[11px] text-black/45 dark:text-white/45">
          Verified {tier.verifiedDate.slice(0, 10)}
          {tier.source ? " · source on file" : ""}
        </span>
      )}
    </div>
  );
}

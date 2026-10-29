import Link from "next/link";
import PolicyPage from "@/components/policy-page";

export const metadata = {
  title: "Disclaimer — Perry",
  description: "How to use the information on Perry, and why to confirm it with the official source before you apply.",
};

const link = "font-medium text-blue-400 hover:text-blue-300";

export default function Disclaimer() {
  return (
    <PolicyPage
      title="Disclaimer"
      updated="6 October 2026"
      intro={
        <p>
          Perry is a free guide to help students and parents see their options. It is not a government website, and it
          is not linked to any exam board, university, college or recruiting body.
        </p>
      }
      sections={[
        {
          heading: "Always check the official notice",
          body: (
            <>
              <p>
                Exam dates, eligibility rules, fees, seat numbers and qualifying marks are taken from each body&apos;s
                latest official notification. These change every year, sometimes at short notice. Before you apply,
                pay a fee or make an admission decision, open the official website linked on each exam or route and
                confirm the details there.
              </p>
              <p>If Perry and the official notice disagree, the official notice is always right.</p>
            </>
          ),
        },
        {
          heading: "Details still being checked",
          body: (
            <p>
              Some exams, routes, courses and colleges are still being checked against their official documents. These
              show only a name and the official website, marked &ldquo;Details soon&rdquo;, until that check is done.
              Where something isn&apos;t published yet, Perry says &ldquo;Not announced&rdquo; instead of guessing.
            </p>
          ),
        },
        {
          heading: "Suggestions are a starting point",
          body: (
            <p>
              The <Link href="/pathfinder" className={link}>Pathfinder</Link> questions and the study topics for each
              course are written with the help of AI. They are ideas to explore, not advice about what you should
              choose. Talk them over with your family, teachers or a counsellor.
            </p>
          ),
        },
        {
          heading: "No guarantees",
          body: (
            <p>
              Perry does its best to keep everything accurate and current, but it can&apos;t promise that every detail
              is complete or error-free, and it isn&apos;t responsible for decisions made using it. Perry never
              guarantees admission, a rank, a seat or a job.
            </p>
          ),
        },
        {
          heading: "Other websites",
          body: (
            <p>
              Perry links to official websites so you can check things for yourself. Those sites are run by their own
              organisations, and Perry has no control over what they show.
            </p>
          ),
        },
      ]}
    />
  );
}

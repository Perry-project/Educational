import PolicyPage from "@/components/policy-page";

export const metadata = {
  title: "Privacy — Perry",
  description: "Perry needs no account and doesn't collect personal information.",
};

export default function Privacy() {
  return (
    <PolicyPage
      title="Privacy"
      updated="6 October 2026"
      intro={<p>Perry is free to use without an account. You never have to tell us who you are.</p>}
      sections={[
        {
          heading: "What we collect",
          body: (
            <>
              <p>
                Nothing personal. Perry has no sign-up, no forms and no login. Your answers to the Pathfinder
                questions stay in your browser and are never sent to us.
              </p>
              <p>Perry doesn&apos;t use advertising, tracking cookies or analytics tools.</p>
            </>
          ),
        },
        {
          heading: "Basic server records",
          body: (
            <p>
              Like any website, the service that hosts Perry automatically keeps short-lived technical records of
              requests, such as the time, the page asked for, your IP address and browser type. These are used only to
              keep the site running and secure, and are not used to identify you.
            </p>
          ),
        },
        {
          heading: "Links you share",
          body: (
            <p>
              Some Perry addresses include the career, exam or route you were looking at, so you can share that view.
              They contain only those choices, nothing about you.
            </p>
          ),
        },
        {
          heading: "Other websites",
          body: (
            <p>
              Official websites that Perry links to have their own privacy policies. Please read those before giving
              them any personal details.
            </p>
          ),
        },
        {
          heading: "Changes",
          body: <p>If this ever changes, for example if Perry adds accounts, this page will be updated first.</p>,
        },
      ]}
    />
  );
}

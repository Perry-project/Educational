// The site's public address, for the sitemap, robots.txt and share previews.
// Set SITE_URL once a domain is chosen; on Vercel the production address is
// used until then.
export const SITE_URL = (
  process.env.SITE_URL ??
  (process.env.VERCEL_PROJECT_PRODUCTION_URL ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}` : "http://localhost:3000")
).replace(/\/$/, "");

export const SITE_NAME = "Perry";
export const SITE_DESCRIPTION = "See every route from Class 10 to a career, clearly and step by step.";

// Every public page, for the sitemap.
export const PAGES = ["/", "/flowchart", "/exams", "/second-chance", "/pathfinder", "/about", "/disclaimer", "/privacy"];

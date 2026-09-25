import type { NextConfig } from "next";
import path from "path";

const nextConfig: NextConfig = {
  turbopack: {
    root: path.resolve(__dirname),
  },
  // The flowchart used to live at /flow.
  redirects() {
    return [{ source: "/flow", destination: "/flowchart", permanent: true }];
  },
};

export default nextConfig;

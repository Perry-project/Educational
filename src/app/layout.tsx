import type { Metadata, Viewport } from "next";
import "./globals.css";
import SiteNav from "@/components/site-nav";
import Footer from "@/components/footer";
import { SITE_DESCRIPTION, SITE_NAME, SITE_URL } from "@/lib/site";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: SITE_NAME,
  description: SITE_DESCRIPTION,
  openGraph: { siteName: SITE_NAME, type: "website", locale: "en_IN" },
  twitter: { card: "summary_large_image" },
};

export const viewport: Viewport = {
  themeColor: "#ffffff",
  colorScheme: "light",
  viewportFit: "cover",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="flex min-h-full flex-col overflow-x-hidden">
        <SiteNav />
        <main className="relative flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}

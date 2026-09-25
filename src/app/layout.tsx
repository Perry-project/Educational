import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import SiteNav from "@/components/site-nav";
import Footer from "@/components/footer";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Perry",
  description: "See every route from Class 10 to a career, clearly and step by step.",
};

export const viewport: Viewport = {
  themeColor: "#111827",
  colorScheme: "dark",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`dark ${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="flex min-h-full flex-col overflow-x-hidden">
        <div className="site-glow" aria-hidden />
        <SiteNav />
        <main className="relative z-10 flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}

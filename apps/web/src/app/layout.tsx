import type { Metadata, Viewport } from "next";
import { Be_Vietnam_Pro, JetBrains_Mono } from "next/font/google";
import { Providers } from "@/components/providers";
import "./globals.css";

const beVietnam = Be_Vietnam_Pro({
  subsets: ["latin", "vietnamese"],
  weight: ["400", "500", "700"],
  variable: "--font-sans-face",
  display: "swap",
});

const mono = JetBrains_Mono({
  subsets: ["latin", "vietnamese"],
  weight: ["400", "500"],
  variable: "--font-mono-face",
  display: "swap",
});

const BASE = process.env.NEXT_PUBLIC_BASE_PATH || "";

export const metadata: Metadata = {
  title: "PyAI Path · Python for AI Engineers",
  description: "Bilingual (VI/EN) Python learning path for AI engineers: lessons, in-browser Python, exercises with tests, quizzes, spaced repetition and mock exams.",
  appleWebApp: {
    capable: true,
    title: "PyAI Path",
    statusBarStyle: "default",
  },
  other: {
    "apple-mobile-web-app-capable": "yes",
  },
  icons: {
    icon: [
      { url: `${BASE}/favicon.svg`, type: "image/svg+xml" },
      { url: `${BASE}/icons/icon-192.png`, sizes: "192x192", type: "image/png" },
    ],
    apple: [{ url: `${BASE}/icons/apple-touch-icon.png`, sizes: "180x180", type: "image/png" }],
  },
};

export const viewport: Viewport = {
  viewportFit: "cover",
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#faf7ef" },
    { media: "(prefers-color-scheme: dark)", color: "#040807" },
  ],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi" suppressHydrationWarning className={`${beVietnam.variable} ${mono.variable}`}>
      <body className="font-sans antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}

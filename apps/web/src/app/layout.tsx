import type { Metadata, Viewport } from "next";
import { Bungee, Chivo, JetBrains_Mono, Silkscreen } from "next/font/google";
import { Providers } from "@/components/providers";
import "./globals.css";

const chivo = Chivo({ subsets: ["latin", "vietnamese"], variable: "--font-chivo", display: "swap" });
const bungee = Bungee({ subsets: ["latin", "vietnamese"], weight: "400", variable: "--font-bungee", display: "swap" });
const pixel = Silkscreen({ subsets: ["latin"], weight: "700", variable: "--font-silkscreen", display: "swap" });
const mono = JetBrains_Mono({ subsets: ["latin", "vietnamese"], variable: "--font-mono-face", display: "swap" });

export const metadata: Metadata = {
  title: "PyAI Path · Python for AI Engineers",
  description: "Bilingual (VI/EN) Python learning path for AI engineers: lessons, in-browser Python, exercises with tests, quizzes, spaced repetition and mock exams.",
  icons: { icon: "/favicon.svg" },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#f8f3e4" },
    { media: "(prefers-color-scheme: dark)", color: "#170e1b" },
  ],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi" suppressHydrationWarning className={`${chivo.variable} ${bungee.variable} ${pixel.variable} ${mono.variable}`}>
      <body className="font-sans antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}

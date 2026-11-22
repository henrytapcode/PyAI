import type { MetadataRoute } from "next";

export const dynamic = "force-static";

const BASE = process.env.NEXT_PUBLIC_BASE_PATH || "";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "PyAI Path · Python for AI Engineers",
    short_name: "PyAI Path",
    description:
      "Bilingual (VI/EN) Python learning path for AI engineers: lessons, in-browser Python, exercises with tests, quizzes, spaced repetition and mock exams.",
    start_url: `${BASE}/`,
    scope: `${BASE}/`,
    display: "standalone",
    orientation: "any",
    background_color: "#faf7ef",
    theme_color: "#107c55",
    icons: [
      {
        src: `${BASE}/icons/icon-192.png`,
        sizes: "192x192",
        type: "image/png",
        purpose: "any",
      },
      {
        src: `${BASE}/icons/icon-512.png`,
        sizes: "512x512",
        type: "image/png",
        purpose: "any",
      },
      {
        src: `${BASE}/icons/icon-512.png`,
        sizes: "512x512",
        type: "image/png",
        purpose: "maskable",
      },
    ],
  };
}

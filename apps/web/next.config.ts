import type { NextConfig } from "next";

// On GitHub Pages the site lives under /<repo>; the workflow sets NEXT_PUBLIC_BASE_PATH.
const basePath = process.env.NEXT_PUBLIC_BASE_PATH || "";

const nextConfig: NextConfig = {
  basePath,
  // Fully static: `pnpm build` writes ./out, which runs anywhere without a server.
  output: "export",
  trailingSlash: true,
  images: { unoptimized: true },
};

export default nextConfig;

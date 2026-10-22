import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Fully static: `pnpm build` writes ./out, which runs anywhere without a server.
  output: "export",
  trailingSlash: true,
  images: { unoptimized: true },
};

export default nextConfig;

import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // The app is fully client-side, so it builds to static files in out/
  // that can be served by nginx or any static host
  output: "export",
};

export default nextConfig;

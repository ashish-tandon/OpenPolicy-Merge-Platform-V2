import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Stability configurations
  experimental: {
    // Disable problematic features
    turbo: {
      rules: {
        '*.svg': {
          loaders: ['@svgr/webpack'],
          as: '*.js',
        },
      },
    },
  },

  // Performance optimizations
  swcMinify: true,

  // File watching optimizations
  webpack: (config, { dev, isServer }) => {
    if (dev && !isServer) {
      // Reduce file watching overhead
      config.watchOptions = {
        poll: 1000,
        aggregateTimeout: 300,
        ignored: ['**/node_modules', '**/.git', '**/.next'],
      };
    }
    return config;
  },

  // Reduce memory usage
  onDemandEntries: {
    maxInactiveAge: 25 * 1000,
    pagesBufferLength: 2,
  },
};

export default nextConfig;

/** @type {import('next').NextConfig} */
const { i18n } = require('./next-i18next.config')

const nextConfig = {
  i18n,
  reactStrictMode: true,
  // Enable static exports for better performance
  output: 'standalone',
  // Image optimization
  images: {
    domains: ['localhost', 'api.openparliament.ca'],
  },
}

module.exports = nextConfig
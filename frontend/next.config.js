/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  async rewrites() {
    return {
      fallback: [
        {
          source: '/api/:path*',
          destination: 'https://api-domain.vercel.app/api/:path*'
        }
      ]
    };
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000/api'
  }
};

module.exports = nextConfig;
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Server build lo lint/type errors valla build fail avvakudadu (Telugu text lo quotes common)
  eslint: { ignoreDuringBuilds: true },
  typescript: { ignoreBuildErrors: true },

  // /api/* ni backend ki proxy — browser localhost ni touch cheyyadu (CORS + docker friendly)
  // Docker: BACKEND_URL=http://backend:8000 · Local/sandbox: http://localhost:8000
  async rewrites() {
    const backend = process.env.BACKEND_URL || 'http://localhost:8000';
    return [
      { source: '/api/:path*', destination: `${backend}/api/:path*` },
      { source: '/docs', destination: `${backend}/docs` },
      { source: '/openapi.json', destination: `${backend}/openapi.json` },
      { source: '/cards/:path*', destination: `${backend}/cards/:path*` },
      { source: '/photos/:path*', destination: `${backend}/photos/:path*` },
    ];
  },

  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          { key: 'X-Frame-Options', value: 'ALLOWALL' },
        ],
      },
    ];
  },
};

export default nextConfig;

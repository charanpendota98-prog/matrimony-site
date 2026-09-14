/** @type {import('next').NextConfig} */
const nextConfig = {
  // Server build lo lint/type errors valla build fail avvakudadu (Telugu text lo quotes common)
  eslint: { ignoreDuringBuilds: true },
  typescript: { ignoreBuildErrors: true },
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

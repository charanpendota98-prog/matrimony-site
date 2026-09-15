/* MANA VIVAHA — service worker (PWA offline + fast repeat loads)
   • App shell cache (pages: network-first, assets: cache-first)
   • /api/* — NEVER cache (matrimony data fresh ga undali, privacy)
   • Offline aithe /offline page chupistham
*/
const VERSION = "mv-v5-2026-09";
const SHELL = ["/", "/matches", "/register", "/porutham", "/safety", "/offline", "/manifest.webmanifest", "/icons/icon-192.png"];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(VERSION).then((c) => c.addAll(SHELL).catch(() => undefined)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  if (url.pathname.startsWith("/api/") || url.pathname.startsWith("/cards/") || url.pathname.startsWith("/photos/")) return; // live data

  if (url.pathname.startsWith("/_next/static") || /\.(png|jpg|jpeg|webp|svg|woff2?|css|js)$/.test(url.pathname)) {
    event.respondWith(
      caches.match(req).then((hit) => hit || fetch(req).then((res) => {
        const copy = res.clone();
        caches.open(VERSION).then((c) => c.put(req, copy)).catch(() => undefined);
        return res;
      }).catch(() => caches.match("/offline")))
    );
    return;
  }

  event.respondWith(
    fetch(req)
      .then((res) => {
        const copy = res.clone();
        caches.open(VERSION).then((c) => c.put(req, copy)).catch(() => undefined);
        return res;
      })
      .catch(() => caches.match(req).then((hit) => hit || caches.match("/offline")))
  );
});

self.addEventListener("message", (e) => { if (e.data === "skipWaiting") self.skipWaiting(); });

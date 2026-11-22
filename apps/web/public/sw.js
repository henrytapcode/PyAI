/* PyAI Path Offline Service Worker (iOS/iPadOS Safari & static export compatible) */

const SHELL_CACHE = "pyai-shell-v1";
const PYODIDE_CACHE = "pyai-pyodide-v0.29.5";

const PRECACHE_PATHS = [
  "",
  "learn/",
  "review/",
  "exams/",
  "interview/",
  "glossary/",
  "playground/",
  "portfolio/",
  "settings/",
  "manifest.webmanifest",
  "favicon.svg",
  "icons/apple-touch-icon.png",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "pyodide-worker.js",
  "pyrunner/runner.py",
  "pyrunner/tracer.py",
  "pyrunner/llm.py",
];

const STATIC_EXT_RE = /\.(?:js|css|json|svg|png|jpg|jpeg|webp|ico|woff2?|py|webmanifest|html|txt)$/i;

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(SHELL_CACHE).then(async (cache) => {
      const scope = self.registration.scope;
      await Promise.allSettled(
        PRECACHE_PATHS.map(async (relPath) => {
          const url = new URL(relPath, scope).href;
          const res = await fetch(url, { cache: "reload" });
          if (res.ok) {
            await cache.put(url, res);
          }
        })
      );
    })
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter(
              (key) =>
                (key.startsWith("pyai-shell-") && key !== SHELL_CACHE) ||
                (key.startsWith("pyai-pyodide-") && key !== PYODIDE_CACHE)
            )
            .map((key) => caches.delete(key))
        )
      )
      .then(() => self.clients.claim())
  );
});

self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
});

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;

  const url = new URL(request.url);
  if (url.protocol !== "http:" && url.protocol !== "https:") return;

  // 1. Pyodide CDN assets (versioned & immutable) -> Cache-first
  if (url.origin === "https://cdn.jsdelivr.net" && url.pathname.startsWith("/pyodide/")) {
    event.respondWith(cacheFirst(request, PYODIDE_CACHE, true));
    return;
  }

  // Only handle same-origin requests below
  if (url.origin !== self.location.origin) return;

  // 2. Navigation requests -> Network-first with offline cache fallback
  if (request.mode === "navigate") {
    event.respondWith(networkFirstNavigation(request));
    return;
  }

  // 3. Next.js content-hashed static chunks -> Cache-first
  if (url.pathname.includes("/_next/static/")) {
    event.respondWith(cacheFirst(request, SHELL_CACHE, false));
    return;
  }

  // 4. Other same-origin static assets -> Stale-While-Revalidate
  if (STATIC_EXT_RE.test(url.pathname)) {
    event.respondWith(staleWhileRevalidate(request, SHELL_CACHE));
  }
});

async function cacheFirst(request, cacheName, allowOpaque) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  if (cached) return cached;

  const response = await fetch(request);
  if (response.ok || (allowOpaque && response.type === "opaque")) {
    cache.put(request, response.clone()).catch(() => {});
  }
  return response;
}

async function networkFirstNavigation(request) {
  const cache = await caches.open(SHELL_CACHE);
  try {
    const response = await fetch(request);
    if (response.ok) {
      cache.put(request, response.clone()).catch(() => {});
    }
    return response;
  } catch {
    const cachedExact = await cache.match(request, { ignoreSearch: true });
    if (cachedExact) return cachedExact;

    const cachedRoot = await cache.match(self.registration.scope);
    if (cachedRoot) return cachedRoot;

    return new Response("Offline", {
      status: 503,
      statusText: "Service Unavailable",
      headers: { "Content-Type": "text/plain; charset=utf-8" },
    });
  }
}

async function staleWhileRevalidate(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);

  const networkPromise = fetch(request)
    .then((response) => {
      if (response.ok) {
        cache.put(request, response.clone()).catch(() => {});
      }
      return response;
    })
    .catch(() => null);

  if (cached) {
    return cached;
  }

  const fresh = await networkPromise;
  if (fresh) return fresh;

  return new Response("", { status: 504, statusText: "Gateway Timeout" });
}

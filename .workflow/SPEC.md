# SPEC: iOS/iPadOS-Compatible PWA & Offline Mode

## Tier & Summary
- **Tier:** TIER 2 (Standard — scoped to `apps/web`, zero schema/DB/auth/dependency changes; includes independent Argon diff review on completion).
- **Summary:** Make PyAI Path installable as a standalone Home Screen web app on iPhone and iPad (Safari iOS/iPadOS) with proper Dose-themed PNG icons, `manifest.webmanifest` aligned to `NEXT_PUBLIC_BASE_PATH`, notch/Dynamic Island/Home Bar safe-area insets, and a zero-dependency Service Worker (`sw.js`) for offline reading, quizzes, flashcards, mock interviews, and cached Pyodide execution.

## Goal & Non-Goals
- **Goals:**
  1. Generate opaque Dose-branded PNG icons (`apple-touch-icon.png` 180x180, `icon-192.png` 192x192, `icon-512.png` 512x512) matching `<Logo>` in `providers.tsx`.
  2. Serve a static `manifest.webmanifest` via Next.js App Router `apps/web/src/app/manifest.ts` (`export const dynamic = "force-static"`) using `NEXT_PUBLIC_BASE_PATH` for `start_url`, `scope`, and icon paths.
  3. Add iOS/iPadOS standalone metadata and `viewportFit: "cover"` in `apps/web/src/app/layout.tsx`.
  4. Apply `env(safe-area-inset-*)` padding cleanly in `apps/web/src/components/app-shell.tsx` (mobile top bar, bottom nav, desktop/iPad sidebar) without breaking tap targets or Dose design tokens.
  5. Add a zero-dependency Service Worker (`apps/web/public/sw.js`) and client registrar/status component (`apps/web/src/components/pwa-register.tsx`) that caches app shell, static assets, visited lessons, and Pyodide CDN assets, plus shows a minimal bilingual offline indicator and an update-reload banner when a new SW is waiting (essential on iOS standalone mode where there is no browser refresh bar).
- **Non-Goals:**
  - Do NOT install new npm packages (`next-pwa`, `serwist`, `workbox`, etc.).
  - Do NOT modify `apps/web/next.config.ts`, `apps/web/src/lib/progress.ts`, `apps/web/src/lib/storage.ts`, or `curriculum/`.
  - Do NOT add Android/desktop custom install prompt banners (iOS Safari does not fire `beforeinstallprompt`).
  - Do NOT add push notifications or background sync.

## File Whitelist
- `apps/web/public/icons/apple-touch-icon.png` (new)
- `apps/web/public/icons/icon-192.png` (new)
- `apps/web/public/icons/icon-512.png` (new)
- `apps/web/public/sw.js` (new)
- `apps/web/src/app/manifest.ts` (new)
- `apps/web/src/app/layout.tsx` (modify)
- `apps/web/src/components/pwa-register.tsx` (new)
- `apps/web/src/components/providers.tsx` (modify)
- `apps/web/src/components/app-shell.tsx` (modify)
- `apps/web/messages/en.json` (modify)
- `apps/web/messages/vi.json` (modify)

## File Blacklist
- `apps/web/package.json`, `pnpm-lock.yaml`, `apps/web/next.config.ts`
- `apps/web/src/lib/progress.ts`, `apps/web/src/lib/storage.ts`, `apps/web/src/lib/auth.ts`
- `curriculum/**`, `tools/**`, `.github/**`

## Technical Design & Interface Contracts

### 1. PNG Icons (`apps/web/public/icons/`)
- Solid opaque background `#107c55` (Dose `--primary` `oklch(50% 0.13 160)` sRGB equivalent), inner frame `#0b5e40` (`--primary-ink`), crisp geometric white `#fbfdfb` `P` glyph + bottom-right square dot matching `Logo` in `apps/web/src/components/providers.tsx`.
- Exact dimensions:
  - `apple-touch-icon.png`: `180x180` (opaque, no rounded-corner transparency so iOS applies its native squircle mask cleanly).
  - `icon-192.png`: `192x192`
  - `icon-512.png`: `512x512`

### 2. Static Web App Manifest (`apps/web/src/app/manifest.ts`)
```ts
import type { MetadataRoute } from "next";

export const dynamic = "force-static";

const BASE = process.env.NEXT_PUBLIC_BASE_PATH || "";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "PyAI Path · Python for AI Engineers",
    short_name: "PyAI Path",
    description:
      "Bilingual (VI/EN) Python learning path for AI engineers: lessons, in-browser Python, exercises with tests, quizzes, spaced repetition and mock exams.",
    start_url: `${BASE}/`,
    scope: `${BASE}/`,
    display: "standalone",
    orientation: "any",
    background_color: "#faf7ef",
    theme_color: "#107c55",
    icons: [
      { src: `${BASE}/icons/icon-192.png`, sizes: "192x192", type: "image/png", purpose: "any" },
      { src: `${BASE}/icons/icon-512.png`, sizes: "512x512", type: "image/png", purpose: "any" },
      { src: `${BASE}/icons/icon-512.png`, sizes: "512x512", type: "image/png", purpose: "maskable" },
    ],
  };
}
```

### 3. iOS Metadata & Viewport (`apps/web/src/app/layout.tsx`)
- `const BASE = process.env.NEXT_PUBLIC_BASE_PATH || "";`
- `metadata`:
  - `appleWebApp: { capable: true, title: "PyAI Path", statusBarStyle: "default" }` (uses `"default"` so iOS status bar text stays legible in both Dose Light `#faf7ef` and Dose Dark `#040807`).
  - `icons`:
    - `icon`: `[{ url: `${BASE}/favicon.svg`, type: "image/svg+xml" }, { url: `${BASE}/icons/icon-192.png`, sizes: "192x192", type: "image/png" }]`
    - `apple`: `[{ url: `${BASE}/icons/apple-touch-icon.png`, sizes: "180x180", type: "image/png" }]`
- `viewport`:
  - Add `viewportFit: "cover"` alongside existing `themeColor`.

### 4. Safe Area Insets (`apps/web/src/components/app-shell.tsx`)
- Mobile `<header>`: add `pt-[env(safe-area-inset-top)] pl-[max(1rem,env(safe-area-inset-left))] pr-[max(1rem,env(safe-area-inset-right))]` with an inner `flex h-14 w-full items-center gap-2` row (or `min-h-14` + safe-area top padding) so header height never collapses beneath the iPhone Dynamic Island / status bar.
- Mobile bottom `<nav>`: keep `pb-[env(safe-area-inset-bottom)]` and add `pl-[env(safe-area-inset-left)] pr-[env(safe-area-inset-right)]` for iPhone/iPad landscape.
- Desktop/iPad `<aside>`: add `pl-[max(0.75rem,env(safe-area-inset-left))] pt-[max(1rem,env(safe-area-inset-top))] pb-[max(1rem,env(safe-area-inset-bottom))]`.
- Dose compliance: zero raw hex/oklch literals, zero `backdrop-blur`, zero `transition-all`, tap targets `>= 44px` (`.hit`).

### 5. Service Worker (`apps/web/public/sw.js`)
- Constants:
  - `SHELL_CACHE = "pyai-shell-v1"`
  - `PYODIDE_CACHE = "pyai-pyodide-v0.29.5"`
  - `PRECACHE_PATHS`: relative to `self.registration.scope`:
    - `""`, `"learn/"`, `"review/"`, `"exams/"`, `"interview/"`, `"glossary/"`, `"playground/"`, `"portfolio/"`, `"settings/"`, `"manifest.webmanifest"`, `"favicon.svg"`, `"icons/apple-touch-icon.png"`, `"icons/icon-192.png"`, `"icons/icon-512.png"`, `"pyodide-worker.js"`, `"pyrunner/runner.py"`, `"pyrunner/tracer.py"`, `"pyrunner/llm.py"`
- Lifecycle:
  - `install`: open `SHELL_CACHE`, resolve each path via `new URL(p, self.registration.scope).href`, fetch & put with `Promise.allSettled` (never fails whole install if one optional asset misses). Do NOT auto-`skipWaiting()` silently on update so active sessions aren't broken; instead listen for `message` `{ type: "SKIP_WAITING" }` -> `self.skipWaiting()`. (On very first install when no active controller exists, SW activates automatically.)
  - `activate`: delete any cache starting with `"pyai-shell-"` or `"pyai-pyodide-"` that does not match current cache names, then `self.clients.claim()`.
- Fetch routing (only `request.method === "GET"` and `http:`/`https:`):
  1. **Pyodide CDN (`url.origin === "https://cdn.jsdelivr.net"` && `url.pathname.startsWith("/pyodide/")`)**: Cache-first in `PYODIDE_CACHE` (caches `response.ok` or opaque `response.type === "opaque"`).
  2. **Same-origin navigation (`request.mode === "navigate"` && `url.origin === self.location.origin`)**: Network-first -> on success update `SHELL_CACHE` (only if `response.ok`) -> on offline/failure return `caches.match(request, { ignoreSearch: true })` or fallback to `caches.match(self.registration.scope)`.
  3. **Same-origin immutable Next chunks (`url.origin === self.location.origin` && `url.pathname.includes("/_next/static/")`)**: Cache-first in `SHELL_CACHE` -> fetch & cache on miss.
  4. **Other same-origin static assets (JS/CSS/JSON/SVG/PNG/WOFF2/PY/HTML)**: Stale-While-Revalidate in `SHELL_CACHE`.
  5. **Other cross-origin requests (e.g. Supabase/local runner/analytics)**: pass through untouched.

### 6. Client Registration & iOS Standalone Update/Offline UI (`apps/web/src/components/pwa-register.tsx` + `providers.tsx` + i18n)
- `PwaRegister` (`"use client"`), mounted inside `Providers` (inside `NextIntlClientProvider`):
  - Tracks `offline` state via `navigator.onLine` + `window` `"online"` / `"offline"` events (initialized safely in `useEffect` to avoid SSR hydration mismatch).
  - Registers `${BASE}/sw.js` with `{ scope: `${BASE}/` }` when `process.env.NODE_ENV === "production"` and `"serviceWorker" in navigator`.
  - Listens for `reg.waiting` and `updatefound` -> `installing.state === "installed"` (when `navigator.serviceWorker.controller` already exists) to set `updateReady = true`.
  - Clicking Reload posts `{ type: "SKIP_WAITING" }` to `waitingWorker`, and on `navigator.serviceWorker` `"controllerchange"` calls `window.location.reload()` (guarded by a `reloadingRef` boolean so it never loops).
  - UI (rendered only when `offline` or `updateReady`):
    - Fixed bottom-right (above mobile bottom nav via `bottom-[calc(4.5rem+env(safe-area-inset-bottom))] lg:bottom-4 right-4 z-40`), compact Dose card (`border border-border bg-card text-foreground shadow-[var(--shadow-lift)]`) with semantic colors (`bg-warning-soft text-warning-ink` pill for offline, primary button for reload, dismiss button with `.hit`).
- i18n keys under `pwa` in both `en.json` and `vi.json`:
  - `pwa.offlineTitle`, `pwa.offlineBody`, `pwa.updateReady`, `pwa.reload`, `pwa.dismiss`
  - VI prose addresses the reader as `"bạn"`.

## Verification Commands
1. `pnpm.cmd --filter web typecheck`
2. `uv run python -c "import json; en=json.load(open('apps/web/messages/en.json',encoding='utf-8')); vi=json.load(open('apps/web/messages/vi.json',encoding='utf-8')); flat=lambda d,p='': {f'{p}.{k}' if p else k for k,v in d.items() if not isinstance(v,dict)} | set().union(*(flat(v,f'{p}.{k}' if p else k) for k,v in d.items() if isinstance(v,dict))); e,v=flat(en),flat(vi); assert e==v, (e-v, v-e); print('i18n parity OK:', len(e))"`
3. Dose design check (no `#hex`/`oklch`/`backdrop-blur`/`transition-all` in `pwa-register.tsx` & `app-shell.tsx`).
4. `pnpm.cmd --filter web build` (both default `""` and test `NEXT_PUBLIC_BASE_PATH=/PyAI` build output check for `manifest.webmanifest`, `sw.js`, `icons/*.png`, and `<link rel="apple-touch-icon">` in `out/index.html`).
5. Live Chrome UI + Service Worker verification on static `out/` server (`http://127.0.0.1:3099`).
6. Independent Argon (`gemini-4-argon-medium`) review of `git diff`.

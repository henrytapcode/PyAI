# Argon Final Review: Selective UI & Motion Polish

## 1. Scope Lock Verification
- **Status:** PASS
- **Modified Source Files (5/5 whitelisted):**
  - `apps/web/src/app/globals.css`
  - `apps/web/src/components/ui/button.tsx`
  - `apps/web/src/components/ui/dialog.tsx`
  - `apps/web/src/components/ui/tooltip.tsx`
  - `apps/web/src/components/pwa-register.tsx`
- **Workflow Files:** `.workflow/SPEC.md`, `.workflow/TASKS.md`
- **Blacklist Integrity:** Zero edits to `package.json`, `pnpm-lock.yaml`, `apps/web/src/app/tokens.css`, `apps/web/design.md`, `apps/web/messages/{en,vi}.json`, or `apps/web/src/components/command-palette.tsx` (instant keyboard UX preserved).

## 2. Dose Design System & Emil Design Engineering Audit

| Before | After | Why |
| --- | --- | --- |
| `html, body { overflow-x: clip; }` (`globals.css:81-83`) | Added `overscroll-behavior: none;`, `touch-action: manipulation;` on interactive tags, and `@media (pointer: coarse)` 16px input font-size (`globals.css:84-98`) | Prevents rubber-band/pull-to-refresh scroll hijacking, removes 300ms iOS tap delay, and stops iOS Safari auto-zoom on inputs without inflating desktop controls |
| `@media (hover: hover)` on `.press:hover` and unfiltered `.row-cursor:hover` (`globals.css:164,186`) | Gated `.press:hover`, `.row-cursor:hover`, and `.row-cursor:hover *` behind `@media (hover: hover) and (pointer: fine)` while keeping `:focus-visible`, `[aria-current="page"]`, and `[data-live="true"]` global (`globals.css:164-209`) | Eliminates sticky hover states after tap on iOS/iPadOS touch screens while preserving keyboard focus and active nav highlighting |
| `ghost` and `soft` buttons lacked `:active` press feedback (`button.tsx:14-17`) | Added `transition-[transform,background-color(,color)] duration-[120ms] ease-[var(--ease-out)] active:scale-[0.98] motion-reduce:transition-none motion-reduce:active:scale-100` (`button.tsx:14-17`) | Gives non-`.press` buttons responsive 120ms tactile feedback using `--ease-out` without `transition-all` |
| `DialogContent` lacked exit animation, explicit duration, `motion-reduce`, and `.hit` on Close (`dialog.tsx:17-28`) | Added `duration-150 motion-reduce:animate-none` on Overlay/Content, `data-[state=closed]:animate-out fade-out-0 zoom-out-95` on Content, and `.hit` + 120ms `active:scale-[0.96]` on Close (`dialog.tsx:17-28`) | Symmetric 150ms centered modal enter/exit, full reduced-motion compliance, and >= 44px touch target on the 36px (`size-9`) close button |
| `TooltipProvider = TooltipPrimitive.Provider` and non-origin-aware `TooltipPrimitive.Content` (`tooltip.tsx:6,36`) | Wrapped `TooltipProvider` with `delayDuration = 300`, `skipDelayDuration = 200` (`tooltip.tsx:6-18`) and added `origin-[var(--radix-tooltip-content-transform-origin)] duration-150 data-[state=closed]:animate-out ... motion-reduce:animate-none` (`tooltip.tsx:36`) | Tooltips scale from their trigger origin in 150ms and open without delay when moving across adjacent triggers |
| Fixed `max-w-sm` toast container and unwrapped flex text (`pwa-register.tsx:87-122`) | Added `max-w-[calc(100vw-2rem)] sm:max-w-sm`, `animate-rise`, `min-w-0 break-words` on text, and `shrink-0` + 120ms `active:scale-[0.97]` on action buttons (`pwa-register.tsx:87-122`) | Prevents horizontal overflow on 320px/375px viewports and gives PWA update/offline cards a clean 160ms entrance |

## 3. Correctness & Edge-Case Checks
- **Dose Guardrails:** 0 occurrences of `transition-all` or `backdrop-blur`; 0 raw `#hex`, `rgb(...)`, or `oklch(...)` literals introduced; all durations within 120–160ms (Dose 120–200ms budget); all animations/transitions disabled under `prefers-reduced-motion: reduce`.
- **Tailwind v4 Compilation:** Verified in `apps/web/out/_next/static/css/ccf3108d269780ba.css` that `.max-w-\[calc\(100vw-2rem\)\]`, `.origin-\[var\(--radix-tooltip-content-transform-origin\)\]`, `.duration-\[120ms\]`, and `.ease-\[var\(--ease-out\)\]` compile to valid CSS rules and resolve `--ease-out` to `cubic-bezier(0.16, 1, 0.3, 1)` from unlayered `:root` in `tokens.css:57`.
- **CSS Layer Cascade:** `@layer base` rules (`globals.css:77-121`) sit below `@layer components` (`globals.css:125-228`) and `@layer utilities`, ensuring utility classes on desktop inputs and buttons override base defaults cleanly.
- **`TooltipProvider` Compatibility:** `providers.tsx:60` (`<TooltipProvider delayDuration={300}>`) passes typecheck and inherits `skipDelayDuration={200}` while allowing per-instance prop overrides.

VERDICT: APPROVE

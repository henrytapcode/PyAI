# SPEC: Selective UI & Motion Polish (Mobile-Native, Emil Design Eng, Dose-Aligned)

- **Tier:** TIER 2 (Standard — 5 files inside `apps/web/src`)
- **Design System Guardrail:** Strictly follow `apps/web/design.md` (Dose v2.1.0): `transform`/`opacity` only, 120–200ms, no `transition-all`, no `backdrop-blur`, no raw color literals, tap targets >= 44px (`.hit`), honor `prefers-reduced-motion`.
- **Rejected Candidates (per `find-animation-opportunities` & `emil-design-eng`):**
  - `command-palette.tsx`: Keyboard-initiated (`Cmd/Ctrl+K`, 100+/day) — MUST stay instant, zero open/close animation.
  - `apps/web` general hover/list navigation: Do NOT stagger high-frequency nav or add Framer Motion / Sonner.

## File Whitelist (ONLY these 5 files may be edited)
1. `apps/web/src/app/globals.css`
2. `apps/web/src/components/ui/button.tsx`
3. `apps/web/src/components/ui/dialog.tsx`
4. `apps/web/src/components/ui/tooltip.tsx`
5. `apps/web/src/components/pwa-register.tsx`

## File Blacklist
- `apps/web/package.json`, `pnpm-lock.yaml` (dependency freeze)
- `apps/web/src/app/tokens.css`, `apps/web/design.md` (Dose palette & rules stay intact)
- `apps/web/messages/{en,vi}.json` (no copy changes needed)
- `apps/web/src/components/command-palette.tsx` (instant keyboard UX preserved)

## Changes by File
1. **`apps/web/src/app/globals.css` (`mobile-native` + `animation-performance`):**
   - Set `overscroll-behavior: none;` on `html, body` to prevent pull-to-refresh / rubber-banding hijacking app scroll.
   - Set `touch-action: manipulation;` on `button, a, [role="button"], summary` inside `@layer base` to eliminate 300ms tap delay on iOS Safari.
   - Add `@media (pointer: coarse) { input, textarea, select { font-size: 16px; } }` inside `@layer base` so iOS Safari never auto-zooms on `<16px` inputs while keeping desktop sizing compact.
   - Tighten `.press:hover` media query from `@media (hover: hover)` to `@media (hover: hover) and (pointer: fine)`.
   - Split `.row-cursor:hover` and `.row-cursor:hover *` into `@media (hover: hover) and (pointer: fine)` while keeping `:focus-visible`, `[aria-current="page"]`, and `[data-live="true"]` active on all pointers (prevents sticky hover on iOS/iPadOS).
2. **`apps/web/src/components/ui/button.tsx` (`mobile-native` + `emil-design-eng`):**
   - Add crisp `:active` press feedback on `ghost` (`transition-[transform,background-color,color] duration-[120ms] ease-[var(--ease-out)] active:scale-[0.98] motion-reduce:transition-none motion-reduce:active:scale-100`) and `soft` (`transition-[transform,background-color] duration-[120ms] ease-[var(--ease-out)] active:scale-[0.98] motion-reduce:transition-none motion-reduce:active:scale-100`) without overriding `.row-cursor` color transitions or using `transition-all`.
3. **`apps/web/src/components/ui/dialog.tsx` (`emil-design-eng` + `mobile-native`):**
   - Add `duration-150 motion-reduce:animate-none` on `DialogPrimitive.Overlay`.
   - Add `duration-150 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95 motion-reduce:animate-none` on `DialogPrimitive.Content` (keep centered; modals do not shift origin).
   - Add `.hit` and `transition-[transform,background-color,color] duration-[120ms] active:scale-[0.96] motion-reduce:transition-none motion-reduce:active:scale-100` on `DialogPrimitive.Close` so the 36px close icon meets >= 44px touch target on iOS/iPadOS.
4. **`apps/web/src/components/ui/tooltip.tsx` (`emil-design-eng`):**
   - Replace `export const TooltipProvider = TooltipPrimitive.Provider` with a compatible wrapper component defaulting `delayDuration={300}` and `skipDelayDuration={200}` for instant sequential toolbar tooltips.
   - Add `origin-[var(--radix-tooltip-content-transform-origin)] duration-150 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95 motion-reduce:animate-none` on `TooltipPrimitive.Content`.
5. **`apps/web/src/components/pwa-register.tsx` (`find-animation-opportunities` + `break-ui`):**
   - Update toast container width guard to `max-w-[calc(100vw-2rem)] sm:max-w-sm` so it never overflows on 320px/375px screens.
   - Add `animate-rise` entrance to both `showUpdate` and `showOffline` cards (auto-disabled under `prefers-reduced-motion: reduce` in `globals.css`).
   - Add `min-w-0 break-words` on flexible text containers (`flex-1 min-w-0`), `shrink-0` on action buttons, and crisp `:active` scale feedback (`active:scale-[0.97] transition-[transform,background-color] duration-[120ms] motion-reduce:transition-none motion-reduce:active:scale-100`).

## Verification Commands
1. `pnpm.cmd --filter web typecheck`
2. Dose check: `Select-String -Path apps/web/src/components/ui/*.tsx, apps/web/src/components/pwa-register.tsx, apps/web/src/app/globals.css -Pattern "transition-all|backdrop-blur"` (expect 0 matches)
3. `pnpm.cmd --filter web build` (static export check)
4. Browser UI verification by Hydrogen (NO `flash` model — use Chrome DevTools MCP or `browser` subagent with `Model: "inherit"` on built static output: desktop 1280x800 + mobile 375x812, 0 console errors, 0 404 assets, 0 horizontal overflow, verify dialog/tooltip/mobile styles).
5. Argon (`gemini-4-argon-high`) diff review (`APPROVE`)

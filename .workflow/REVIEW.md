# PHASE 5 INDEPENDENT CODE REVIEW: Global Search / Command Palette (`Ctrl+K` / `⌘K`)

**VERDICT: APPROVE**

## 1. Scope & Invariant Audit
- **Whitelist / Blacklist Compliance:** **PASS**. `git status --short` confirms only the 11 whitelisted source files (`tools/build_content.py`, `tools/test_build_content.py`, `apps/web/src/lib/types.ts`, `apps/web/src/lib/search.ts`, `apps/web/src/components/command-palette.tsx`, `apps/web/src/components/app-shell.tsx`, `apps/web/src/components/lesson/lesson-view.tsx`, `apps/web/src/app/(main)/glossary/page.tsx`, `apps/web/src/app/(main)/interview/page.tsx`, `apps/web/messages/en.json`, `apps/web/messages/vi.json`) were created or modified alongside `.workflow/*` state files.
- **Dependency Freeze & Anti-Cheating:** **PASS**. Zero package/lockfile modifications (`package.json`, `pnpm-lock.yaml`, `pyproject.toml`, `uv.lock` untouched). No weakened tests, `@ts-ignore`, `any`, `# noqa`, or `eslint-disable` directives introduced.

## 2. Critic Blocking Risks Verification (All 4 Resolved)
1. **Same-Route Navigation (`pyai:deeplink`):** **RESOLVED**.
   - `apps/web/src/components/command-palette.tsx:146-153` dispatches `window.dispatchEvent(new CustomEvent(DEEPLINK_EVENT, { detail: { href } }))` right after `router.push(href)`.
   - `apps/web/src/app/(main)/glossary/page.tsx:26-54`, `apps/web/src/app/(main)/interview/page.tsx:30-60`, and `apps/web/src/components/lesson/lesson-view.tsx:281-315` all subscribe to initial mount, `popstate`, and `"pyai:deeplink"` with route matching and clean listener teardown.
2. **Active Filter Masking on Deep-Links:** **RESOLVED**.
   - `apps/web/src/app/(main)/glossary/page.tsx:29-32` resets `setTag(null)` before `setQuery(q)`.
   - `apps/web/src/app/(main)/interview/page.tsx:33-38` resets `setTopic(null)` before expanding `setOpen` and scrolling `accordion-trigger-${q}` into view via `requestAnimationFrame`.
   - `apps/web/src/components/lesson/lesson-view.tsx:286-293` resets `setMobilePane("content")` when switching to an exercise or tab via deep-link.
3. **Radix `DialogContent` Close Button Collision:** **RESOLVED**.
   - `apps/web/src/components/command-palette.tsx:183-208` renders no duplicate close button and applies `pr-12` on the search header row so the clear (`X`) button never overlaps `DialogContent`'s built-in close button at `right-3.5 top-3.5`.
4. **Typed Dynamic Import of `@/generated/search.json`:** **RESOLVED**.
   - `apps/web/src/lib/search.ts:44-60` safely types the dynamic import (`default?.items` and top-level `items`) and resets `cachedSearchIndex = null` on failure.

## 3. Dose Design System & Accessibility Audit (`apps/web/design.md`)
- **Tokens & Surfaces:** **PASS**. Zero raw color literals (`#hex`, `oklch`, `rgb`), zero `backdrop-blur`, zero `transition-all`. `DialogContent` (`apps/web/src/components/command-palette.tsx:178`) omits outer `border`, preserving Dose floating surface elevation (`bg-popover` + `shadow-[var(--shadow-lift)]`).
- **Typography:** **PASS**. Uses only `font-medium` (500) and `font-bold` (700) — zero `font-semibold` or `font-black`. Result counter (`command-palette.tsx:366`) uses `font-mono tabular-nums`.
- **Tap Targets & A11y:** **PASS**. `.hit` applied on the clear button (`command-palette.tsx:203`), filter pills (`command-palette.tsx:225`), and mobile header trigger (`app-shell.tsx:142`). Visually hidden `DialogTitle` and `DialogDescription` (`sr-only`), `aria-pressed` on filter buttons, `role="listbox"` / `role="option"` with `aria-selected`, `aria-label` on icon-only controls, and `aria-hidden="true"` on decorative icons.

## 4. Bilingual i18n Parity & Logic Audit
- **EN/VI Parity:** **PASS**. `apps/web/messages/en.json` and `apps/web/messages/vi.json` have identical keys under `nav.search` and `search.*` (including `search.kinds.*`), with natural Vietnamese terminology and zero forbidden pronouns (`"ta"` / `"chúng ta"`).
- **Build & Search Logic:** **PASS**. `tools/build_content.py` indexes only ready lessons (`built == True`) and properly URL-encodes `ex`, `term`, and interview `id` query parameters with `urllib.parse.quote(..., safe='')`. `tools/test_build_content.py` covers all 6 `SearchKind` variants, truncation, URL encoding, and unbuilt lesson exclusion.

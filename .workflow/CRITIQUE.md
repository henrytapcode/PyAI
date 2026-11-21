# CRITIQUE: Global Search / Command Palette (`Ctrl+K` / `⌘K`)

**VERDICT: REVISE**

The overall architecture, static-export strategy (`output: "export"`, `trailingSlash: true`, `basePath`-safe dynamic JSON import), Dose Design System alignment, and parallel task split (`T1`–`T4` have zero file overlap) are well-structured. However, there are **4 concrete Blocking Risks** (primarily around same-route navigation, active-filter masking on deep-links, Dialog close-button collision, and parallel TypeScript type-checking before `search.json` exists) that must be tightened in `SPEC.md` and `TASKS.md` before coding starts.

---

## Blocking Risks (Must Fix in SPEC Before Coding)

1. **Same-Route Navigation Failure (`window.location.search` effects only run on mount or `meta.id` change)**
   - **Risk:** In Next.js App Router (`next@16.4.5`), calling `router.push("/glossary/?q=rag")` when already on `/glossary/?q=token`, or `router.push("/lesson/p1-01/?tab=exercises&ex=ex02")` when already on `/lesson/p1-01/?tab=theory`, or `router.push("/interview/?q=q2")` when already on `/interview/`, **does not remount** the page/component and **does not change `pathname` or `meta.id`**. Moreover, bypassing `useSearchParams()` means Next.js will not trigger a re-render of those components on query-only route pushes unless explicitly notified.
   - **Required SPEC Fix:**
     - Define a lightweight custom DOM event (e.g. `window.dispatchEvent(new CustomEvent("pyai:deeplink"))` or `popstate`) fired by `<CommandPalette />` right after `router.push(item.href)` (e.g., via `setTimeout` / `requestAnimationFrame` or after navigation), **AND** listen to both `popstate` and `"pyai:deeplink"` inside the `useEffect` hooks in `lesson-view.tsx`, `glossary/page.tsx`, and `interview/page.tsx` (in addition to initial mount / `meta.id` change).
     - Alternatively, have `<CommandPalette />` dispatch `new CustomEvent("pyai:navigate", { detail: { href: item.href } })` alongside `router.push(item.href)` so same-route components immediately parse the query string from the event or `window.location.search`.

2. **Active Filter Masking on `/glossary/` and `/interview/` Deep-Links**
   - **Risk:**
     - In `apps/web/src/app/(main)/interview/page.tsx`, if the user has selected a topic filter (`topic !== null`) and then uses `Ctrl+K` to jump to an interview question from a *different* topic (`/interview/?q=<id>`), `list` filters out that question (`!topic || q.topic === topic`). `document.getElementById("accordion-trigger-" + q)` will be `null` and the question will be invisible.
     - Similarly, in `apps/web/src/app/(main)/glossary/page.tsx`, if a `tag` filter is active (`tag !== null`) and the user deep-links to `/glossary/?q=<term>` outside that tag, the term is hidden.
   - **Required SPEC Fix:**
     - In `interview/page.tsx`, when handling deep-link `?q=<id>`, also call `setTopic(null)` so the target question is guaranteed to be rendered in `list` before `requestAnimationFrame` scrolls to `accordion-trigger-${q}`.
     - In `glossary/page.tsx`, when handling deep-link `?q=<term>`, also call `setTag(null)`.

3. **Radix `DialogContent` Built-in Close Button Collides with Custom Search Header**
   - **Risk:** `apps/web/src/components/ui/dialog.tsx` (`DialogContent`) unconditionally renders an absolute-positioned `<DialogPrimitive.Close className="absolute right-3.5 top-3.5 ...">` inside `DialogContent`. Meanwhile, `SPEC.md` §3 states: *"Search input autofocused on open, with `Search` icon, clear button when query non-empty (`aria-label={t("clear")}`), and Escape/close button."* If `<CommandPalette />` renders its own close button or puts the clear button near the right edge of the top input bar without accounting for `DialogContent`'s built-in close button at `right-3.5 top-3.5`, the buttons will overlap visually and fail Dose UI/a11y checks.
   - **Required SPEC Fix:** Explicitly specify in `SPEC.md` §3 that `<CommandPalette />` must **not** render a duplicate close button—instead, reserve right padding (`pr-12`) on the search input row so the clear button sits cleanly to the left of `DialogContent`'s built-in top-right close (`X`) button.

4. **Dynamic Import of `@/generated/search.json` vs. TypeScript & Parallel Worker Execution**
   - **Risk:**
     - In TypeScript with `resolveJsonModule: true`, `import("@/generated/search.json")` resolves to `{ default: { items: ... }, items: ... }`, and fails `tsc --noEmit` if `apps/web/src/generated/search.json` has not been generated yet by `T1`.
     - If `T2` runs in parallel with `T1`, or if `search.json` is typed directly from the JSON literal, `T2` could hit a missing-module error or inferred literal type mismatch (`string` vs `SearchKind`).
   - **Required SPEC Fix:**
     - In `SPEC.md` §2, specify the exact `loadSearchIndex()` extraction pattern:
       ```ts
       const mod = (await import("@/generated/search.json")) as {
         default?: { items?: SearchItem[] };
         items?: SearchItem[];
       };
       return mod.items ?? mod.default?.items ?? [];
       ```
     - In `TASKS.md`, note that `T1` (`tools/build_content.py`) must either complete before `pnpm.cmd --filter web typecheck` is run (already in `T5`, since `typecheck` runs `pnpm run content` first), and `T2`/`T4` workers must not run `tsc` before `search.json` exists.

---

## Minor Notes (Non-Blocking Polish)

- **Dose Elevation Rule (`apps/web/design.md` §4):** Floating surfaces (`DialogContent`, `bg-popover`) use `shadow-[var(--shadow-lift)]` and **must not** have an outer `border border-border`. Internal hairline dividers (`border-b border-border` between search input, filter bar, results list, and footer) are fine, just ensure `DialogContent` itself has no outer border class added.
- **Mobile Exercise Deep-Link Pane (`lesson-view.tsx`):** When deep-linking to `/lesson/<id>/?tab=exercises&ex=<exId>`, also reset `setMobilePane("content")` so mobile users see the exercise prompt/picker first (or document the desired pane).
- **`AppShell` Translation Namespace:** `AppShell` currently uses `const t = useTranslations("nav")`. `SPEC.md` §3 mentions `t("search")` and §5 adds `"nav.search"`—this is consistent; just ensure `AppShell` uses `t("search")` from `"nav"`.

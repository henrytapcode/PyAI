# TASKS: Selective UI & Motion Polish

- [x] **T1:** Update `apps/web/src/app/globals.css` (`overscroll-behavior: none`, `touch-action: manipulation`, `@media (pointer: coarse)` 16px input font-size, `@media (hover: hover) and (pointer: fine)` on `.row-cursor:hover`).
- [x] **T2:** Update `apps/web/src/components/ui/button.tsx` (`active:scale-[0.98]` + `motion-reduce` on `ghost` and `soft`).
- [x] **T3:** Update `apps/web/src/components/ui/dialog.tsx` (symmetric 150ms open/close fade+zoom, `motion-reduce:animate-none`, `.hit` on close button).
- [x] **T4:** Update `apps/web/src/components/ui/tooltip.tsx` (`origin-[var(--radix-tooltip-content-transform-origin)]`, 150ms open/close, `motion-reduce:animate-none`, `TooltipProvider` `delayDuration`/`skipDelayDuration` defaults).
- [x] **T5:** Update `apps/web/src/components/pwa-register.tsx` (`animate-rise`, `min-w-0` wrapping safety).
- [x] **T6 (QA + Browser + Argon):** Run `typecheck`, Dose guard check, `build`, browser visual/console/375px check, and Argon `git diff` review.

"use client";

import {
  BookA,
  BookOpen,
  Briefcase,
  ClipboardCheck,
  Code2,
  Map,
  MessagesSquare,
  Repeat,
  Search,
  SquareTerminal,
  X,
} from "lucide-react";
import { useRouter } from "next/navigation";
import { useTranslations } from "next-intl";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogTitle,
} from "@/components/ui/dialog";
import { useLoc } from "@/lib/i18n";
import {
  DEEPLINK_EVENT,
  loadSearchIndex,
  SEARCH_KINDS,
  type SearchFilter,
  searchItems,
} from "@/lib/search";
import type { SearchItem, SearchKind } from "@/lib/types";
import { cn } from "@/lib/utils";

const QUICK_JUMPS = [
  { href: "/learn/", key: "learn", icon: Map },
  { href: "/review/", key: "review", icon: Repeat },
  { href: "/exams/", key: "exams", icon: ClipboardCheck },
  { href: "/playground/", key: "playground", icon: SquareTerminal },
  { href: "/glossary/", key: "glossary", icon: BookA },
  { href: "/interview/", key: "interview", icon: MessagesSquare },
] as const;

const KIND_ICON: Record<SearchKind, typeof BookOpen> = {
  lesson: BookOpen,
  exercise: Code2,
  glossary: BookA,
  interview: MessagesSquare,
  exam: ClipboardCheck,
  portfolio: Briefcase,
};

const FILTERS: readonly SearchFilter[] = ["all", ...SEARCH_KINDS];

export function CommandPalette({
  open,
  onOpenChange,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}) {
  const ts = useTranslations("search");
  const tn = useTranslations("nav");
  const loc = useLoc();
  const router = useRouter();

  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState<SearchFilter>("all");
  const [activeIndex, setActiveIndex] = useState(0);
  const [items, setItems] = useState<SearchItem[] | null>(null);
  const [loading, setLoading] = useState(false);

  const inputRef = useRef<HTMLInputElement>(null);
  const itemRefs = useRef<(HTMLButtonElement | null)[]>([]);

  // Global Ctrl+K / Cmd+K shortcut
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if (e.altKey || e.isComposing) return;
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        onOpenChange(!open);
      }
    }
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [open, onOpenChange]);

  // Lazy-load search index on first open; reset transient state on close
  useEffect(() => {
    if (!open) {
      setQuery("");
      setFilter("all");
      setActiveIndex(0);
      return;
    }

    requestAnimationFrame(() => {
      inputRef.current?.focus();
    });

    if (items !== null) return;
    let cancelled = false;
    setLoading(true);
    loadSearchIndex()
      .then((data) => {
        if (!cancelled) {
          setItems(data);
          setLoading(false);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setLoading(false);
        }
      });
    return () => {
      cancelled = true;
    };
  }, [open, items]);

  // Reset active row when query or filter changes
  useEffect(() => {
    setActiveIndex(0);
  }, [query, filter]);

  const trimmedQuery = query.trim();
  const isEmptyQuery = trimmedQuery === "";

  const results = useMemo(() => {
    if (isEmptyQuery || !items) return [];
    return searchItems(items, query, filter, 30);
  }, [isEmptyQuery, items, query, filter]);

  const visibleCount = isEmptyQuery ? QUICK_JUMPS.length : results.length;

  // Keep active row visible when navigating with arrow keys
  useEffect(() => {
    if (!open || visibleCount === 0) return;
    const el = itemRefs.current[activeIndex];
    el?.scrollIntoView({ block: "nearest" });
  }, [activeIndex, open, visibleCount]);

  const navigateTo = useCallback(
    (href: string) => {
      router.push(href);
      window.dispatchEvent(new CustomEvent(DEEPLINK_EVENT, { detail: { href } }));
      onOpenChange(false);
    },
    [router, onOpenChange],
  );

  function handleInputKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (visibleCount === 0) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActiveIndex((prev) => (prev + 1) % visibleCount);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActiveIndex((prev) => (prev - 1 + visibleCount) % visibleCount);
    } else if (e.key === "Enter") {
      e.preventDefault();
      if (isEmptyQuery) {
        const target = QUICK_JUMPS[activeIndex];
        if (target) navigateTo(target.href);
      } else {
        const target = results[activeIndex];
        if (target) navigateTo(target.href);
      }
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="p-0 gap-0 max-w-2xl overflow-hidden">
        <DialogTitle className="sr-only">{ts("title")}</DialogTitle>
        <DialogDescription className="sr-only">{ts("description")}</DialogDescription>

        {/* Search input bar (pr-14 reserves space for DialogContent's built-in close button) */}
        <div className="flex items-center gap-2.5 border-b border-border px-4 py-3.5 pr-14">
          <Search className="size-4 shrink-0 text-muted-foreground" aria-hidden="true" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleInputKeyDown}
            placeholder={ts("placeholder")}
            aria-label={ts("placeholder")}
            className="min-w-0 flex-1 bg-transparent text-sm text-foreground placeholder:text-muted-foreground outline-none"
          />
          {query.length > 0 && (
            <button
              type="button"
              onClick={() => {
                setQuery("");
                inputRef.current?.focus();
              }}
              aria-label={ts("clear")}
              className="hit inline-flex size-7 shrink-0 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-accent hover:text-primary focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
            >
              <X className="size-4" aria-hidden="true" />
            </button>
          )}
        </div>

        {/* Category filter pills */}
        <div
          role="group"
          aria-label={ts("title")}
          className="flex items-center gap-1.5 overflow-x-auto border-b border-border px-4 py-2"
        >
          {FILTERS.map((kind) => {
            const selected = filter === kind;
            return (
              <button
                key={kind}
                type="button"
                aria-pressed={selected}
                onClick={() => setFilter(kind)}
                className={cn(
                  "hit shrink-0 rounded-full px-2.5 py-1 text-xs font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring",
                  selected
                    ? "bg-primary font-bold text-primary-foreground"
                    : "bg-muted text-muted-foreground hover:bg-accent hover:text-foreground",
                )}
              >
                {ts(`kinds.${kind}`)}
              </button>
            );
          })}
        </div>

        {/* Results or Quick Jump list */}
        <div className="max-h-[60vh] overflow-y-auto p-2" role="listbox" aria-label={ts("title")}>
          {isEmptyQuery ? (
            <div>
              <div className="px-2 py-1.5 text-xs font-medium text-muted-foreground">
                {ts("quickJump")}
              </div>
              <div className="flex flex-col gap-0.5">
                {QUICK_JUMPS.map(({ href, key, icon: Icon }, idx) => {
                  const active = idx === activeIndex;
                  return (
                    <button
                      key={href}
                      ref={(el) => {
                        itemRefs.current[idx] = el;
                      }}
                      type="button"
                      role="option"
                      aria-selected={active}
                      onMouseEnter={() => setActiveIndex(idx)}
                      onClick={() => navigateTo(href)}
                      className={cn(
                        "flex w-full items-center gap-3 rounded-md px-3 py-2.5 text-left text-sm transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring",
                        active
                          ? "bg-accent font-medium text-primary"
                          : "text-foreground hover:bg-accent/60",
                      )}
                    >
                      <Icon className="size-4 shrink-0 text-muted-foreground" aria-hidden="true" />
                      <span className="flex-1 truncate">{tn(key)}</span>
                      <span className="font-mono text-xs text-muted-foreground">{href}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          ) : loading ? (
            <div className="px-4 py-8 text-center text-sm text-muted-foreground">
              {ts("loading")}
            </div>
          ) : results.length === 0 ? (
            <div className="px-4 py-8 text-center text-sm text-muted-foreground">
              {ts("empty")}
            </div>
          ) : (
            <div className="flex flex-col gap-0.5">
              {results.map((item, idx) => {
                const active = idx === activeIndex;
                const Icon = KIND_ICON[item.kind];
                const title = loc.t(item.title);
                const subtitle = item.subtitle ? loc.t(item.subtitle) : undefined;
                return (
                  <button
                    key={item.id}
                    ref={(el) => {
                      itemRefs.current[idx] = el;
                    }}
                    type="button"
                    role="option"
                    aria-selected={active}
                    onMouseEnter={() => setActiveIndex(idx)}
                    onClick={() => navigateTo(item.href)}
                    className={cn(
                      "flex w-full items-start gap-3 rounded-md px-3 py-2.5 text-left transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring",
                      active ? "bg-accent" : "hover:bg-accent/60",
                    )}
                  >
                    <Icon
                      className={cn(
                        "mt-0.5 size-4 shrink-0",
                        active ? "text-primary" : "text-muted-foreground",
                      )}
                      aria-hidden="true"
                    />
                    <div className="min-w-0 flex-1">
                      <div
                        className={cn(
                          "truncate text-sm",
                          active ? "font-bold text-primary" : "font-medium text-foreground",
                        )}
                      >
                        {title}
                      </div>
                      {subtitle && (
                        <div className="mt-0.5 truncate text-xs text-muted-foreground">
                          {subtitle}
                        </div>
                      )}
                    </div>
                    <div className="flex shrink-0 items-center gap-1.5">
                      {item.phase && (
                        <Badge variant="outline" className="font-mono text-[11px]">
                          {item.phase}
                        </Badge>
                      )}
                      <Badge variant={active ? "default" : "muted"}>
                        {ts(`kinds.${item.kind}`)}
                      </Badge>
                    </div>
                  </button>
                );
              })}
            </div>
          )}
        </div>

        {/* Footer hints */}
        <div className="flex flex-wrap items-center justify-between gap-2 border-t border-border bg-muted px-4 py-2 text-xs text-muted-foreground">
          <div className="flex items-center gap-3">
            <span className="inline-flex items-center gap-1">
              <kbd className="rounded-sm border border-border bg-card px-1.5 py-0.5 font-mono text-[11px]">
                ↑↓
              </kbd>
              <span>{ts("hintNavigate")}</span>
            </span>
            <span className="inline-flex items-center gap-1">
              <kbd className="rounded-sm border border-border bg-card px-1.5 py-0.5 font-mono text-[11px]">
                Enter
              </kbd>
              <span>{ts("hintSelect")}</span>
            </span>
            <span className="inline-flex items-center gap-1">
              <kbd className="rounded-sm border border-border bg-card px-1.5 py-0.5 font-mono text-[11px]">
                Esc
              </kbd>
              <span>{ts("hintClose")}</span>
            </span>
          </div>
          {!isEmptyQuery && !loading && (
            <span className="font-mono tabular-nums">
              {ts("resultsCount", { count: results.length })}
            </span>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}

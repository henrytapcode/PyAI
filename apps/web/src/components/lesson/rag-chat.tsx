"use client";

import {
  AlertCircle,
  ArrowUpRight,
  Bot,
  ExternalLink,
  Lightbulb,
  Maximize2,
  Minimize2,
  RefreshCw,
  Send,
  Sparkles,
  Trash2,
  X,
} from "lucide-react";
import Link from "next/link";
import { useTranslations } from "next-intl";
import { useCallback, useEffect, useRef, useState } from "react";
import ReactMarkdown, { type Components } from "react-markdown";
import rehypeHighlight from "rehype-highlight";
import remarkGfm from "remark-gfm";
import { CodeBlock } from "@/components/markdown";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  askRag,
  checkHealth,
  isRagConfigured,
  nextHint,
  RagApiError,
  type RagResponse,
  type SourceItem,
} from "@/lib/rag";
import { cn } from "@/lib/utils";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: number;
  // Assistant response fields
  refused?: boolean;
  sources?: SourceItem[];
  cited?: number[];
  tier?: number | null;
  exercise?: string | null;
  error?: string | null;
  status?: number;
}

type ProviderChoice = "auto" | "claude" | "gemini";

type HastNode = {
  type: string;
  tagName?: string;
  value?: string;
  properties?: Record<string, unknown>;
  children?: HastNode[];
};

function textOf(node: HastNode | undefined): string {
  if (!node) return "";
  if (node.type === "text") return node.value ?? "";
  return (node.children ?? []).map(textOf).join("");
}

/**
 * Transforms citations like [1], [2] outside code blocks into markdown links for chips.
 */
function transformCitations(text: string): string {
  const parts = text.split(/(```[\s\S]*?```|`[^`\n]+`)/g);
  return parts
    .map((part, idx) => {
      if (idx % 2 === 1) return part;
      return part.replace(/\[(\d+)\]/g, "[$1](#source-$1)");
    })
    .join("");
}

export function RagChat({
  lessonId,
  exerciseId,
}: {
  lessonId: string;
  exerciseId: string | null;
}) {
  const t = useTranslations("assistant");
  const tc = useTranslations("common");

  // Invariant: Completely hide chat if NEXT_PUBLIC_RAG_URL is not configured
  if (!isRagConfigured) return null;

  return <RagChatInner lessonId={lessonId} exerciseId={exerciseId} t={t} tc={tc} />;
}

function RagChatInner({
  lessonId,
  exerciseId,
  t,
  tc,
}: {
  lessonId: string;
  exerciseId: string | null;
  t: ReturnType<typeof useTranslations>;
  tc: ReturnType<typeof useTranslations>;
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [provider, setProvider] = useState<ProviderChoice>("auto");
  const [isLoading, setIsLoading] = useState(false);
  const [isOnline, setIsOnline] = useState<boolean | null>(null);
  const [retryCountdown, setRetryCountdown] = useState<number>(0);
  const [activeSourceId, setActiveSourceId] = useState<string | null>(null);

  const abortControllerRef = useRef<AbortController | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const toggleButtonRef = useRef<HTMLButtonElement>(null);

  // Check health lazily when opening for the first time
  const checkedHealthRef = useRef(false);
  const verifyHealth = useCallback(async () => {
    try {
      await checkHealth();
      setIsOnline(true);
    } catch {
      setIsOnline(false);
    }
  }, []);

  useEffect(() => {
    if (isOpen && !checkedHealthRef.current) {
      checkedHealthRef.current = true;
      void verifyHealth();
    }
  }, [isOpen, verifyHealth]);

  // Focus textarea when opened
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => textareaRef.current?.focus(), 150);
    } else {
      toggleButtonRef.current?.focus();
    }
  }, [isOpen]);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isLoading, isOpen]);

  // Rate-limit countdown timer
  useEffect(() => {
    if (retryCountdown <= 0) return;
    const interval = setInterval(() => {
      setRetryCountdown((prev) => Math.max(0, prev - 1));
    }, 1000);
    return () => clearInterval(interval);
  }, [retryCountdown]);

  // Keyboard navigation: Escape closes chat
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen) {
        setIsOpen(false);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen]);

  // Abort pending request on unmount
  useEffect(() => {
    return () => {
      abortControllerRef.current?.abort();
    };
  }, []);

  const handleCancel = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    setIsLoading(false);
  };

  const getLocalizedErrorMessage = (status: number, retryAfter?: number | null) => {
    if (status === 401) return t("err401");
    if (status === 422) return t("err422");
    if (status === 429) return t("err429", { seconds: retryAfter ?? 60 });
    if (status === 500) return t("err500");
    return t("err503");
  };

  const handleSend = async () => {
    const trimmed = input.trim();
    if (!trimmed || isLoading || retryCountdown > 0) return;

    const userMsg: ChatMessage = {
      id: "u_" + Date.now(),
      role: "user",
      content: trimmed,
      timestamp: Date.now(),
      exercise: exerciseId,
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsLoading(true);

    const controller = new AbortController();
    abortControllerRef.current = controller;

    try {
      const selectedProvider = provider === "auto" ? null : provider;
      const res: RagResponse = await askRag(
        {
          question: trimmed,
          exercise: exerciseId,
          provider: selectedProvider,
        },
        controller.signal,
      );

      const assistantMsg: ChatMessage = {
        id: "a_" + Date.now(),
        role: "assistant",
        content: res.answer,
        timestamp: Date.now(),
        refused: res.refused,
        sources: res.sources,
        cited: res.cited,
        tier: res.tier,
        exercise: exerciseId,
      };

      setMessages((prev) => [...prev, assistantMsg]);
      setIsOnline(true);
    } catch (err: unknown) {
      if (controller.signal.aborted) return;

      let status = 503;
      let retryAfter: number | null = null;
      if (err instanceof RagApiError) {
        status = err.status;
        retryAfter = err.retryAfter ?? null;
        if (status === 429 && retryAfter) {
          setRetryCountdown(retryAfter);
        }
      }

      const errorMsg: ChatMessage = {
        id: "err_" + Date.now(),
        role: "assistant",
        content: "",
        timestamp: Date.now(),
        error: getLocalizedErrorMessage(status, retryAfter),
        status,
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  };

  const handleHintNext = async (msg: ChatMessage) => {
    if (isLoading || retryCountdown > 0) return;

    setIsLoading(true);
    const controller = new AbortController();
    abortControllerRef.current = controller;

    try {
      const selectedProvider = provider === "auto" ? null : provider;
      // Find the user question that prompted this
      const userQuestion =
        [...messages]
          .reverse()
          .find((m) => m.role === "user")?.content ||
        "Gợi ý cho bài tập " + (msg.exercise || exerciseId || "");

      const res = await nextHint(
        {
          question: userQuestion,
          exercise: msg.exercise || exerciseId,
          provider: selectedProvider,
          current_tier: msg.tier ?? 1,
        },
        controller.signal,
      );

      // Append new progressive hint message
      const hintMsg: ChatMessage = {
        id: "hint_" + Date.now(),
        role: "assistant",
        content: res.answer,
        timestamp: Date.now(),
        refused: res.refused,
        sources: res.sources,
        cited: res.cited,
        tier: res.tier,
        exercise: msg.exercise || exerciseId,
      };

      setMessages((prev) => [...prev, hintMsg]);
    } catch (err: unknown) {
      if (controller.signal.aborted) return;
      let status = 503;
      let retryAfter: number | null = null;
      if (err instanceof RagApiError) {
        status = err.status;
        retryAfter = err.retryAfter ?? null;
        if (status === 429 && retryAfter) {
          setRetryCountdown(retryAfter);
        }
      }
      const errorMsg: ChatMessage = {
        id: "err_" + Date.now(),
        role: "assistant",
        content: "",
        timestamp: Date.now(),
        error: getLocalizedErrorMessage(status, retryAfter),
        status,
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  };

  const scrollToSource = (msgId: string, n: number) => {
    const targetId = `source-${msgId}-${n}`;
    setActiveSourceId(targetId);
    const el = document.getElementById(targetId);
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "nearest" });
      setTimeout(() => setActiveSourceId(null), 2500);
    }
  };

  const getTierLabel = (tier: number | null | undefined) => {
    if (tier === 1) return t("tier1");
    if (tier === 2) return t("tier2");
    if (tier === 3) return t("tier3");
    return null;
  };

  return (
    <>
      {/* Floating Toggle Button */}
      <button
        ref={toggleButtonRef}
        type="button"
        onClick={() => setIsOpen((prev) => !prev)}
        aria-expanded={isOpen}
        aria-controls="rag-chat-panel"
        aria-label={isOpen ? t("close") : t("open")}
        className={cn(
          "fixed bottom-5 right-5 z-40 flex items-center gap-2 rounded-full border-2 border-edge px-4 py-2.5 font-bold shadow-xl transition-all hover:scale-105 focus:outline-none focus-visible:ring-2 focus-visible:ring-ring",
          isOpen ? "bg-muted text-foreground" : "bg-primary text-primary-foreground",
        )}
      >
        <Bot className="size-5 shrink-0" />
        <span className="hidden sm:inline">{t("open")}</span>
        {isOnline === false && <span className="size-2 rounded-full bg-danger animate-pulse" />}
      </button>

      {/* Floating Chat Panel */}
      {isOpen && (
        <section
          id="rag-chat-panel"
          aria-label={t("title")}
          className={cn(
            "fixed z-50 flex flex-col rounded-lg border-2 border-border bg-card shadow-2xl transition-all duration-200 animate-rise",
            "bottom-4 right-3 sm:bottom-5 sm:right-5",
            isExpanded
              ? "h-[90vh] w-[96vw] sm:w-[680px]"
              : "h-[560px] max-h-[82vh] w-[calc(100vw-1.5rem)] sm:w-[420px]",
          )}
        >
          {/* Header */}
          <header className="flex items-center justify-between border-b px-4 py-3 bg-muted/40">
            <div className="flex items-center gap-2 min-w-0">
              <div className="flex size-8 shrink-0 items-center justify-center rounded-[4px] bg-primary/10 text-primary">
                <Sparkles className="size-4" />
              </div>
              <div className="min-w-0">
                <div className="flex items-center gap-2">
                  <h2 className="text-sm font-bold truncate leading-none">{t("title")}</h2>
                  <span
                    className={cn(
                      "size-2 shrink-0 rounded-full",
                      isOnline === true ? "bg-success" : isOnline === false ? "bg-danger" : "bg-muted-foreground",
                    )}
                    title={isOnline === false ? t("offline") : "Online"}
                  />
                </div>
                <p className="text-[11px] text-muted-foreground truncate leading-tight mt-0.5">
                  {exerciseId ? `Bài tập: ${exerciseId}` : `Bài học: ${lessonId}`}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-1">
              {/* Provider selector */}
              <select
                value={provider}
                onChange={(e) => setProvider(e.target.value as ProviderChoice)}
                className="h-7 rounded-[2px] border border-border bg-background px-2 text-xs font-medium text-foreground focus:outline-none"
                title={t("provider")}
                aria-label={t("provider")}
              >
                <option value="auto">{t("providerAuto")}</option>
                <option value="claude">Claude</option>
                <option value="gemini">Gemini</option>
              </select>

              {/* Clear chat */}
              {messages.length > 0 && (
                <Button
                  variant="ghost"
                  size="icon-sm"
                  onClick={() => setMessages([])}
                  title={t("clearChat")}
                  aria-label={t("clearChat")}
                >
                  <Trash2 className="size-3.5" />
                </Button>
              )}

              {/* Expand / Minimize */}
              <Button
                variant="ghost"
                size="icon-sm"
                className="hidden sm:inline-flex"
                onClick={() => setIsExpanded((prev) => !prev)}
                title={isExpanded ? "Thu nhỏ" : "Mở rộng"}
                aria-label={isExpanded ? "Thu nhỏ" : "Mở rộng"}
              >
                {isExpanded ? <Minimize2 className="size-3.5" /> : <Maximize2 className="size-3.5" />}
              </Button>

              {/* Close */}
              <Button
                variant="ghost"
                size="icon-sm"
                onClick={() => setIsOpen(false)}
                title={t("close")}
                aria-label={t("close")}
              >
                <X className="size-4" />
              </Button>
            </div>
          </header>

          {/* Offline notice banner */}
          {isOnline === false && (
            <div className="flex items-center justify-between gap-2 border-b border-warning/30 bg-warning-soft px-3 py-2 text-xs text-warning">
              <div className="flex items-center gap-1.5 min-w-0">
                <AlertCircle className="size-3.5 shrink-0" />
                <span className="truncate">{t("offline")}</span>
              </div>
              <button
                type="button"
                onClick={() => void verifyHealth()}
                className="flex items-center gap-1 underline font-bold shrink-0 hover:opacity-80"
              >
                <RefreshCw className="size-3" /> {t("retryConnection")}
              </button>
            </div>
          )}

          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 text-sm" aria-live="polite">
            {messages.length === 0 ? (
              <div className="flex h-full flex-col items-center justify-center p-6 text-center text-muted-foreground">
                <Bot className="size-12 mb-3 text-muted-foreground/40 stroke-1" />
                <p className="max-w-[280px] text-xs leading-relaxed">{t("emptyNotice")}</p>
              </div>
            ) : (
              messages.map((msg) => (
                <div
                  key={msg.id}
                  className={cn("flex flex-col", msg.role === "user" ? "items-end" : "items-start")}
                >
                  {/* User message */}
                  {msg.role === "user" ? (
                    <div className="max-w-[85%] rounded-2xl rounded-tr-sm bg-primary px-3.5 py-2 text-sm text-primary-foreground whitespace-pre-wrap break-words">
                      {msg.content}
                    </div>
                  ) : (
                    /* Assistant message */
                    <div className="max-w-[95%] space-y-3 rounded-2xl rounded-tl-sm border border-border bg-muted/40 p-3.5 text-sm">
                      {/* Refused notice */}
                      {msg.refused ? (
                        <div className="flex items-start gap-2 rounded-[4px] border border-warning/40 bg-warning-soft p-3 text-xs text-warning">
                          <AlertCircle className="size-4 shrink-0 mt-0.5" />
                          <span>{t("refused")}</span>
                        </div>
                      ) : msg.error ? (
                        /* Error message */
                        <div className="flex items-start gap-2 rounded-[4px] border border-danger/40 bg-danger-soft p-3 text-xs text-danger">
                          <AlertCircle className="size-4 shrink-0 mt-0.5" />
                          <span>{msg.error}</span>
                        </div>
                      ) : (
                        /* Standard answer */
                        <>
                          {/* Answer body with custom markdown */}
                          <div className="prose-lesson text-sm space-y-2 [&_p]:m-0 break-words">
                            <ReactMarkdown
                              remarkPlugins={[remarkGfm]}
                              rehypePlugins={[[rehypeHighlight, { detect: false }]]}
                              components={{
                                pre: ({ node, children }) => {
                                  const codeEl = (node as unknown as HastNode)?.children?.find(
                                    (c) => c.tagName === "code",
                                  );
                                  const classes = (codeEl?.properties?.className as string[] | undefined) ?? [];
                                  const lang = classes.find((c) => c.startsWith("language-"))?.replace("language-", "");
                                  const raw = textOf(codeEl).replace(/\n$/, "");
                                  const inner = (children as React.ReactElement<{ children?: React.ReactNode }>)?.props
                                    ?.children;
                                  return (
                                    <CodeBlock code={raw} language={lang}>
                                      {inner}
                                    </CodeBlock>
                                  );
                                },
                                a: ({ href, children }) => {
                                  if (href?.startsWith("#source-")) {
                                    const n = parseInt(href.replace("#source-", ""), 10);
                                    return (
                                      <button
                                        type="button"
                                        onClick={() => scrollToSource(msg.id, n)}
                                        className="mx-0.5 inline-flex items-center justify-center rounded bg-primary/15 px-1.5 py-0.2 font-mono text-xs font-bold text-primary align-baseline transition hover:bg-primary/25 cursor-pointer"
                                        title={`Xem nguồn [${n}]`}
                                      >
                                        [{n}]
                                      </button>
                                    );
                                  }
                                  return (
                                    <a
                                      href={href}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      className="text-primary underline hover:opacity-80"
                                    >
                                      {children}
                                    </a>
                                  );
                                },
                              }}
                            >
                              {transformCitations(msg.content)}
                            </ReactMarkdown>
                          </div>

                          {/* Tier label badge if available */}
                          {msg.tier && (
                            <div className="pt-1">
                              <Badge variant="outline" className="text-[11px]">
                                {getTierLabel(msg.tier) ?? t("tier", { n: msg.tier })}
                              </Badge>
                            </div>
                          )}

                          {/* Sources list */}
                          {msg.sources && msg.sources.length > 0 && (
                            <div className="mt-3 space-y-1.5 border-t border-border/60 pt-2.5">
                              <div className="text-xs font-bold text-muted-foreground">{t("sourcesTitle")}</div>
                              <ul className="space-y-1 text-xs">
                                {msg.sources.map((src) => {
                                  const isTargeted = activeSourceId === `source-${msg.id}-${src.n}`;
                                  return (
                                    <li
                                      key={src.n}
                                      id={`source-${msg.id}-${src.n}`}
                                      className={cn(
                                        "flex items-start gap-1.5 rounded p-1 transition-all",
                                        isTargeted && "bg-primary/15 ring-1 ring-primary",
                                      )}
                                    >
                                      <span className="font-mono font-bold text-primary shrink-0">[{src.n}]</span>
                                      <div className="min-w-0 flex-1">
                                        {src.lesson_id ? (
                                          <Link
                                            href={`/lesson/${src.lesson_id}/`}
                                            className="inline-flex items-center gap-1 font-medium text-primary hover:underline"
                                          >
                                            <span className="truncate">{src.title}</span>
                                            <ArrowUpRight className="size-3 shrink-0" />
                                          </Link>
                                        ) : src.url ? (
                                          <a
                                            href={src.url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="inline-flex items-center gap-1 font-medium text-primary hover:underline"
                                          >
                                            <span className="truncate">{src.title}</span>
                                            <ExternalLink className="size-3 shrink-0" />
                                          </a>
                                        ) : (
                                          <span className="font-medium text-foreground">{src.title}</span>
                                        )}
                                        {src.heading && (
                                          <span className="text-muted-foreground"> · {src.heading}</span>
                                        )}
                                      </div>
                                    </li>
                                  );
                                })}
                              </ul>
                            </div>
                          )}

                          {/* 3-Tier progressive hint button */}
                          {(msg.exercise || exerciseId) && (
                            <div className="pt-1">
                              {msg.tier && msg.tier >= 3 ? (
                                <span className="text-xs text-muted-foreground">{t("maxTierReached")}</span>
                              ) : (
                                <Button
                                  variant="outline"
                                  size="sm"
                                  onClick={() => void handleHintNext(msg)}
                                  disabled={isLoading || retryCountdown > 0}
                                  className="h-7 text-xs"
                                >
                                  <Lightbulb className="size-3 text-warning" />
                                  {t("nextHint")}
                                </Button>
                              )}
                            </div>
                          )}
                        </>
                      )}
                    </div>
                  )}
                </div>
              ))
            )}

            {/* Thinking / Loading indicator */}
            {isLoading && (
              <div className="flex items-center gap-2 rounded-2xl rounded-tl-sm border border-border bg-muted/40 p-3 text-xs text-muted-foreground">
                <RefreshCw className="size-3.5 animate-spin text-primary" />
                <span>{t("thinking")}</span>
                <button
                  type="button"
                  onClick={handleCancel}
                  className="ml-auto underline font-bold text-foreground hover:text-danger"
                >
                  {tc("cancel")}
                </button>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Footer */}
          <footer className="border-t p-3 bg-muted/20 space-y-2">
            {/* Rate-limit warning countdown if active */}
            {retryCountdown > 0 && (
              <div className="rounded bg-warning-soft px-2.5 py-1 text-xs text-warning font-medium">
                {t("err429", { seconds: retryCountdown })}
              </div>
            )}

            <div className="relative flex items-end gap-2">
              <textarea
                ref={textareaRef}
                value={input}
                onChange={(e) => setInput(e.target.value.slice(0, 1000))}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    void handleSend();
                  }
                }}
                disabled={isLoading || retryCountdown > 0}
                placeholder={t("placeholder")}
                rows={2}
                maxLength={1000}
                className="w-full resize-none rounded-[4px] border border-border bg-background p-2 text-xs text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring disabled:opacity-50"
              />
              <Button
                type="button"
                variant="default"
                size="icon"
                onClick={() => void handleSend()}
                disabled={!input.trim() || isLoading || retryCountdown > 0}
                title={t("send")}
                aria-label={t("send")}
                className="size-9 shrink-0"
              >
                <Send className="size-4" />
              </Button>
            </div>

            {/* Character count */}
            <div className="flex justify-between items-center text-[10px] text-muted-foreground px-0.5">
              <span>Enter gửi · Shift+Enter xuống dòng</span>
              <span className={cn(input.length > 900 && "text-warning font-bold", input.length >= 1000 && "text-danger")}>
                {input.length}/1000
              </span>
            </div>
          </footer>
        </section>
      )}
    </>
  );
}


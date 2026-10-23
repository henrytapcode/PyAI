"use client";

import { AlertTriangle, Check, Copy, Eye, Info, Lightbulb, Play } from "lucide-react";
import { useTranslations } from "next-intl";
import { useTheme } from "next-themes";
import { useEffect, useId, useState } from "react";
import ReactMarkdown, { type Components } from "react-markdown";
import rehypeHighlight from "rehype-highlight";
import remarkGfm from "remark-gfm";
import { visualize } from "@/components/visualizer";
import { cn } from "@/lib/utils";

type HastNode = {
  type: string;
  tagName?: string;
  value?: string;
  properties?: Record<string, unknown>;
  children?: HastNode[];
};

const CALLOUT = /^\[!(TIP|NOTE|WARNING)\]\s*/;

/** rehype plugin: `> [!TIP] ...` blockquotes become <aside data-callout="tip">. */
function rehypeCallouts() {
  const walk = (node: HastNode) => {
    for (const child of node.children ?? []) {
      if (child.type === "element" && child.tagName === "blockquote") {
        const p = child.children?.find((c) => c.type === "element" && c.tagName === "p");
        const first = p?.children?.[0];
        const m = first?.type === "text" ? CALLOUT.exec(first.value ?? "") : null;
        if (m && first) {
          first.value = (first.value ?? "").replace(CALLOUT, "");
          child.tagName = "aside";
          child.properties = { ...child.properties, dataCallout: m[1].toLowerCase() };
        }
      }
      walk(child);
    }
  };
  return (tree: HastNode) => walk(tree);
}

function textOf(node: HastNode | undefined): string {
  if (!node) return "";
  if (node.type === "text") return node.value ?? "";
  return (node.children ?? []).map(textOf).join("");
}

const CALLOUT_STYLE = {
  tip: { icon: Lightbulb, cls: "border-success/30 bg-success-soft/60", iconCls: "text-success" },
  note: { icon: Info, cls: "border-primary/25 bg-accent/60", iconCls: "text-primary" },
  warning: { icon: AlertTriangle, cls: "border-warning/40 bg-warning-soft/70", iconCls: "text-warning" },
} as const;

export function CodeBlock({
  code,
  children,
  language,
  onTry,
  canVisualize,
}: {
  code: string;
  children?: React.ReactNode;
  language?: string;
  onTry?: (code: string) => void;
  canVisualize?: boolean;
}) {
  const t = useTranslations();
  const [copied, setCopied] = useState(false);
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      /* clipboard blocked */
    }
  };
  return (
    <div className="group relative overflow-hidden rounded-xl border bg-code">
      <div className="flex items-center justify-between border-b px-3 py-1.5 text-xs text-muted-foreground">
        <span className="font-mono">{language ?? "python"}</span>
        <div className="flex items-center gap-1">
          <button onClick={copy} className="inline-flex items-center gap-1 rounded-md px-2 py-1 hover:bg-muted hover:text-foreground">
            {copied ? <Check className="size-3.5 text-success" /> : <Copy className="size-3.5" />}
            {copied ? t("common.copied") : t("common.copy")}
          </button>
          {canVisualize && (
            <button
              onClick={() => visualize(code)}
              className="inline-flex items-center gap-1 rounded-md px-2 py-1 font-medium hover:bg-muted hover:text-foreground"
            >
              <Eye className="size-3.5" />
              {t("lesson.visualize")}
            </button>
          )}
          {onTry && (
            <button
              onClick={() => onTry(code)}
              className="inline-flex items-center gap-1 rounded-md bg-primary/10 px-2 py-1 font-medium text-primary hover:bg-primary/15"
            >
              <Play className="size-3.5" />
              {t("lesson.tryIt")}
            </button>
          )}
        </div>
      </div>
      <pre className="overflow-x-auto p-4 font-mono text-[13.5px] leading-relaxed">
        <code className="hljs">{children ?? code}</code>
      </pre>
    </div>
  );
}

/** Flow diagrams from ```mermaid fences. Loaded lazily; falls back to the source if it fails to parse. */
function MermaidDiagram({ chart }: { chart: string }) {
  const id = "mmd" + useId().replace(/[^a-zA-Z0-9]/g, "");
  const { resolvedTheme } = useTheme();
  const [svg, setSvg] = useState<string | null>(null);
  const [failed, setFailed] = useState(false);
  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const mermaid = (await import("mermaid")).default;
        mermaid.initialize({ startOnLoad: false, theme: resolvedTheme === "dark" ? "dark" : "neutral", securityLevel: "strict" });
        const out = await mermaid.render(id, chart);
        if (alive) setSvg(out.svg);
      } catch {
        if (alive) setFailed(true);
      }
    })();
    return () => {
      alive = false;
    };
  }, [chart, id, resolvedTheme]);
  if (failed) return <CodeBlock code={chart} language="mermaid" />;
  return (
    <div
      className="my-4 flex justify-center overflow-x-auto rounded-xl border bg-card p-4 [&_svg]:h-auto [&_svg]:max-w-full"
      role="img"
      aria-label="diagram"
      dangerouslySetInnerHTML={svg ? { __html: svg } : undefined}
    />
  );
}

export function Markdown({ text, onTryCode, className }: { text: string; onTryCode?: (code: string) => void; className?: string }) {
  const components: Components = {
    pre: ({ node, children }) => {
      const codeEl = (node as unknown as HastNode)?.children?.find((c) => c.tagName === "code");
      const classes = (codeEl?.properties?.className as string[] | undefined) ?? [];
      const lang = classes.find((c) => c.startsWith("language-"))?.replace("language-", "");
      const raw = textOf(codeEl).replace(/\n$/, "");
      const inner = (children as React.ReactElement<{ children?: React.ReactNode }>)?.props?.children;
      const isPython = !lang || lang === "python" || lang === "py";
      if (lang === "mermaid") return <MermaidDiagram chart={raw} />;
      return (
        <CodeBlock code={raw} language={lang} onTry={isPython ? onTryCode : undefined} canVisualize={isPython}>
          {inner}
        </CodeBlock>
      );
    },
    aside: ({ node, children }) => {
      const kind = ((node as unknown as HastNode)?.properties?.dataCallout as keyof typeof CALLOUT_STYLE) ?? "note";
      const style = CALLOUT_STYLE[kind] ?? CALLOUT_STYLE.note;
      const Icon = style.icon;
      return (
        <aside className={cn("flex gap-3 rounded-xl border px-4 py-3 text-[0.95rem] [&_p]:m-0", style.cls)}>
          <Icon className={cn("mt-1 size-[18px] shrink-0", style.iconCls)} />
          <div className="min-w-0 space-y-2">{children}</div>
        </aside>
      );
    },
    a: ({ children, href }) => (
      <a href={href} target={href?.startsWith("http") ? "_blank" : undefined} rel="noreferrer">
        {children}
      </a>
    ),
  };
  return (
    <div className={cn("prose-lesson", className)}>
      <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeCallouts, [rehypeHighlight, { detect: false }]]} components={components}>
        {text}
      </ReactMarkdown>
    </div>
  );
}

/** Highlighted, non-editable code (quiz questions, flashcards). */
export function StaticCode({ code, className }: { code: string; className?: string }) {
  return (
    <div className={className}>
      <Markdown text={"```python\n" + code.replace(/\n$/, "") + "\n```"} />
    </div>
  );
}

"use client";

import Editor, { type BeforeMount, type OnMount } from "@monaco-editor/react";
import { useTranslations } from "next-intl";
import { useTheme } from "next-themes";
import { useEffect, useRef } from "react";

type MonacoEditor = Parameters<OnMount>[0];
type Monaco = Parameters<OnMount>[1];

const defineThemes: BeforeMount = (monaco) => {
  monaco.editor.defineTheme("pyai-light", {
    base: "vs",
    inherit: true,
    rules: [{ token: "comment", foreground: "8a8a9a", fontStyle: "italic" }],
    colors: {
      "editor.background": "#ffffff",
      "editorLineNumber.foreground": "#b4b4c4",
      "editor.lineHighlightBackground": "#f5f5fa",
      "editorGutter.background": "#ffffff",
    },
  });
  monaco.editor.defineTheme("pyai-dark", {
    base: "vs-dark",
    inherit: true,
    rules: [{ token: "comment", foreground: "7d7d92", fontStyle: "italic" }],
    colors: {
      "editor.background": "#1b1b24",
      "editorLineNumber.foreground": "#4d4d60",
      "editor.lineHighlightBackground": "#22222d",
      "editorGutter.background": "#1b1b24",
    },
  });
};

export interface CodeEditorProps {
  value: string;
  onChange?: (value: string) => void;
  onRun?: () => void;
  onCheck?: () => void;
  readOnly?: boolean;
  errorLine?: number | null;
  /** Highlight `___` placeholders (fill-in-the-blank exercises). */
  highlightBlanks?: boolean;
  className?: string;
}

export function CodeEditor({ value, onChange, onRun, onCheck, readOnly, errorLine, highlightBlanks, className }: CodeEditorProps) {
  const { resolvedTheme } = useTheme();
  const t = useTranslations("editor");
  const editorRef = useRef<MonacoEditor | null>(null);
  const monacoRef = useRef<Monaco | null>(null);
  const decorations = useRef<ReturnType<MonacoEditor["createDecorationsCollection"]> | null>(null);
  // Keep the latest callbacks without re-registering Monaco commands.
  const handlers = useRef({ onRun, onCheck });
  handlers.current = { onRun, onCheck };

  const decorate = () => {
    const editor = editorRef.current;
    const monaco = monacoRef.current;
    if (!editor || !monaco) return;
    const model = editor.getModel();
    if (!model) return;
    const items: Parameters<MonacoEditor["createDecorationsCollection"]>[0] = [];
    if (highlightBlanks) {
      for (const m of model.findMatches("___", false, false, true, null, false)) {
        items.push({ range: m.range, options: { inlineClassName: "blank-decoration" } });
      }
    }
    if (errorLine && errorLine <= model.getLineCount()) {
      items.push({
        range: new monaco.Range(errorLine, 1, errorLine, 1),
        options: { isWholeLine: true, className: "error-line-decoration" },
      });
    }
    decorations.current?.clear();
    decorations.current = editor.createDecorationsCollection(items);
  };

  useEffect(decorate, [value, errorLine, highlightBlanks]); // eslint-disable-line react-hooks/exhaustive-deps

  const onMount: OnMount = (editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => handlers.current.onRun?.());
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.Enter, () =>
      (handlers.current.onCheck ?? handlers.current.onRun)?.(),
    );
    decorate();
  };

  return (
    <div className={className}>
      <Editor
        language="python"
        value={value}
        onChange={(v) => onChange?.(v ?? "")}
        beforeMount={defineThemes}
        onMount={onMount}
        theme={resolvedTheme === "dark" ? "pyai-dark" : "pyai-light"}
        loading={<div className="grid h-full place-items-center text-sm text-muted-foreground">{t("loading")}</div>}
        options={{
          readOnly,
          fontSize: 14,
          fontFamily: "var(--font-mono-face), 'JetBrains Mono', Consolas, monospace",
          fontLigatures: true,
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 4,
          insertSpaces: true,
          lineNumbersMinChars: 3,
          padding: { top: 12, bottom: 12 },
          renderLineHighlight: "line",
          smoothScrolling: true,
          wordWrap: "on",
          scrollbar: { verticalScrollbarSize: 8, horizontalScrollbarSize: 8 },
          overviewRulerLanes: 0,
          guides: { indentation: true },
          stickyScroll: { enabled: false },
        }}
      />
    </div>
  );
}

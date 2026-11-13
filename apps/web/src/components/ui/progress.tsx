import type { CSSProperties } from "react";
import { cn } from "@/lib/utils";

/** Meter: the fill scales with transform scaleX, never animating width. */
export function Progress({ value, className, tone = "primary" }: { value: number; className?: string; tone?: "primary" | "success" }) {
  const clamped = Math.max(0, Math.min(1, value));
  return (
    <div
      role="progressbar"
      aria-valuemin={0}
      aria-valuemax={100}
      aria-valuenow={Math.round(clamped * 100)}
      className={cn("meter w-full", className)}
      style={{ "--scale": clamped, "--meter-fill": tone === "success" ? "var(--success)" : "var(--primary)" } as CSSProperties}
    >
      <i />
    </div>
  );
}

/** Ring with a label in the middle: clean circular progress indicator. */
export function Ring({
  value,
  size = 56,
  stroke = 5,
  children,
  className,
}: {
  value: number;
  size?: number;
  stroke?: number;
  children?: React.ReactNode;
  className?: string;
}) {
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const v = Math.max(0, Math.min(1, value));
  return (
    <div className={cn("relative inline-grid place-items-center", className)} style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90" aria-hidden="true">
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="var(--muted)" strokeWidth={stroke} />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke={v >= 1 ? "var(--success)" : "var(--primary)"}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={c}
          strokeDashoffset={c * (1 - v)}
          className="transition-[stroke-dashoffset] duration-300"
        />
      </svg>
      <div className="absolute inset-0 grid place-items-center font-mono text-xs font-bold tabular-nums">{children}</div>
    </div>
  );
}

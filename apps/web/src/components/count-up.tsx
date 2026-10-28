"use client";

import { useEffect, useRef, useState } from "react";

function reduced() {
  return typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

/** Rolls a number from its previous value to the new one. Shows the target at once under reduced motion. */
export function useRoll(value: number, { fromZero = false, ms = 700 }: { fromZero?: boolean; ms?: number } = {}) {
  const [shown, setShown] = useState(fromZero ? 0 : value);
  // What is on screen right now, so an interrupted roll (or a strict-mode re-run) starts from there.
  const cur = useRef(fromZero ? 0 : value);
  useEffect(() => {
    const from = cur.current;
    if (from === value) return;
    if (reduced()) {
      cur.current = value;
      setShown(value);
      return;
    }
    // Timer, not rAF: it still lands on the final value when the tab is throttled or off screen.
    const t0 = performance.now();
    let id: ReturnType<typeof setTimeout>;
    const step = () => {
      const k = Math.min(1, (performance.now() - t0) / ms);
      const v = Math.round(from + (value - from) * (1 - (1 - k) ** 3));
      cur.current = v;
      setShown(v);
      if (k < 1) id = setTimeout(step, 16);
    };
    id = setTimeout(step, 16);
    return () => clearTimeout(id);
  }, [value, ms]);
  return shown;
}

/** A score that counts up from zero when it first appears. */
export function CountUp({ value }: { value: number }) {
  return <>{useRoll(value, { fromZero: true })}</>;
}

/** A running total: rolls on change and floats the gain above it. */
export function XpFigure({ value, className }: { value: number; className?: string }) {
  const shown = useRoll(value);
  const prev = useRef(value);
  const [gain, setGain] = useState(0);
  const timer = useRef<ReturnType<typeof setTimeout>>(undefined);
  useEffect(() => {
    const d = value - prev.current;
    prev.current = value;
    if (d <= 0 || reduced()) return;
    setGain(d);
    clearTimeout(timer.current);
    timer.current = setTimeout(() => setGain(0), 1200);
  }, [value]);
  useEffect(() => () => clearTimeout(timer.current), []);
  return (
    <span className="relative inline-block">
      <span className={className}>{shown}</span>
      {gain > 0 && (
        <span aria-hidden className="xp-pop pointer-events-none absolute -top-1 right-0 text-sm font-black text-hit">
          +{gain}
        </span>
      )}
    </span>
  );
}

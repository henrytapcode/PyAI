"use client";

import { useEffect, useRef, useState } from "react";

function reduced() {
  return typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

/** Rolls a number from its previous value to the new one. Shows the target at once under reduced motion. */
export function useRoll(value: number, { fromZero = false, ms = 700 }: { fromZero?: boolean; ms?: number } = {}) {
  const [shown, setShown] = useState(fromZero ? 0 : value);
  const last = useRef(fromZero ? 0 : value);
  useEffect(() => {
    const from = last.current;
    last.current = value;
    if (from === value) return;
    if (reduced()) {
      setShown(value);
      return;
    }
    const t0 = performance.now();
    let raf = 0;
    const step = (now: number) => {
      const k = Math.min(1, (now - t0) / ms);
      setShown(Math.round(from + (value - from) * (1 - (1 - k) ** 3)));
      if (k < 1) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
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
  useEffect(() => {
    const d = value - prev.current;
    prev.current = value;
    if (d <= 0 || reduced()) return;
    setGain(d);
    const id = setTimeout(() => setGain(0), 1200);
    return () => clearTimeout(id);
  }, [value]);
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

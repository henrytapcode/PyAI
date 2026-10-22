import { Brain, Code2, Layers, Network, Rocket, ShieldCheck, Sparkles, Table2, Terminal, type LucideIcon } from "lucide-react";

const ICONS: Record<string, LucideIcon> = {
  terminal: Terminal,
  code: Code2,
  layers: Layers,
  "shield-check": ShieldCheck,
  table: Table2,
  brain: Brain,
  network: Network,
  sparkles: Sparkles,
  rocket: Rocket,
};

export function PhaseIcon({ name, className }: { name: string; className?: string }) {
  const Icon = ICONS[name] ?? Code2;
  return <Icon className={className} />;
}

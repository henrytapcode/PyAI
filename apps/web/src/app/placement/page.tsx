import { PlacementView } from "@/components/placement-view";
import { getExam } from "@/lib/content-server";
import { catalog } from "@/lib/content";

export default function PlacementPage() {
  const summary = catalog.exams.find((e) => e.kind === "placement");
  if (!summary) return null;
  return <PlacementView exam={getExam(summary.id)} />;
}

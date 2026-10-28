import { cva, type VariantProps } from "class-variance-authority";
import * as React from "react";
import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center gap-1 rounded-[2px] border-2 px-1.5 py-0.5 text-xs font-bold whitespace-nowrap [&_svg]:size-3",
  {
    variants: {
      variant: {
        default: "border-accent-foreground bg-accent text-accent-foreground",
        outline: "border-border text-muted-foreground",
        success: "border-success bg-success-soft text-success",
        danger: "border-danger bg-danger-soft text-danger",
        warning: "border-warning bg-warning-soft text-warning",
        muted: "border-transparent bg-muted text-muted-foreground",
      },
    },
    defaultVariants: { variant: "default" },
  },
);

export function Badge({ className, variant, ...props }: React.ComponentProps<"span"> & VariantProps<typeof badgeVariants>) {
  return <span className={cn(badgeVariants({ variant }), className)} {...props} />;
}

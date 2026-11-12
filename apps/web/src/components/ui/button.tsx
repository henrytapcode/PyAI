import { cva, type VariantProps } from "class-variance-authority";
import { Slot } from "radix-ui";
import * as React from "react";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "relative inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring select-none",
  {
    variants: {
      variant: {
        default: "press [--press-edge:var(--primary-ink)] border-[var(--press-edge)] bg-primary text-primary-foreground hover:opacity-95",
        secondary: "press bg-secondary text-secondary-foreground hover:bg-accent",
        outline: "press bg-card text-foreground hover:bg-muted",
        ghost: "row-cursor text-foreground hover:bg-accent hover:text-primary",
        soft: "border border-border bg-accent text-primary hover:bg-accent/80",
        success: "press [--press-edge:var(--primary-ink)] border-[var(--press-edge)] bg-success text-success-foreground hover:opacity-95",
        danger:
          "press [--press-edge:color-mix(in_oklch,var(--danger)_75%,var(--foreground))] border-[var(--press-edge)] bg-danger text-danger-foreground hover:opacity-95",
        link: "text-foreground underline decoration-border underline-offset-4 hover:decoration-primary hover:text-primary",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 gap-1.5 px-3 text-xs",
        lg: "h-11 px-6 text-base",
        icon: "size-10 after:absolute after:-inset-1 after:content-['']",
        "icon-sm": "size-9 after:absolute after:-inset-[4px] after:content-['']",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  },
);

export interface ButtonProps extends React.ComponentProps<"button">, VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

export function Button({ className, variant, size, asChild = false, ...props }: ButtonProps) {
  const Comp = asChild ? Slot.Root : "button";
  return <Comp data-slot="button" className={cn(buttonVariants({ variant, size, className }))} {...props} />;
}

export { buttonVariants };

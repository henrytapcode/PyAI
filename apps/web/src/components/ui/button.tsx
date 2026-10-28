import { cva, type VariantProps } from "class-variance-authority";
import { Slot } from "radix-ui";
import * as React from "react";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-[4px] text-sm font-bold disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-ring",
  {
    variants: {
      variant: {
        default: "press bg-primary text-primary-foreground",
        secondary: "press bg-secondary text-secondary-foreground",
        outline: "press bg-card text-foreground",
        ghost: "row-cursor text-foreground hover:text-primary-foreground",
        soft: "border-2 border-border bg-accent text-accent-foreground hover:border-hit",
        success: "press bg-success text-success-foreground",
        danger: "press bg-danger text-primary-foreground",
        link: "text-foreground underline decoration-hit decoration-2 underline-offset-4 hover:decoration-primary",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-8 gap-1.5 px-3 text-[13px]",
        lg: "h-12 px-6 text-base",
        icon: "size-10",
        "icon-sm": "size-8",
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

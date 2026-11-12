"use client";

import { X } from "lucide-react";
import { Dialog as DialogPrimitive } from "radix-ui";
import { useTranslations } from "next-intl";
import * as React from "react";
import { cn } from "@/lib/utils";

export const Dialog = DialogPrimitive.Root;
export const DialogTrigger = DialogPrimitive.Trigger;
export const DialogClose = DialogPrimitive.Close;

export function DialogContent({ className, children, ...props }: React.ComponentProps<typeof DialogPrimitive.Content>) {
  const tc = useTranslations("common");
  return (
    <DialogPrimitive.Portal>
      <DialogPrimitive.Overlay className="fixed inset-0 z-50 bg-[color-mix(in_oklch,var(--foreground)_35%,transparent)] data-[state=open]:animate-in data-[state=open]:fade-in-0 data-[state=closed]:animate-out data-[state=closed]:fade-out-0" />
      <DialogPrimitive.Content
        className={cn(
          "fixed left-1/2 top-1/2 z-50 grid w-[calc(100%-2rem)] max-w-lg -translate-x-1/2 -translate-y-1/2 gap-4 rounded-lg bg-popover p-6 shadow-[var(--shadow-lift)] data-[state=open]:animate-in data-[state=open]:fade-in-0 data-[state=open]:zoom-in-95",
          className,
        )}
        {...props}
      >
        {children}
        <DialogPrimitive.Close
          aria-label={tc("close")}
          className="absolute right-3.5 top-3.5 inline-flex size-9 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-accent hover:text-primary focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
        >
          <X className="size-4" aria-hidden="true" />
          <span className="sr-only">{tc("close")}</span>
        </DialogPrimitive.Close>
      </DialogPrimitive.Content>
    </DialogPrimitive.Portal>
  );
}

export function DialogTitle({ className, ...props }: React.ComponentProps<typeof DialogPrimitive.Title>) {
  return <DialogPrimitive.Title className={cn("text-lg font-bold tracking-tight", className)} {...props} />;
}

export function DialogDescription({ className, ...props }: React.ComponentProps<typeof DialogPrimitive.Description>) {
  return <DialogPrimitive.Description className={cn("text-sm text-muted-foreground", className)} {...props} />;
}

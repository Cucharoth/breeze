import { cn } from "@/lib/utils";

interface GlassPanelProps extends React.HTMLAttributes<HTMLDivElement> {
  hoverable?: boolean;
}

export function GlassPanel({
  className,
  children,
  hoverable = true,
  ...props
}: GlassPanelProps) {
  return (
    <div
      className={cn(
        "glass-panel",
        !hoverable && "hover:border-[var(--glass-border)] hover:shadow-none",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

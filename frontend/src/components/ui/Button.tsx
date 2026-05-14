import { cn } from "@/lib/utils";
import { LucideIcon } from "lucide-react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline";
  icon?: LucideIcon;
  loading?: boolean;
}

export function Button({
  className,
  variant = "primary",
  icon: Icon,
  loading,
  children,
  ...props
}: ButtonProps) {
  const variants = {
    primary: "btn-primary",
    secondary: "bg-white/5 text-text-primary hover:bg-white/10",
    outline: "border border-[var(--glass-border)] hover:border-primary/50",
  };

  return (
    <button
      className={cn(
        variants[variant],
        "active:scale-95 transition-transform",
        loading && "opacity-50 cursor-not-allowed",
        className
      )}
      disabled={loading}
      {...props}
    >
      {loading ? (
        <span className="animate-pulse">Processing...</span>
      ) : (
        <>
          {Icon && <Icon className="size-4" />}
          {children}
        </>
      )}
    </button>
  );
}

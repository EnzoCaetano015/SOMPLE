import type { StatusIndicatorProps } from "./StatusIndicator.types";

export const StatusIndicator = ({ online, label }: StatusIndicatorProps) => {
  return (
    <div className="flex items-center gap-2 text-sm text-muted-foreground">
      <span
        className={`size-2 rounded-full ${online ? "bg-somple-highlight" : "bg-somple-danger"}`}
        aria-hidden="true"
      />
      <span>{label}</span>
    </div>
  );
};

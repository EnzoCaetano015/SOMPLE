import type { ComponentProps } from "react";

export type NeumorphicCardVariant = "raised" | "inset" | "flat";

export interface NeumorphicCardProps extends ComponentProps<"div"> {
  variant?: NeumorphicCardVariant;
}

import type { NeumorphicCardProps } from "./NeumorphicCard.types";
import { NEUMORPHIC_CARD_VARIANTS } from "./NeumorphicCard.utils";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

export const NeumorphicCard = ({
  variant = "raised",
  className,
  children,
  ...props
}: NeumorphicCardProps) => {
  return (
    <Card className={cn(NEUMORPHIC_CARD_VARIANTS[variant], className)} {...props}>
      {children}
    </Card>
  );
};

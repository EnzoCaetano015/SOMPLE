import type { NeumorphicCardVariant } from "./NeumorphicCard.types";
import { NEU_CARD_INSET, NEU_CARD_RAISED } from "@/lib/utils/neumorphic.utils";

export const NEUMORPHIC_CARD_VARIANTS: Record<NeumorphicCardVariant, string> = {
  raised: NEU_CARD_RAISED,
  inset: NEU_CARD_INSET,
  flat: "border border-somple-border/60 bg-somple-bg rounded-neumorphic shadow-none",
};

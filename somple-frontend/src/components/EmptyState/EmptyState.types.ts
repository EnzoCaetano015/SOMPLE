import type { LucideIcon } from "lucide-react";

export interface EmptyStateProps {
  title: string;
  description?: string;
  Icon?: LucideIcon;
  actionLabel?: string;
  onAction?: () => void;
}

export const EMPTY_STATE_DEFAULT_DESCRIPTION =
  "Tente ajustar os filtros ou revise os termos de busca.";

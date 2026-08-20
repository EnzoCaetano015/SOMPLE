import type { LucideIcon } from "lucide-react";

export type SidebarItem = {
  label: string;
  href: string;
  icon: LucideIcon;
  badge?: string;
};

export type SidebarGroup = {
  label: string;
  items: SidebarItem[];
};

export type SidebarProps = {
  isOpen: boolean;
  onNavigate: () => void;
};

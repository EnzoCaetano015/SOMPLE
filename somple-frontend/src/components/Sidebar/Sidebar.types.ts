import type { LucideIcon } from "lucide-react";

import type { Enum } from "@/api/enums/enum";

export type SidebarItem = {
  label: string;
  href: string;
  icon: LucideIcon;
  badge?: string;
  allowedRoles?: readonly Enum.UserRole[];
};

export type SidebarGroup = {
  label: string;
  items: SidebarItem[];
};

export type SidebarProps = {
  isOpen: boolean;
  onNavigate: () => void;
};

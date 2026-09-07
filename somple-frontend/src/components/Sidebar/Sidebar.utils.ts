import {
  Activity,
  Bell,
  FileText,
  History,
  LayoutDashboard,
  Map,
  Settings,
  Tractor,
} from "lucide-react";

import type { SidebarGroup } from "./Sidebar.types";
import { ANALYTICAL_ROLES } from "@/lib/auth/permissions";

export const SIDEBAR_GROUPS: SidebarGroup[] = [
  {
    label: "Principal",
    items: [
      { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
      { label: "Monitoramento", href: "/monitoring", icon: Activity },
      { label: "Equipamentos", href: "/equipment", icon: Tractor },
      { label: "Operações", href: "/operations", icon: Map },
      { label: "Alertas", href: "/alerts", icon: Bell, badge: "6" },
    ],
  },
  {
    label: "Dados",
    items: [
      { label: "Histórico", href: "/audit", icon: History, allowedRoles: ANALYTICAL_ROLES },
      { label: "Relatórios", href: "#", icon: FileText },
    ],
  },
  {
    label: "",
    items: [{ label: "Configurações", href: "#", icon: Settings }],
  },
];

export const ROUTE_TITLES: Record<string, string> = {
  "/dashboard": "Dashboard operacional",
  "/monitoring": "Monitoramento operacional",
  "/equipment": "Equipamentos",
  "/operations": "Operações",
  "/alerts": "Alertas",
  "/audit": "Histórico",
};

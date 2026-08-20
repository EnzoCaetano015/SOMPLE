import { Bell, LogOut, Menu } from "lucide-react";
import { useLocation } from "react-router";

import { useTopbar } from "./Topbar.hook";
import type { TopbarProps } from "./Topbar.types";
import { ROUTE_TITLES } from "@/components/Sidebar/Sidebar.utils";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export const Topbar = ({ onMenuClick }: TopbarProps) => {
  const { pathname } = useLocation();
  const { lastUpdatedLabel, handleLogout } = useTopbar();
  const title =
    ROUTE_TITLES[pathname] ??
    (pathname.startsWith("/equipment/") ? "Detalhe do equipamento" : "SOMPLE");

  return (
    <header className="z-10 flex h-14 shrink-0 items-center justify-between border-b border-somple-border bg-somple-bg/92 px-4 backdrop-blur-md md:px-7">
      <div className="flex items-center gap-3">
        <button
          type="button"
          aria-label="Abrir menu"
          onClick={onMenuClick}
          className="flex size-9 items-center justify-center rounded-[10px] bg-somple-bg shadow-neumorphic-soft md:hidden"
        >
          <Menu className="size-4 text-somple-muted" />
        </button>
        <p className="text-[15px] font-semibold text-somple-ink">{title}</p>
      </div>
      <div className="flex items-center gap-3 md:gap-5">
        <span className="hidden font-mono text-[11px] text-somple-muted sm:inline">
          {lastUpdatedLabel}
        </span>
        <span className="hidden items-center gap-1.5 font-mono text-[11px] text-somple-field sm:flex">
          <span className="size-[7px] animate-somple-pulse rounded-full bg-somple-field" />
          Sistema online
        </span>
        <button
          type="button"
          aria-label="Notificações"
          className="relative flex size-9 items-center justify-center rounded-[10px] bg-somple-bg shadow-neumorphic-soft"
        >
          <Bell className="size-4 text-somple-muted" />
          <span className="absolute top-1.5 right-1.5 size-[7px] rounded-full border-[1.5px] border-somple-bg bg-somple-danger" />
        </button>

        <DropdownMenu>
          <DropdownMenuTrigger
            aria-label="Abrir menu do perfil"
            className="flex size-[34px] cursor-pointer items-center justify-center rounded-full bg-somple-corporate text-[13px] font-bold text-somple-white transition-opacity hover:opacity-90"
          >
            JR
          </DropdownMenuTrigger>
          <DropdownMenuContent
            align="end"
            side="bottom"
            sideOffset={8}
            className="min-w-44 rounded-neumorphic-sm border-somple-border bg-somple-white p-1.5 shadow-neumorphic-soft"
          >
            <DropdownMenuGroup>
              <DropdownMenuLabel className="px-2.5 py-2 text-xs font-medium text-somple-muted">
                Minha conta
              </DropdownMenuLabel>
              <DropdownMenuItem
                variant="destructive"
                onClick={handleLogout}
                className="cursor-pointer rounded-[10px] px-2.5 py-2"
              >
                <LogOut className="size-4" />
                Sair
              </DropdownMenuItem>
            </DropdownMenuGroup>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
};

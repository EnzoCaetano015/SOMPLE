import { Tractor } from "lucide-react";
import { NavLink } from "react-router";

import type { SidebarProps } from "./Sidebar.types";
import { SIDEBAR_GROUPS } from "./Sidebar.utils";
import { cn } from "@/lib/utils";

export const Sidebar = ({ isOpen, onNavigate }: SidebarProps) => {
  return (
    <>
      {isOpen ? (
        <button
          type="button"
          aria-label="Fechar menu"
          className="fixed inset-0 z-40 bg-black/30 md:hidden"
          onClick={onNavigate}
        />
      ) : null}
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-50 flex w-65 shrink-0 flex-col bg-somple-bg shadow-[4px_0_16px_rgba(28,28,28,0.06)] transition-transform duration-200 md:static md:translate-x-0 lg:w-55",
          isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0",
        )}
      >
        <div className="flex items-center gap-2.5 border-b border-somple-border px-6 py-5">
          <div className="flex size-9 items-center justify-center rounded-[10px] bg-somple-corporate text-somple-white">
            <Tractor className="size-4.5" aria-hidden="true" />
          </div>
          <span className="text-lg font-bold tracking-tight text-somple-corporate">SOMPLE</span>
        </div>

        <nav className="flex flex-1 flex-col gap-0.5 overflow-y-auto px-3 py-4">
          {SIDEBAR_GROUPS.map((group) => (
            <div key={group.label || "settings"} className={group.label ? "" : "mt-auto"}>
              {group.label ? (
                <p className="px-3 py-3 font-mono text-[10px] tracking-widest text-somple-muted uppercase">
                  {group.label}
                </p>
              ) : null}
              <ul className="space-y-0.5">
                {group.items.map((item) => (
                  <li key={item.label}>
                    {item.href.startsWith("/") ? (
                      <NavLink
                        to={item.href}
                        viewTransition
                        onClick={onNavigate}
                        className={({ isActive }) =>
                          cn(
                            "relative flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm font-medium transition-all duration-150",
                            isActive
                              ? "bg-somple-bg font-semibold text-somple-corporate shadow-neumorphic-inset"
                              : "text-somple-muted hover:bg-black/4 hover:text-somple-ink",
                          )
                        }
                      >
                        {({ isActive }) => (
                          <>
                            {isActive ? (
                              <span className="absolute top-1/2 left-0 h-5 w-0.75 -translate-y-1/2 rounded-r bg-somple-highlight" />
                            ) : null}
                            <item.icon className="size-4.5 shrink-0" aria-hidden="true" />
                            <span className="flex-1">{item.label}</span>
                            {item.badge ? (
                              <span className="flex size-5 items-center justify-center rounded-full bg-somple-danger font-mono text-[10px] font-bold text-somple-white">
                                {item.badge}
                              </span>
                            ) : null}
                          </>
                        )}
                      </NavLink>
                    ) : (
                      <span className="flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm text-somple-muted/70">
                        <item.icon className="size-4.5 shrink-0" aria-hidden="true" />
                        {item.label}
                      </span>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </nav>
      </aside>
    </>
  );
};

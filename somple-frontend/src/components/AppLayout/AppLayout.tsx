import { Outlet } from "react-router";

import { useAppLayout } from "./AppLayout.hook";
import { OfflineBanner } from "@/components/OfflineBanner/OfflineBanner";
import { Sidebar } from "@/components/Sidebar/Sidebar";
import { Topbar } from "@/components/Topbar/Topbar";
import { useNetworkStatus } from "@/lib/hooks/useNetworkStatus.hook";

export const AppLayout = () => {
  const { isSidebarOpen, toggleSidebar, closeSidebar } = useAppLayout();
  const { isOffline } = useNetworkStatus();

  return (
    <div className="flex h-screen overflow-hidden bg-somple-bg">
      <Sidebar isOpen={isSidebarOpen} onNavigate={closeSidebar} />
      <div className="flex min-w-0 flex-1 flex-col">
        {isOffline ? <OfflineBanner /> : null}
        <Topbar onMenuClick={toggleSidebar} />
        <main className="content-scroll page-content flex-1 overflow-y-auto p-4 md:p-5 lg:p-7">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

import { Navigate, Outlet } from "react-router";

import { isAuthenticated } from "@/lib/auth/token.storage";

export const GuestOnly = () => {
  if (isAuthenticated()) {
    return <Navigate to="/dashboard" replace />;
  }

  return <Outlet />;
};

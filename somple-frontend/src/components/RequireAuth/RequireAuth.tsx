import { Navigate, Outlet, useLocation } from "react-router";

import { isAuthenticated } from "@/lib/auth/token.storage";

export const RequireAuth = () => {
  const location = useLocation();

  if (!isAuthenticated()) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  return <Outlet />;
};

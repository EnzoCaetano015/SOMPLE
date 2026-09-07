import { Navigate, Outlet } from "react-router";

import type { Enum } from "@/api/enums/enum";
import { hasRole } from "@/lib/auth/permissions";

type RequireRoleProps = {
  allowedRoles: readonly Enum.UserRole[];
};

export const RequireRole = ({ allowedRoles }: RequireRoleProps) => {
  if (!hasRole(...allowedRoles)) {
    return <Navigate to="/dashboard" replace />;
  }

  return <Outlet />;
};

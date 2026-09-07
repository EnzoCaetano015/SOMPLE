import { Enum } from "@/api/enums/enum";
import { decodeJwtPayload, getAuthToken } from "@/lib/auth/token.storage";

export type CurrentUser = {
  id: number;
  email: string;
  role: Enum.UserRole;
};

export const ALL_ROLES = [
  Enum.UserRole.ADMIN,
  Enum.UserRole.ANALYST,
  Enum.UserRole.OPERATOR,
] as const;

export const ANALYTICAL_ROLES = [Enum.UserRole.ADMIN, Enum.UserRole.ANALYST] as const;

const isUserRole = (role: string | undefined): role is Enum.UserRole =>
  role !== undefined && Object.values(Enum.UserRole).includes(role as Enum.UserRole);

export const currentUser = (): CurrentUser | null => {
  const token = getAuthToken();
  if (!token) return null;

  const payload = decodeJwtPayload(token);
  if (!payload?.user_id || !payload.sub || !isUserRole(payload.role)) return null;

  return {
    id: payload.user_id,
    email: payload.sub,
    role: payload.role,
  };
};

export const currentRole = (): Enum.UserRole | null => currentUser()?.role ?? null;

export const hasRole = (...allowedRoles: readonly Enum.UserRole[]): boolean => {
  const role = currentRole();
  return role !== null && allowedRoles.includes(role);
};

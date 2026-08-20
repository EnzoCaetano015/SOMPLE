const AUTH_TOKEN_KEY = "somple_auth_token";

type JwtPayload = {
  exp?: number;
};

const decodeJwtPayload = (token: string): JwtPayload | null => {
  try {
    const payload = token.split(".")[1];
    if (!payload) return null;

    return JSON.parse(atob(payload.replace(/-/g, "+").replace(/_/g, "/"))) as JwtPayload;
  } catch {
    return null;
  }
};

export const getAuthToken = (): string | null => {
  return localStorage.getItem(AUTH_TOKEN_KEY);
};

export const setAuthToken = (token: string): void => {
  localStorage.setItem(AUTH_TOKEN_KEY, token);
};

export const clearAuthToken = (): void => {
  localStorage.removeItem(AUTH_TOKEN_KEY);
};

export const isAuthenticated = (): boolean => {
  const token = getAuthToken();
  if (!token) return false;

  const payload = decodeJwtPayload(token);
  if (!payload?.exp) {
    clearAuthToken();
    return false;
  }

  const now = Math.floor(Date.now() / 1000);
  if (payload.exp <= now) {
    clearAuthToken();
    return false;
  }

  return true;
};
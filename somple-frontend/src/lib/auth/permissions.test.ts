import { beforeEach, describe, expect, it } from "vite-plus/test";

import { Enum } from "@/api/enums/enum";
import { ANALYTICAL_ROLES, currentRole, currentUser, hasRole } from "@/lib/auth/permissions";

const storage = new Map<string, string>();

Object.defineProperty(globalThis, "localStorage", {
  value: {
    getItem: (key: string) => storage.get(key) ?? null,
    setItem: (key: string, value: string) => storage.set(key, value),
    removeItem: (key: string) => storage.delete(key),
  },
  configurable: true,
});

const tokenFor = (payload: Record<string, unknown>) => {
  const encoded = btoa(JSON.stringify(payload))
    .replace(/=/g, "")
    .replace(/\+/g, "-")
    .replace(/\//g, "_");
  return `header.${encoded}.signature`;
};

describe("frontend permissions", () => {
  beforeEach(() => storage.clear());

  it("reads the current user and role from the existing JWT", () => {
    localStorage.setItem(
      "somple_auth_token",
      tokenFor({ user_id: 3, sub: "operador@somple.com", role: "operator" }),
    );

    expect(currentUser()).toEqual({
      id: 3,
      email: "operador@somple.com",
      role: Enum.UserRole.OPERATOR,
    });
    expect(currentRole()).toBe(Enum.UserRole.OPERATOR);
  });

  it("applies the analytical role matrix", () => {
    localStorage.setItem(
      "somple_auth_token",
      tokenFor({ user_id: 2, sub: "analista@somple.com", role: "analyst" }),
    );
    expect(hasRole(...ANALYTICAL_ROLES)).toBe(true);

    localStorage.setItem(
      "somple_auth_token",
      tokenFor({ user_id: 3, sub: "operador@somple.com", role: "operator" }),
    );
    expect(hasRole(...ANALYTICAL_ROLES)).toBe(false);
  });

  it("rejects missing, malformed, and unknown-role tokens", () => {
    expect(currentUser()).toBeNull();

    localStorage.setItem("somple_auth_token", "invalid");
    expect(currentUser()).toBeNull();

    localStorage.setItem(
      "somple_auth_token",
      tokenFor({ user_id: 4, sub: "visitor@somple.com", role: "visitor" }),
    );
    expect(currentUser()).toBeNull();
  });
});

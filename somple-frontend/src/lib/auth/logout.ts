import type { QueryClient } from "@tanstack/react-query";

import { API_ROUTES } from "@/api/routes";
import { sompleAPI } from "@/lib/config/axios";

import { clearAuthToken } from "./token.storage";

export const logout = async (queryClient?: QueryClient): Promise<void> => {
  try {
    await sompleAPI.post(API_ROUTES.auth.logout);
  } catch {
    // Local cleanup proceeds even if the API call fails.
  } finally {
    clearAuthToken();
    queryClient?.clear();
  }
};

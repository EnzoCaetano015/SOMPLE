import { useMutation, useQueryClient } from "@tanstack/react-query";

import type { Login } from "@/api/models/auth.types";
import { API_ROUTES } from "@/api/routes";
import { logout } from "@/lib/auth/logout";
import { sompleAPI } from "@/lib/config/axios";

export const useLogin = () => {
  return useMutation({
    mutationFn: async (payload: Login.Request) => {
      const { data } = await sompleAPI.post<Login.Response>(API_ROUTES.auth.login, payload);
      return data;
    },
  });
};

export const useLogout = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async () => {
      await logout(queryClient);
    },
  });
};
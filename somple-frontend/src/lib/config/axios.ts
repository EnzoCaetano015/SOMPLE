import axios from "axios";

import { env } from "./env";
import { clearAuthToken, getAuthToken } from "@/lib/auth/token.storage";
import { toast } from "@/lib/toast/toast.utils";

export const sompleAPI = axios.create({
  baseURL: env.apiBaseUrl,
  headers: {
    "Content-Type": "application/json",
  },
});

sompleAPI.interceptors.request.use((config) => {
  const token = getAuthToken();

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

sompleAPI.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      clearAuthToken();
      if (window.location.pathname !== "/login") {
        window.location.assign("/login");
      }
    } else if (error.response?.status === 403) {
      toast.error("Acesso negado", {
        description: "Seu perfil não possui permissão para executar esta ação.",
      });
    }
    return Promise.reject(error);
  },
);

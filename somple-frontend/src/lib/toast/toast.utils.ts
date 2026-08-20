import { toastManager } from "./toast.manager";

type ToastOptions = {
  description?: string;
  timeout?: number;
};

export const toast = {
  success: (title: string, options?: ToastOptions) =>
    toastManager.add({
      title,
      description: options?.description,
      type: "success",
      timeout: options?.timeout ?? 4000,
    }),

  error: (title: string, options?: ToastOptions) =>
    toastManager.add({
      title,
      description: options?.description,
      type: "error",
      timeout: options?.timeout ?? 5000,
    }),

  info: (title: string, options?: ToastOptions) =>
    toastManager.add({
      title,
      description: options?.description,
      type: "info",
      timeout: options?.timeout ?? 4000,
    }),
};

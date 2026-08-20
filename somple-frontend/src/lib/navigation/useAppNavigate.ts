import { useCallback } from "react";
import { useNavigate, type NavigateOptions, type To } from "react-router";

export const useAppNavigate = () => {
  const navigate = useNavigate();

  return useCallback(
    (to: To, options?: NavigateOptions) => {
      void navigate(to, { viewTransition: true, ...options });
    },
    [navigate],
  );
};

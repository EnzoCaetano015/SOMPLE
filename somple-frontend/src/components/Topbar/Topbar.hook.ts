import { useEffect, useState } from "react";

import { useLogout } from "@/api/controllers/auth.controller";
import { useAppNavigate } from "@/lib/navigation/useAppNavigate";
import { toast } from "@/lib/toast/toast.utils";

import { formatLastUpdatedLabel } from "./Topbar.utils";

export const useTopbar = () => {
  const navigate = useAppNavigate();
  const logoutMutation = useLogout();
  const [secondsAgo, setSecondsAgo] = useState(12);

  useEffect(() => {
    const interval = window.setInterval(() => {
      setSecondsAgo((current) => current + 1);
    }, 1000);

    return () => window.clearInterval(interval);
  }, []);

  const handleLogout = () => {
    logoutMutation.mutate(undefined, {
      onSuccess: () => {
        toast.info("Sessão encerrada com sucesso.");
        void navigate("/login");
      },
    });
  };

  return {
    lastUpdatedLabel: formatLastUpdatedLabel(secondsAgo),
    handleLogout,
  };
};

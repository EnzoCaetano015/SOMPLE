import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";

import { useLogin as useLoginMutation } from "@/api/controllers/auth.controller";
import { setAuthToken } from "@/lib/auth/token.storage";
import { useAppNavigate } from "@/lib/navigation/useAppNavigate";
import { toast } from "@/lib/toast/toast.utils";
import type { LoginFormValues } from "./Login.types";
import { loginSchema } from "./Login.utils";

export const useLogin = () => {
  const navigate = useAppNavigate();
  const [error, setError] = useState<string | null>(null);
  const loginMutation = useLoginMutation();

  const form = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = form.handleSubmit((values) => {
    setError(null);
    loginMutation.mutate(values, {
      onSuccess: (response) => {
        setAuthToken(response.access_token);
        toast.success("Login realizado com sucesso!");
        void navigate("/dashboard");
      },
      onError: () => {
        setError("Não foi possível autenticar. Verifique suas credenciais.");
      },
    });
  });

  return {
    form,
    onSubmit,
    isLoading: loginMutation.isPending,
    error,
  };
};

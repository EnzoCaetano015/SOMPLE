import { z } from "zod";

export const loginSchema = z.object({
  email: z.string().email("E-mail inválido"),
  password: z.string().min(6, "Senha deve ter no mínimo 6 caracteres"),
});

export type LoginFormValues = z.infer<typeof loginSchema>;

export const LOGIN_DEFAULT_VALUES: LoginFormValues = {
  email: "operator@exemplo.com.br",
  password: "123456",
};

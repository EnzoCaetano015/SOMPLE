import { Tractor } from "lucide-react";

import { useLogin } from "./Login.hook";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

export const Login = () => {
  const { form, onSubmit, isLoading, error } = useLogin();

  return (
    <main className="flex h-screen">
      <section className="relative hidden h-screen w-[45%] shrink-0 flex-col overflow-hidden bg-somple-corporate px-[clamp(40px,6vw,80px)] py-12 text-somple-white md:flex">
        <div className="login-grid-bg" />
        <div className="pointer-events-none absolute -top-20 -right-20 size-100 rounded-full bg-white/6" />
        <div className="pointer-events-none absolute -bottom-30 -left-15 size-75 rounded-full bg-white/4" />

        <div className="relative z-1 flex items-center gap-3">
          <div className="flex size-10 items-center justify-center rounded-xl bg-white/15">
            <Tractor className="size-5" aria-hidden="true" />
          </div>
          <span className="text-[28px] font-bold tracking-[-0.02em]">SOMPLE</span>
        </div>

        <div className="relative z-1 flex flex-1 flex-col justify-center">
          <h1 className="max-w-[14ch] text-[clamp(28px,3.5vw,42px)] leading-[1.15] font-bold">
            Antecipe riscos.
            <br />
            Proteja operações.
          </h1>
          <p className="mt-5 max-w-[38ch] text-base leading-relaxed text-white/75">
            Monitoramento inteligente de riscos ambientais e operacionais para equipamentos
            agrícolas.
          </p>
        </div>

        <div className="font-mono-num absolute bottom-10 left-[clamp(40px,6vw,80px)] z-1 flex gap-8 text-[11px] tracking-wider text-white/50 uppercase">
          <span>Telemetria ativa</span>
          <span>v2.4.1</span>
          <span>API OK</span>
        </div>
      </section>

      <section className="flex h-screen flex-1 flex-col items-center justify-center bg-somple-bg px-[clamp(32px,5vw,64px)] py-12">
        <div className="w-full max-w-95">
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-somple-ink">Acessar sistema</h2>
            <p className="mt-1.5 text-sm text-somple-muted">
              Entre com suas credenciais para continuar
            </p>
          </div>

          <Form {...form}>
            <form onSubmit={onSubmit}>
              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <FormItem className="mb-5">
                    <FormLabel className="mb-1.5 block text-xs font-semibold tracking-[0.03em] text-somple-muted uppercase">
                      E-mail
                    </FormLabel>
                    <FormControl>
                      <input
                        {...field}
                        type="email"
                        autoComplete="email"
                        placeholder="operator@exemplo.com.br"
                        className="login-input"
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="password"
                render={({ field }) => (
                  <FormItem className="mb-5">
                    <FormLabel className="mb-1.5 block text-xs font-semibold tracking-[0.03em] text-somple-muted uppercase">
                      Senha
                    </FormLabel>
                    <FormControl>
                      <input
                        {...field}
                        type="password"
                        autoComplete="current-password"
                        placeholder="••••••••"
                        className="login-input"
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {error ? <p className="mb-4 text-sm text-destructive">{error}</p> : null}

              <button type="submit" disabled={isLoading} className="login-submit">
                {isLoading ? "Entrando..." : "Entrar"}
              </button>

              <div className="mt-6 text-center">
                <button
                  type="button"
                  className="text-[13px] font-medium text-somple-corporate hover:underline"
                >
                  Esqueceu a senha?
                </button>
              </div>
            </form>
          </Form>
        </div>
      </section>
    </main>
  );
};

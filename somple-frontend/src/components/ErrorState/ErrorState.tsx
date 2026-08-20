import type { ErrorStateProps } from "./ErrorState.types";
import { NEU_BTN } from "@/lib/utils/neumorphic.utils";

export const ErrorState = ({
  title = "Não foi possível carregar os dados.",
  description = "Verifique sua conexão e tente novamente.",
  onRetry,
}: ErrorStateProps) => {
  return (
    <div className="flex flex-col items-center justify-center rounded-neumorphic bg-somple-bg px-6 py-12 text-center shadow-neumorphic-raised">
      <h3 className="text-lg font-semibold text-somple-ink">{title}</h3>
      <p className="mt-2 max-w-md text-sm text-somple-muted">{description}</p>
      {onRetry ? (
        <button type="button" onClick={onRetry} className={`${NEU_BTN} mt-6 px-5 py-2.5`}>
          Tentar novamente
        </button>
      ) : null}
    </div>
  );
};

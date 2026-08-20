import { useEffect, useState } from "react";

type UseDelay = <T>(value: T, delay?: number) => T;

/**
 * Aguarda um intervalo antes de expor o novo valor recebido.
 */
export const useDelay: UseDelay = (value, delay = 500) => {
  const [delayValue, setDelayValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDelayValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [delay, value]);

  return delayValue;
};

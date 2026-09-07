import { useDelay } from "./useDelay";

export const FILTER_DELAY_MS = 500;

type FilterLoadingOptions = {
  isFetchingNextPage?: boolean;
};

const areFilterValuesEqual = <T>(current: T, delayed: T) => {
  if (Object.is(current, delayed)) return true;

  if (
    typeof current === "object" &&
    current !== null &&
    typeof delayed === "object" &&
    delayed !== null
  ) {
    return JSON.stringify(current) === JSON.stringify(delayed);
  }

  return false;
};

/**
 * Aguarda um intervalo antes de expor o valor do filtro para consultas.
 */
export const useDelayedFilter = <T>(value: T, delay = FILTER_DELAY_MS) => {
  const delayedValue = useDelay(value, delay);
  const isDelaying = !areFilterValuesEqual(value, delayedValue);

  return {
    value: delayedValue,
    isDelaying,
  };
};

/**
 * Indica quando a UI deve manter skeletons durante delay ou refetch de filtros.
 */
export const useFilterLoading = (
  isDelaying: boolean,
  isLoading: boolean,
  isFetching: boolean,
  options?: FilterLoadingOptions,
) => {
  const isRefetching = isFetching && !isLoading && !options?.isFetchingNextPage;

  return isDelaying || isLoading || isRefetching;
};

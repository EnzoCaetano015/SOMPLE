import { QueryClient } from "@tanstack/react-query";

export const sompleQueryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 10,
      retry: 1,
      retryOnMount: false,
      refetchOnWindowFocus: false,
    },
  },
});

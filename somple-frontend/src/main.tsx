import { QueryClientProvider } from "@tanstack/react-query";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import App from "./App.tsx";
import { Toaster } from "@/components/Toaster/Toaster";
import { sompleQueryClient } from "@/lib/config/api";
import "./index.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={sompleQueryClient}>
      <Toaster />
      <App />
    </QueryClientProvider>
  </StrictMode>,
);

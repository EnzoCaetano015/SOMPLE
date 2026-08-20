import { Toast } from "@base-ui/react/toast";
import { CircleCheck, CircleX, Info } from "lucide-react";

import { toastManager } from "@/lib/toast/toast.manager";
import { cn } from "@/lib/utils";

const toastTypeStyles = {
  success: "border-somple-field/30 bg-somple-white text-somple-ink",
  error: "border-somple-danger/30 bg-somple-white text-somple-ink",
  info: "border-somple-border bg-somple-white text-somple-ink",
} as const;

const toastIconStyles = {
  success: "text-somple-field",
  error: "text-somple-danger",
  info: "text-somple-muted",
} as const;

const ToastIcon = ({ type }: { type?: string }) => {
  const className = cn("size-4 shrink-0", toastIconStyles[type as keyof typeof toastIconStyles] ?? toastIconStyles.info);

  if (type === "success") return <CircleCheck className={className} aria-hidden="true" />;
  if (type === "error") return <CircleX className={className} aria-hidden="true" />;
  return <Info className={className} aria-hidden="true" />;
};

const ToasterViewport = () => {
  const { toasts } = Toast.useToastManager();

  return (
    <Toast.Portal>
      <Toast.Viewport className="fixed right-4 bottom-4 z-[100] flex w-[min(100vw-2rem,22rem)] flex-col gap-2 outline-none">
        {toasts.map((item) => (
          <Toast.Root
            key={item.id}
            toast={item}
            className={cn(
              "pointer-events-auto flex w-full items-start gap-3 rounded-neumorphic-sm border px-4 py-3 shadow-neumorphic-soft transition-transform",
              toastTypeStyles[item.type as keyof typeof toastTypeStyles] ?? toastTypeStyles.info,
            )}
          >
            <ToastIcon type={item.type} />
            <Toast.Content className="min-w-0 flex-1">
              <Toast.Title className="text-sm font-semibold" />
              <Toast.Description className="mt-0.5 text-xs text-somple-muted" />
            </Toast.Content>
          </Toast.Root>
        ))}
      </Toast.Viewport>
    </Toast.Portal>
  );
};

export const Toaster = () => {
  return (
    <Toast.Provider toastManager={toastManager} limit={4}>
      <ToasterViewport />
    </Toast.Provider>
  );
};

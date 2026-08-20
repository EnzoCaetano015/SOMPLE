import type { TemplatePagesProps } from "./TemplatePages.types";

export const TemplatePages = ({ Icon, title, description }: TemplatePagesProps) => {
  return (
    <main className="flex min-h-screen items-center justify-center bg-somple-surface p-6">
      <div className="max-w-md text-center">
        <Icon className="mx-auto size-12 text-somple-corporate" aria-hidden="true" />
        <h1 className="mt-4 text-2xl font-semibold text-somple-ink">{title}</h1>
        <p className="mt-2 text-sm leading-6 text-muted-foreground">{description}</p>
      </div>
    </main>
  );
};

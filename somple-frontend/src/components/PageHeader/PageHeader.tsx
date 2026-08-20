import type { PageHeaderProps } from "./PageHeader.types";

export const PageHeader = ({ title, subtitle, actions }: PageHeaderProps) => {
  return (
    <div className="mb-7 flex flex-wrap items-start justify-between gap-4">
      <div>
        <h1 className="text-h1 text-somple-ink">{title}</h1>
        {subtitle ? <p className="mt-1 text-sm text-somple-muted">{subtitle}</p> : null}
      </div>
      {actions ? <div className="flex flex-wrap items-center gap-3">{actions}</div> : null}
    </div>
  );
};

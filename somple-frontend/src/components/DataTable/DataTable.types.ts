import type { ReactNode } from "react";

export type DataTableColumn = {
  key: string;
  label: string;
};

export type DataTableRow = {
  id: string;
  cells: Record<string, ReactNode>;
};

export interface DataTableProps {
  columns: DataTableColumn[];
  rows: DataTableRow[];
  onRowClick?: (rowId: string) => void;
}

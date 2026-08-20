import type { DataTableProps } from "./DataTable.types";
import { NeumorphicCard } from "@/components/NeumorphicCard/NeumorphicCard";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { cn } from "@/lib/utils";

export const DataTable = ({ columns, rows, onRowClick }: DataTableProps) => {
  return (
    <NeumorphicCard className="overflow-hidden p-0">
      <Table>
        <TableHeader>
          <TableRow className="border-somple-border/50 hover:bg-transparent">
            {columns.map((column) => (
              <TableHead
                key={column.key}
                className="px-4 py-3 font-mono text-[10px] tracking-wider text-somple-muted uppercase"
              >
                {column.label}
              </TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {rows.map((row) => (
            <TableRow
              key={row.id}
              className={cn(
                "border-somple-border/40 transition-colors hover:bg-black/3",
                onRowClick && "cursor-pointer",
              )}
              onClick={onRowClick ? () => onRowClick(row.id) : undefined}
            >
              {columns.map((column) => (
                <TableCell key={column.key} className="px-4 py-3 text-[13px]">
                  {row.cells[column.key]}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </NeumorphicCard>
  );
};

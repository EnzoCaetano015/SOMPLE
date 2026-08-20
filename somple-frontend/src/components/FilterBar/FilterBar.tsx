import type { FilterBarProps } from "./FilterBar.types";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { NEU_SELECT } from "@/lib/utils/neumorphic.utils";
import { cn } from "@/lib/utils";

export const FilterBar = ({ filters, onFilterChange }: FilterBarProps) => {
  return (
    <div className="flex flex-wrap gap-2.5">
      {filters.map((filter) => (
        <Select
          key={filter.id}
          value={filter.value}
          items={filter.options}
          onValueChange={(value) => {
            if (value) onFilterChange(filter.id, value);
          }}
        >
          <SelectTrigger className={cn("min-w-40", NEU_SELECT)}>
            <SelectValue placeholder={filter.label} />
          </SelectTrigger>
          <SelectContent>
            {filter.options.map((option) => (
              <SelectItem key={option.value} value={option.value}>
                {option.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      ))}
    </div>
  );
};

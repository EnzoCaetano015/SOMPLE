export type FilterOption = {
  value: string;
  label: string;
};

export type FilterDefinition = {
  id: string;
  label: string;
  value: string;
  options: FilterOption[];
};

export interface FilterBarProps {
  filters: FilterDefinition[];
  onFilterChange: (filterId: string, value: string) => void;
}

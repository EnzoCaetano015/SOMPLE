import { Search } from "lucide-react";

import type { SearchInputProps } from "./SearchInput.types";
import { NEU_INPUT } from "@/lib/utils/neumorphic.utils";
import { cn } from "@/lib/utils";

export const SearchInput = ({ value, onValueChange, placeholder, className }: SearchInputProps) => {
  return (
    <div
      className={cn(
        "flex min-w-[280px] items-center gap-2 px-3.5 py-2.5",
        NEU_INPUT,
        className,
      )}
    >
      <Search className="size-3.5 shrink-0 text-somple-muted" aria-hidden="true" />
      <input
        value={value}
        onChange={(event) => onValueChange(event.target.value)}
        placeholder={placeholder}
        aria-label={placeholder}
        className="w-full border-0 bg-transparent text-[13px] text-somple-ink outline-none placeholder:text-[#aaa]"
      />
    </div>
  );
};

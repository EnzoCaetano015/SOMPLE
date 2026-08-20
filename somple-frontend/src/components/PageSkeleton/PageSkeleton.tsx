import { Skeleton } from "@/components/ui/skeleton";
import { NEU_CARD_RAISED } from "@/lib/utils/neumorphic.utils";
import { cn } from "@/lib/utils";

const skeletonCard = cn(NEU_CARD_RAISED, "p-5");

export const DashboardSkeleton = () => {
  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-4 w-72" />
      </div>
      <div className="grid gap-[18px] md:grid-cols-2 xl:grid-cols-4">
        {Array.from({ length: 4 }).map((_, index) => (
          <div key={index} className={cn(skeletonCard, "h-32 p-4")}>
            <Skeleton className="h-full w-full rounded-neumorphic-sm" />
          </div>
        ))}
      </div>
      <div className="grid gap-[22px] xl:grid-cols-[1fr_1.2fr]">
        <div className={cn(skeletonCard, "p-4")}>
          <Skeleton className="h-72 w-full rounded-neumorphic-sm" />
        </div>
        <div className={cn(skeletonCard, "p-4")}>
          <Skeleton className="h-72 w-full rounded-neumorphic-sm" />
        </div>
      </div>
    </div>
  );
};

export const TableSkeleton = () => {
  return (
    <div className={cn(NEU_CARD_RAISED, "overflow-hidden p-0")}>
      <div className="border-b border-somple-border/60 px-6 py-4">
        <Skeleton className="h-5 w-40" />
      </div>
      <div className="space-y-3 p-6">
        {Array.from({ length: 6 }).map((_, index) => (
          <Skeleton key={index} className="h-10 w-full" />
        ))}
      </div>
    </div>
  );
};

export const CardsSkeleton = () => {
  return (
    <div className="grid gap-4.5 sm:grid-cols-1 md:grid-cols-2 xl:grid-cols-3">
      {Array.from({ length: 6 }).map((_, index) => (
        <div key={index} className={skeletonCard}>
          <div className="mb-4 flex items-start justify-between gap-3">
            <Skeleton className="size-10 rounded-[10px] bg-somple-corporate/10 shadow-neumorphic-inset" />
            <Skeleton className="h-6 w-16 rounded-full" />
          </div>
          <Skeleton className="h-4 w-24" />
          <Skeleton className="mt-2 h-4 w-40" />
          <div className="mt-4 h-1.5 w-full overflow-hidden rounded-sm bg-somple-border/90">
            <Skeleton className="h-full w-2/3 rounded-sm shadow-none" />
          </div>
          <Skeleton className="mt-3.5 h-3 w-32 opacity-70" />
        </div>
      ))}
    </div>
  );
};

export const DetailSkeleton = () => {
  return (
    <div className="space-y-6">
      <Skeleton className="h-8 w-56" />
      <div className="grid gap-[22px] xl:grid-cols-[360px_1fr]">
        <div className={cn(skeletonCard, "p-4")}>
          <Skeleton className="h-72 w-full rounded-neumorphic-sm" />
        </div>
        <div className={cn(skeletonCard, "p-4")}>
          <Skeleton className="h-72 w-full rounded-neumorphic-sm" />
        </div>
      </div>
    </div>
  );
};

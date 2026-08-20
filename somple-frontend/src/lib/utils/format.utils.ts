export const formatTimeAgo = (isoDate: string | null | undefined): string => {
  if (!isoDate) return "—";
  const date = new Date(isoDate);
  const diffMs = Date.now() - date.getTime();
  const minutes = Math.floor(diffMs / 60000);
  if (minutes < 1) return "agora";
  if (minutes < 60) return `há ${minutes} min`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `há ${hours} h`;
  const days = Math.floor(hours / 24);
  return `há ${days} d`;
};

export const formatSpeed = (value: number | null | undefined): string =>
  value == null ? "—" : `${value} km/h`;

export const formatPercent = (value: number | null | undefined): string =>
  value == null || !Number.isFinite(value) ? "—" : `${value}%`;

export const formatSharePercent = (value: number, total: number): string => {
  if (!Number.isFinite(value) || !Number.isFinite(total) || total <= 0) {
    return "0%";
  }

  const percent = Math.round((value / total) * 100);
  return Number.isFinite(percent) ? `${percent}%` : "0%";
};

export const formatCount = (value: number | null | undefined): string => {
  if (value == null || !Number.isFinite(value)) return "0";
  return String(value);
};

export const formatRain = (value: number | null | undefined): string =>
  value == null ? "—" : `${value} mm`;

export const formatDateTime = (isoDate: string | null | undefined): string => {
  if (!isoDate) return "—";
  return new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(new Date(isoDate));
};

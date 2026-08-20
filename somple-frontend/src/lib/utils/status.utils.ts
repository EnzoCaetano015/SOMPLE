import { Enum } from "@/api/enums/enum";

export type StatusPresentation = {
  label: string;
  textClass: string;
  bgClass: string;
};

export const ALERT_STATUS_MAP: Record<Enum.AlertStatus, StatusPresentation> = {
  [Enum.AlertStatus.OPEN]: {
    label: "Aberto",
    textClass: "text-somple-danger",
    bgClass: "bg-somple-danger/10",
  },
  [Enum.AlertStatus.ACKNOWLEDGED]: {
    label: "Reconhecido",
    textClass: "text-somple-field",
    bgClass: "bg-somple-field/15",
  },
  [Enum.AlertStatus.RESOLVED]: {
    label: "Resolvido",
    textClass: "text-muted-foreground",
    bgClass: "bg-somple-data",
  },
  [Enum.AlertStatus.DISMISSED]: {
    label: "Dispensado",
    textClass: "text-muted-foreground",
    bgClass: "bg-somple-data",
  },
};

export const EQUIPMENT_STATUS_MAP: Record<Enum.EquipmentStatus, StatusPresentation> = {
  [Enum.EquipmentStatus.ACTIVE]: {
    label: "Ativo",
    textClass: "text-somple-field",
    bgClass: "bg-somple-field/15",
  },
  [Enum.EquipmentStatus.MAINTENANCE]: {
    label: "Manutenção",
    textClass: "text-somple-highlight",
    bgClass: "bg-somple-highlight/20",
  },
  [Enum.EquipmentStatus.INACTIVE]: {
    label: "Inativo",
    textClass: "text-muted-foreground",
    bgClass: "bg-somple-data",
  },
};

export const OPERATION_STATUS_MAP: Record<Enum.OperationStatus, StatusPresentation> = {
  [Enum.OperationStatus.PLANNED]: {
    label: "Planejada",
    textClass: "text-muted-foreground",
    bgClass: "bg-somple-data",
  },
  [Enum.OperationStatus.RUNNING]: {
    label: "Em execução",
    textClass: "text-somple-field",
    bgClass: "bg-somple-field/15",
  },
  [Enum.OperationStatus.PAUSED]: {
    label: "Pausada",
    textClass: "text-somple-highlight",
    bgClass: "bg-somple-highlight/20",
  },
  [Enum.OperationStatus.COMPLETED]: {
    label: "Concluída",
    textClass: "text-muted-foreground",
    bgClass: "bg-somple-data",
  },
  [Enum.OperationStatus.CANCELLED]: {
    label: "Cancelada",
    textClass: "text-muted-foreground",
    bgClass: "bg-somple-data",
  },
};

export const getAlertStatusPresentation = (status: Enum.AlertStatus): StatusPresentation =>
  ALERT_STATUS_MAP[status];

export const getEquipmentStatusPresentation = (status: Enum.EquipmentStatus): StatusPresentation =>
  EQUIPMENT_STATUS_MAP[status];

export const getOperationStatusPresentation = (status: Enum.OperationStatus): StatusPresentation =>
  OPERATION_STATUS_MAP[status];

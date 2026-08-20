export namespace Enum {
  export enum RiskLevel {
    LOW = "low",
    MEDIUM = "medium",
    HIGH = "high",
    CRITICAL = "critical",
  }

  export enum AlertStatus {
    OPEN = "open",
    ACKNOWLEDGED = "acknowledged",
    RESOLVED = "resolved",
    DISMISSED = "dismissed",
  }

  export enum EquipmentStatus {
    ACTIVE = "active",
    MAINTENANCE = "maintenance",
    INACTIVE = "inactive",
  }

  export enum OperationStatus {
    PLANNED = "planned",
    RUNNING = "running",
    PAUSED = "paused",
    COMPLETED = "completed",
    CANCELLED = "cancelled",
  }

  export enum UserRole {
    ADMIN = "admin",
    ANALYST = "analyst",
    OPERATOR = "operator",
  }
}

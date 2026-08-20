import type { Enum } from "@/api/enums/enum";

export namespace Login {
  export type Request = {
    email: string;
    password: string;
  };

  export type Response = {
    access_token: string;
    token_type: string;
    expires_in: number;
    user: {
      id: number;
      name: string;
      email: string;
      role: Enum.UserRole;
    };
  };
}

import { AppLayout } from "@/components/AppLayout/AppLayout";
import { GuestOnly } from "@/components/GuestOnly/GuestOnly";
import { RequireAuth } from "@/components/RequireAuth/RequireAuth";
import { RequireRole } from "@/components/RequireRole/RequireRole";
import { TemplatePages } from "@/components/TemplatePages/TemplatePages";
import { AlertTriangle, CircleQuestionMark, MonitorX } from "lucide-react";
import { createBrowserRouter, Outlet, redirect, RouterProvider } from "react-router";

import { Pages } from "./pages";
import { ANALYTICAL_ROLES } from "@/lib/auth/permissions";

const routes = createBrowserRouter([
  {
    element: <Outlet />,
    errorElement: (
      <TemplatePages
        Icon={MonitorX}
        title="Ops, algo deu errado!"
        description="Parece que houve algum problema, estamos trabalhando para resolver isso!"
      />
    ),
    children: [
      {
        element: <GuestOnly />,
        children: [
          {
            path: "/login",
            element: <Pages.Login />,
          },
        ],
      },
      {
        element: <RequireAuth />,
        children: [
          {
            path: "/maintenance",
            element: (
              <TemplatePages
                Icon={AlertTriangle}
                title="Em Manutenção"
                description="No momento, estamos realizando melhorias na plataforma para oferecer uma experiência ainda melhor para você. Em breve, estaremos de volta."
              />
            ),
          },
          {
            path: "*",
            element: (
              <TemplatePages
                Icon={CircleQuestionMark}
                title="Página não encontrada"
                description="A página que você está procurando não existe ou está indisponível no momento. Verifique a url do site."
              />
            ),
          },
          {
            path: "/",
            element: <AppLayout />,
            children: [
              {
                index: true,
                loader: async () => redirect("dashboard"),
              },
              {
                path: "dashboard",
                element: <Pages.Dashboard />,
              },
              {
                path: "monitoring",
                element: <Pages.Monitoring />,
              },
              {
                path: "equipment",
                element: <Pages.Equipment />,
              },
              {
                path: "equipment/:equipmentId",
                element: <Pages.EquipmentDetail />,
              },
              {
                path: "operations",
                element: <Pages.Operations />,
              },
              {
                path: "alerts",
                element: <Pages.Alerts />,
              },
              {
                element: <RequireRole allowedRoles={ANALYTICAL_ROLES} />,
                children: [
                  {
                    path: "assessment/:assessmentId",
                    element: <Pages.Assessment />,
                  },
                  {
                    path: "audit",
                    element: <Pages.Audit />,
                  },
                ],
              },
            ],
          },
        ],
      },
    ],
  },
]);

const Routes = () => {
  return <RouterProvider router={routes} />;
};

export default Routes;

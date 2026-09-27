# Segurança, acesso e rastreabilidade

| Recurso | Público | Admin | Analyst | Operator |
| --- | --- | --- | --- | --- |
| Health, readiness e login | Sim | Sim | Sim | Sim |
| Dashboard, filtros, equipamentos, operações, monitoramento e alertas | Não | Sim | Sim | Sim |
| Envio de telemetria | Não | Sim | Não | Sim |
| Assessment detalhado e auditoria | Não | Sim | Sim | Não |
| Alteração de status de alerta | Não | Sim | Sim | Não |
| Logout | Não | Sim | Sim | Sim |

Senhas, hashes, JWT e secrets não são persistidos em `audit_logs`. Login inválido registra somente e-mail normalizado e motivo genérico. Cada request recebe um request ID; assessments guardam leitura, versão do modelo, features, score, nível, probabilidades, método e versão da política.

Limitações conhecidas: logout sem revogação server-side, HTTP na implantação acadêmica AWS e ausência de gestão avançada de sessão. Essas limitações são explícitas e não são apresentadas como controles de produção.

# Evidências do projeto

As evidências desta pasta são produzidas somente por execuções reais. Cada subpasta registra cenário, ambiente, comando e resultado. Tokens, senhas e secrets devem ser removidos das capturas e logs.

| Pasta | Conteúdo |
| --- | --- |
| `qualidade-dados` | validações, duplicidade e atomicidade |
| `modelo` | treinamento, metadata, métricas e integridade |
| `score-alertas` | fronteiras da política e exemplos de alerta |
| `dashboard-relatorios` | dashboard e filtros reais |
| `testes` | suítes, build e validação do MVP |
| `seguranca` | 401, 403, acesso permitido e auditoria |
| `fluxo-ponta-a-ponta` | sequência completa executada |
| `funcional` | capturas funcionais da aplicação |
| `aws` | evidências da implantação acadêmica |

Ambiente de validação: Windows, Docker Desktop, PostgreSQL 16, Python 3.14.7 e Node/Vite+ conforme os manifests do repositório. Data: 26/09/2026. A execução limpa usou `docker-compose.validation.yml`, com volume e portas isolados. O relatório consolidado está em `docs/VALIDATION.md`.

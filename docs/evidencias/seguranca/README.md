# Segurança e rastreabilidade

- Health, readiness e login permaneceram públicos.
- Dashboard e `dashboard/filter-options` exigem autenticação e preservam os papéis atuais.
- Testes cobrem `401`, `403`, acesso permitido, request ID e auditoria.
- O pipeline usa transação única e não inclui detalhes internos do banco nos erros de duplicidade.
- Logs inspecionados não exibiram senha ou token.
- A chave JWT padrão do ambiente local gera aviso de comprimento e permanece explicitamente limitada ao desenvolvimento; produção deve fornecer segredo forte e HTTPS.

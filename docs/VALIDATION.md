# Relatório de validação do projeto

Data: 26/09/2026.

## Resultado executivo

| Requisito | Status | Evidência objetiva |
| --- | --- | --- |
| Domínios, idempotência e rollback | ATENDE | migration 005 e testes de API, concorrência e rollback |
| Treinamento e modelo 1.1.0 | ATENDE | artefato, metadata, relatórios, migration 006 e SHA conferido |
| Política única de risco | ATENDE | testes de fronteira, snapshot completo e alertas somente alto/crítico |
| Dashboard e filtros consistentes | ATENDE | testes de filtros e inspeção visual dos três recortes operacionais |
| Confiabilidade e validação integrada | ATENDE | 81 testes backend, 6 frontend, build e validador HTTP aprovados |
| Segurança e matriz de acesso | ATENDE | matriz RBAC, testes 401/403, auditoria e request ID |
| Execução e evidências | ATENDE PARCIALMENTE | stack limpa aprovada e evidências textuais reais; captura binária ainda não anexada |
| Arquitetura | ATENDE | componentes e sequência Mermaid refletem o código existente |
| Documentação consolidada | ATENDE | arquitetura, métricas, segurança, execução e limitações documentadas |
| Roteiro de vídeo | ATENDE | roteiro de até cinco minutos e placeholder explícito criados, sem gravação ou URL inventada |
| Relatório final | ATENDE | este documento classifica requisitos com evidência objetiva |

## Critérios técnicos

- **Dados e modelo — ATENDE:** validações, duplicidade `409`, rollback, treino reproduzível, SHA, carregamento e fronteiras aprovados.
- **Aplicação — ATENDE:** filtros isolados e combinados, relatório, estado vazio, RBAC, auditoria e build aprovados.
- **Entrega — ATENDE PARCIALMENTE:** ambiente recriado do zero e documentação concluída; a captura exportada ainda depende de inclusão no repositório.

## Limitações verificadas

- Dataset acadêmico simulado de 180 registros, com apenas dois exemplos da classe `low`; não representa desempenho de produção.
- Segredo JWT padrão e HTTP são exclusivos do ambiente local. Revogação de token e HTTPS de produção não fazem parte do escopo.
- O build frontend mantém warning não bloqueante de chunk acima de 500 kB.
- Os quatro warnings de Fast Refresh já existiam no baseline e permaneceram sem erros de lint ou tipos.

## Conclusão

Os requisitos implementáveis por código e execução automatizada foram validados. Para encerrar integralmente o pacote de evidências, ainda é necessário anexar ao repositório uma captura exportada. A gravação/publicação do vídeo é uma etapa humana posterior já preparada pelo roteiro e pelo placeholder exigidos.

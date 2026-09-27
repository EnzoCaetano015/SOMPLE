# Testes e build

Execução final em 26/09/2026:

| Comando | Resultado |
| --- | --- |
| `.venv\\Scripts\\python.exe -m pytest` | 81 passed, 2 warnings de depreciação |
| `vp check` | 0 erros, 4 warnings preexistentes de Fast Refresh |
| `vp test` | 2 arquivos e 6 testes aprovados |
| `vp run build` | build aprovado; warning não bloqueante de chunk acima de 500 kB |
| `python -m scripts.validate_mvp` na stack limpa | 10 checks `PASS` |

O frontend também foi reconstruído em Docker. A revisão de boas práticas React confirmou uso das query keys filtradas, dados derivados memoizados e ausência de novos efeitos para sincronização de estado.

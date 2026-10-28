| Módulo | Ações que existem | Equipe · Transcrição | Equipe · Processamento (parceiro) | Equipe · Assistente de análise | Cliente Empresa | Participante |
| --- | --- | --- | --- | --- | --- | --- |
| Pesquisas | Visualizar, Criar, Editar, Excluir, Importar, Exportar | — | — | — | — | visualizar |
| Projetos | Visualizar, Criar, Editar, Excluir | — | — | — | visualizar | — |
| Convites | Visualizar, Gerenciar convites | — | — | — | — | — |
| Cadastros | Visualizar, Criar, Editar, Excluir, Exportar, Dados detalhados | — | — | — | — | — |
| Resultados | Consultar resultados, Dados detalhados, Exportar | — | — | consultar resultados, dados detalhados, exportar | consultar resultados | — |
| Reuniões | Visualizar, Criar, Editar, Excluir | visualizar | visualizar | visualizar | — | visualizar |
| Transcrições | Visualizar, Importar, Editar, Excluir, Exportar | visualizar, importar, editar | visualizar, editar | visualizar, editar, exportar | — | — |
| Usuários | Gerenciar usuários | — | — | — | — | — |
| Integrações | Administrar integrações | — | — | — | — | — |

Desde 28/10/2026 esta matriz é **só leitura**: ela está no código (`POLITICAS`) e muda por revisão de código (pull request). A tela **Usuários e acessos → Arquitetura de acessos** mostra a matriz e explica cada decisão. O acesso de cada pessoa vem dos **vínculos** da conta (função, empresa, código, nomeação de administrador aprovada), não de caixas marcadas por usuário. Detalhes em [ACESSOS.md](ACESSOS.md).

## Onde a regra é aplicada

| Camada | No protótipo | Em produção (pendente) |
| --- | --- | --- |
| Interface | Menus, abas e botões só aparecem com a permissão (`pode(módulo, ação)`) | Igual |
| Rota | O roteador confere sessão, perfil e matriz antes de abrir qualquer tela (`guard`) | Igual, mais checagem no servidor ao carregar dados |
| Ação | Toda ação que altera dados passa por `exigir(módulo, ação)`, mesmo se o botão for criado à mão no navegador | **Backend obrigatório**: o protótipo roda inteiro no navegador, então quem controla o navegador controla os dados dele. A mesma matriz precisa ser aplicada na API (E.5) |
| Dados | Respostas detalhadas só por código, sem nome/e-mail; cliente vê só a própria empresa | Filtrar no servidor, nunca no navegador |

## Comportamentos definidos (E.7)

| Situação | O que acontece |
| --- | --- |
| Sem login abre uma área interna | Vai para o login com o aviso "Entre com sua conta para acessar essa página" |
| Logado abre área de outro perfil (endereço digitado ou link) | Página **Acesso negado (403)** com o motivo; a tentativa é registrada |
| Clica num botão sem permissão (forjado) | Nada muda; aviso "Acesso negado"; tentativa registrada |
| Sessão parada há mais de 30 minutos | Sessão encerrada; login com o aviso "Sua sessão expirou" |
| Conta sem nenhum perfil | Login recusado |
| Dados do navegador adulterados para virar administrador | `admin`, `perms`, `empresa` e a matriz gravada são ignorados: o acesso é recalculado pelos vínculos a cada leitura; a rota é negada e registrada |
| Conta suspensa ou vínculo revogado com sessão aberta | Perde o acesso na próxima tela ou ação (R11) |
| Vínculo em convite, revisão ou vencido | Não dá acesso; o login explica o que falta |

O registro fica em **Usuários e acessos → Auditoria**, junto com as alterações de acesso (quem, quando, motivo), guardado no navegador neste protótipo.

## Testes

`tests/test_acessos.py` cobre a refatoração de 28/10/2026 (vínculos, isolamento, revogação, múltiplos vínculos, auditoria, estados). `tests/test_autorizacao.py` cobre: escalada pelo `localStorage`, rota direta sem permissão, acesso sem login, sessão expirada, ações forjadas (excluir pesquisa, remover usuário, avançar etapa de outra função), matriz só leitura (adulterar a cópia gravada não muda nada) e cliente sem dados individuais.

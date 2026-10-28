# Permissões por perfil

Matriz atualizada pela implementação do Prompt Master V2 (28/10/2026, RF01–RF03). **\*** = exclusivo do administrador (`SO_ADMIN`): nenhuma política de outro perfil consegue ganhar essa ação.

| Módulo | Ações que existem | Administrador | Equipe · Transcrição | Equipe · Processamento (parceiro) | Equipe · Assistente de análise | Cliente Empresa | Participante | Agente terceirizado (V2) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Pesquisas | Visualizar, Criar, Editar, Excluir, Importar, Exportar, Enviar para revisão, Revisar e aprovar\*, Publicar\*, Enviar arquivos | todas | — | — | — | — | visualizar | criar, editar, enviar para revisão, enviar arquivos (só as próprias, só em rascunho ou devolvida) |
| Projetos | Visualizar, Criar, Editar, Excluir | todas | — | — | — | visualizar | — | — |
| Convites | Visualizar, Gerenciar convites | todas | — | — | — | — | — | — |
| Cadastros | Visualizar, Criar, Editar, Excluir, Exportar, Dados detalhados | todas | — | — | — | — | — | — |
| Resultados | Consultar resultados, Dados detalhados, Exportar, Solicitar acesso, Liberar resultados ao cliente\* | consultar, dados detalhados, exportar, liberar | — | — | consultar, dados detalhados, exportar | consultar **só o que foi liberado**, solicitar acesso | — | — |
| Reuniões | Visualizar, Criar, Editar, Excluir | todas | visualizar | visualizar | visualizar | — | visualizar | — |
| Transcrições | Visualizar, Importar, Editar, Excluir, Exportar | todas | visualizar, importar, editar | visualizar, editar | visualizar, editar, exportar | — | — | — |
| Usuários | Gerenciar usuários\* (inclui gerar e desativar login de agente) | sim | — | — | — | — | — | — |
| Integrações | Administrar integrações\* | sim | — | — | — | — | — | — |
| Audiovisual confidencial (V2) | Ver registro\*, Autorizar acesso individual\*, Assistir com autorização | ver registro, autorizar (**só o responsável** configurado) | — | — | — | — | assistir, **só com autorização individual válida**, no celular, depois do check-in | — |

Por categoria de resultado (RF01):

| Categoria | Quem acessa | Situação |
| --- | --- | --- |
| Resultados consolidados | Administrador, Assistente de análise; Cliente só das pesquisas liberadas após pedido | Matriz provisória (DP-01); regra do cliente definida pela Sinergia em 28/10 |
| Respostas individuais (por código, sem nome nem e-mail) | Administrador, Assistente de análise | Provisório (DP-01) |
| Comentários e insights de focus group | Administrador, Assistente de análise; Cliente só de projetos com todas as pesquisas publicadas liberadas | Provisório (DP-01) |
| Relatórios e exportação | Administrador, Assistente de análise | Provisório (DP-01) |
| Próprias respostas | Participante (só as dele) | Mantido até a decisão DP-13 |
| Qualquer categoria | Participante e agente: **nunca** | Requisito confirmado |

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

## V2 (28/10/2026): o que mudou nas regras

| Situação | O que acontece |
| --- | --- |
| Participante ou agente abre qualquer tela de resultados | Página 403, sem nome de pesquisa nem número; tentativa registrada |
| Cliente sem liberação abre Resultados | Vê só o pedido de acesso (todas as pesquisas contratadas ou uma); nenhum número |
| Cliente com liberação | Vê o agregado só das pesquisas liberadas; "todas" vale para as publicadas no momento da aprovação |
| Agente abre pesquisa de outro autor | "Esta pesquisa não existe ou não é sua"; tentativa registrada |
| Login de agente desativado com sessão aberta | Perde o acesso no próximo clique; histórico intacto |
| Pesquisa de agente | Só vai ao ar com revisão humana e publicação pelo administrador; o formulário antigo não muda a situação dela |
| Acesso interno (administrador) | Link discreto no rodapé; conta sem nomeação é recusada e registrada |

## Testes

`tests/test_acessos.py` cobre a refatoração de 28/10/2026 (vínculos, isolamento, revogação, múltiplos vínculos, auditoria, estados). `tests/test_autorizacao.py` cobre: escalada pelo `localStorage`, rota direta sem permissão, acesso sem login, sessão expirada, ações forjadas (excluir pesquisa, remover usuário, avançar etapa de outra função), matriz só leitura (adulterar a cópia gravada não muda nada) e cliente sem dados individuais. Os arquivos `tests/test_v2_*.py` cobrem RF01–RF05 (ver [REFATORACAO-V2.md](REFATORACAO-V2.md)).

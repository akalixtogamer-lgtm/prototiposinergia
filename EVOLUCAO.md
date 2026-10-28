# Evolução de 27/10/2026 — relatório (módulos A a E)

Evolução do sistema existente a partir do "Prompt master — evolução e reestruturação". Nada foi reescrito do zero: as telas, dados e etiquetas S1–S5 continuam, e a versão anterior pode ser restaurada (ver [REVERSAO.md](REVERSAO.md)).

## Decisões tomadas com a Sinergia antes de começar

| Tema | Resposta |
| --- | --- |
| Reuniões | Só link externo (Teams ou Meet). A sala própria com vídeo e chat simulados saiu; o material protegido continua na Sinergia |
| Documentos do projeto | Briefing do cliente, Termo de confidencialidade, Proposta ou contrato, Questionário ou roteiro. Nenhum obrigatório por padrão; a obrigatoriedade é configurável |
| Dispositivo usado | Próprio · Cedido pela Sinergia · Cedido pelo local de aplicação · Não informado |
| SurveyMonkey | Link + importação de arquivo. Sem API |

## Diagnóstico do que existia

- Importação de pesquisas aparecia em três lugares (Projetos, Projeto e Resultados).
- Convites sem detalhe nem histórico; projeto com aba "Arquivos" genérica.
- Cadastros sem paginação, sem seleção e sem filtros por região/projeto/idade/sexo.
- Focus group com "sala ao vivo" que simulava vídeo, chat e transcrição.
- Permissões em lista de capacidades por perfil, aplicadas só a menus; a área do administrador conferia apenas o modo da sessão no navegador, permitindo escalada por adulteração do `localStorage` (achado da auditoria anterior).

## O que mudou

| Módulo | Mudança |
| --- | --- |
| A | Botão **Importar** só em Pesquisas (pesquisas por CSV e respostas por CSV); aba **Importações**; link do SurveyMonkey validado e aberto em nova aba; Resultados com aba **Respostas detalhadas** (por código, com filtros, paginação, exportação e estados vazio/erro) para quem tem permissão; Resultados também para a assistente de análise |
| B | Aba **Documentos** no projeto (4 tipos, nenhum obrigatório, configurável); validação na criação do projeto quando algum for marcado como obrigatório; convites com **Detalhes**, edição, ciclo de vida e histórico de cada ação |
| C | Participantes com paginação (10 por página), busca, filtros por região, projeto, sexo, faixa de idade e tipo de pesquisa, ordenação; seleção individual, da página e de todo o conjunto filtrado com contagem explícita; convite em massa com confirmação do número; exportação CSV; idade e sexo informados no cadastro, sem classificação automática, visíveis só com "dados detalhados"; **dispositivo usado** pedido na revisão do participante e aceito na importação |
| D | Reuniões só por link do Teams/Meet (formato validado); apresentação protegida sem vídeo e sem chat; transcrição ao vivo marcada como **indisponível**; transcrição entra por arquivo `.vtt`/`.txt` ou texto colado (nada é gerado); consentimento de gravação/transcrição junto do termo de sigilo; exclusão da transcrição; retenção configurável ("A definir") |
| E | Matriz **módulo × ação** por perfil (6 perfis, 9 módulos, 11 ações); checagem central antes de cada ação que altera dados (também para botões forjados); página **403**; sessão expira após 30 min sem uso; conta precisa ser administradora para a área do administrador; "Gerenciar usuários" e "Administrar integrações" exclusivos do administrador; registro de **acessos negados** |

Correção extra encontrada nos testes: uma expressão regular com caracteres acentuados literais quebrava o script inteiro quando o arquivo era servido sem `charset`. Agora usa `̀-ͯ` e o `index.html` declara `<meta charset="utf-8">`.

## Arquivos modificados no repositório

| Arquivo | O que é |
| --- | --- |
| `index.html` | Site e sistema (HTML, CSS e JS num arquivo) |
| `README.md` | Estrutura, permissões, evolução e como rodar os testes |
| `SOLICITACOES.md` | Mapa das etiquetas ▶ INÍCIO / ◆ MEIO / ■ FIM, regenerado (78 etiquetas) |
| `EVOLUCAO.md` | Este relatório |
| `PERMISSOES.md` | Perfis, matriz padrão e comportamento de rotas, sessão e auditoria |
| `INTEGRACOES.md` | SurveyMonkey, Teams/Meet e transcrição: o que existe e como ativar |
| `REVERSAO.md` | Plano de reversão |
| `tests/` | `conftest.py`, `test_funcional.py`, `test_autorizacao.py`, `test_integracoes.py`, `test_regressao.py` |
| `.gitignore` | Ignora caches do Python |

## Testes executados

Comando: `pytest -q tests` (Chromium headless via Playwright). Resultado da última execução: **30 de 30 aprovados**.

| Grupo | Testes | O que cobre |
| --- | --- | --- |
| Funcional | 12 | Importação só em Pesquisas, importação válida e inválida, respostas detalhadas filtradas sem e-mail, documentos opcionais e obrigatoriedade configurável, ciclo e histórico do convite, paginação, seleção da página e do conjunto filtrado, convite em massa, limpeza da seleção ao filtrar, filtro por projeto, dispositivo obrigatório no envio, link de reunião válido/inválido, ausência de chat e vídeo, transcrição só por arquivo |
| Autorização | 9 | Escalada pelo `localStorage`, rota direta sem permissão, acesso sem login, sessão expirada, ações forjadas, matriz adulterada, matriz alterada pelo administrador, função da equipe fora da própria etapa, cliente sem dados individuais |
| Integrações | 4 | Validação do link do SurveyMonkey e abertura em nova aba, formatos aceitos de Teams/Meet, tela de integrações declarando o que não existe, varredura de credenciais no repositório |
| Regressão | 5 | Todas as telas e abas de 6 perfis sem erro de JavaScript, agente continua sem login, marca d'água do material protegido, site público atualizado, etiquetas de início e fim pareadas |

Limite: os testes rodam no navegador contra o protótipo estático. Não há testes de servidor porque não existe servidor.

## Status por requisito

| Req. | Requisito | Status | Observação |
| --- | --- | --- | --- |
| A.1 | Importação centralizada em Pesquisas | Validado | Testes automatizados; falta aceite da Sinergia |
| A.2 | Importar respostas por arquivo | Validado | CSV lido; XLSX e PDF guardados sem leitura (limitação declarada) |
| A.3 | Resultados por perfil, agregados e detalhados, filtros, estados | Validado | |
| A.4 | Link externo do SurveyMonkey | Validado | Links de exemplo: trocar pelos reais |
| A.4b | Sincronização pela API do SurveyMonkey | Não implementado, com justificativa | Fora do escopo aprovado; exige conta com API e servidor |
| B.1 | Projetos separados de convites | Validado | |
| B.2 | Criar, editar e acompanhar convites | Validado | |
| B.3 | Documentos do projeto | Validado | 4 tipos definidos pela Sinergia |
| B.4 | Obrigatoriedade sem confirmação | Validado | Quais serão obrigatórios: decisão pendente (D-01) |
| B.5 | Ciclo de vida e histórico do convite | Validado | |
| C.1 | Paginação | Validado | |
| C.2 | Filtros por região e projeto | Validado | |
| C.3 | Seleção individual e múltipla | Validado | |
| C.4 | Página × conjunto filtrado, contagem e confirmação | Validado | |
| C.5 | Idade e sexo sem classificação automática | Validado | Faixas e opções a confirmar (D-07) |
| C.6 | Dispositivo usado | Validado | |
| C.7 | LGPD (dados por código, só com permissão) | Implementado, aguardando testes | Falta revisão jurídica e política de retenção |
| D.1 | Teams/Meet por link | Validado | |
| D.2 | Redirecionamento × integração | Validado | Tela Integrações e INTEGRACOES.md |
| D.3 | Transcrição sem simulação | Validado | Importação de `.vtt`/`.txt` ou texto |
| D.3b | Transcrição ao vivo | Não implementado, com justificativa | Sem serviço de captura e reconhecimento de fala |
| D.4 | Consentimento de gravação/transcrição | Implementado, aguardando testes | Sem teste automatizado específico |
| D.5 | Retenção e exclusão | Bloqueado por decisão | Exclusão existe; prazo de retenção pendente (D-03) |
| E.1 | Perfis | Bloqueado por decisão | Proposta a validar (D-02) |
| E.2 | Matriz módulo × ação | Validado | |
| E.3 | Aplicação na interface | Validado | |
| E.4 | Matriz padrão | Bloqueado por decisão | Proposta a validar (D-02) |
| E.5 | Aplicação no backend e na API | Não implementado, com justificativa | Não há backend; a checagem central roda no navegador (D-06) |
| E.6 | Impedir escalada de privilégio | Validado | No navegador; em produção depende do servidor |
| E.7 | Sem permissão, sessão expirada, rota direta | Validado | Tempo de sessão a confirmar (D-08) |
| E.8 | Registro de acessos negados | Validado | Guardado no navegador |

## Decisões pendentes

| Código | Decisão |
| --- | --- |
| D-01 | Quais documentos do projeto serão obrigatórios |
| D-02 | Validar perfis e matriz padrão de permissões |
| D-03 | Prazo de retenção das transcrições (LGPD) |
| D-04 | Sincronizar respostas pela API do SurveyMonkey |
| D-05 | Integrar Teams/Meet (criar reunião, ler gravação, transcrição automática) |
| D-06 | Backend para aplicar a matriz no servidor |
| D-07 | Faixas de idade e opções de sexo do cadastro |
| D-08 | Tempo de expiração da sessão |

## Figma

Arquivo "Sinergia — Protótipo Consolidado", página Protótipo, seção **"Evolução 27/10/2026 · módulos A–E (prompt master)"**:

- 19 telas e modais: EV-A1, EV-A2a/b, EV-A3, EV-B1–B4, EV-C1–C3, EV-D1–D4, EV-E1–E4.
- EV-00 Mapa de navegação, EV-90 Decisões pendentes, EV-91 Requisitos × telas × status, EV-92 Estados.
- Componente novo **Estado** (página Componentes) com 6 variantes: Carregando, Vazio, Sucesso, Erro, Desabilitado, Acesso negado.
- Menus laterais atualizados nos componentes: Administrador ("Reuniões" e "Integrações") e Equipe interna ("Reuniões" e "Resultados"). A mudança aparece também nas telas antigas que usam esses menus.
- Protótipo clicável: fluxo "Evolução 27/10/2026" com 68 interações (menus, aberturas de modal e fechamento).
- Telas antigas substituídas (sala ao vivo, lista e agendamento de focus group, projetos com importação, modal de importação antigo) receberam uma faixa vermelha "ALTERADA em 27/10/2026", mantidas como histórico.

## Validação e reversão

- Validação: rodar `pytest -q tests` e percorrer o fluxo "Evolução 27/10/2026" no Figma.
- Reversão: branch `reversao-pre-evolucao` (commit `87d64a1`); passos em [REVERSAO.md](REVERSAO.md).

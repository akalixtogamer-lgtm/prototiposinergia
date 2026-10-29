# Solicitações da cliente — mapa das etiquetas

Relatório de solicitações recebido em 21/10/2026 (4 áudios da cliente). Cada alteração ficou marcada no código, nas telas e no Figma com três etiquetas:

- **▶ INÍCIO** — onde a alteração começa
- **◆ MEIO** — o miolo (o que aquele trecho faz)
- **■ FIM** — onde a alteração termina

| Código | Solicitação | Onde aparece no sistema | Telas no Figma |
| --- | --- | --- | --- |
| S1 | Proteção anti-vazamento (DRM) | Material protegido dentro da sala: marca d'água individual, pausa fora da tela, bloqueio de captura, impressão e clique direito, registro de acesso | FG-ADM-03 Materiais e registro, FG-SALA-01/02, FG-SALA-03 Proteção em ação |
| S2 | Ambiente de focus group (chat de vídeo) | `#adm-focus`, `#adm-sala`, `#pa-focus`, `#pa-sala`, `#eq-focus`, `#eq-sala`, página pública `#focusgroup` | FG-ADM-01 Lista, FG-ADM-02 Agendar, FG-PA-01 Debates, FG-PA-02 Termo de sigilo, FG-SALA-01/02, Site · Focus group online |
| S3 | Apresentação de materiais no chat | Controles da moderação na sala (`#adm-sala`) | FG-SALA-01 |
| S4 | Integração com as ferramentas | Aba Focus group no projeto, esteira `#eq-transcricoes`, insights em `#cl-resultados` e `#cl-resultado` | FG-EQ-01 Esteira, FG-CL-01 Insights do cliente |
| S5 | Controle de acesso rigoroso | Login recusa entrevistadores; área do Agente desativada; perfil Equipe interna; Usuários e Cadastros | FG-LOGIN-01, A8 (MEIO), A7 (FIM), seção Agente marcada como desativada |

No Figma, tudo está na seção "Solicitações da cliente · relatório 21/10/2026 (S1–S5)" da página Protótipo, com o componente Etiqueta de solicitação (Etapa = INÍCIO, MEIO ou FIM).

Etapas do fluxo mostradas nas telas: **1 · INÍCIO** agendar e convidar → **2 · MEIO** sala ao vivo → **3 · FIM** transcrição e análise.

## Evolução de 27/10/2026 (prompt master, módulos A–E)

As etiquetas dos requisitos novos usam o código do prompt: **A.1–A.4** pesquisas e resultados, **B.1–B.5** projetos, documentos e convites, **C.1–C.7** cadastros, **C.6** dispositivo, **D.1–D.5** reuniões e transcrição, **E.1–E.8** permissões. Detalhes e status em EVOLUCAO.md.

## Prompt Master V2 · implementação de 28/10/2026 (RF01–RF05)

Os requisitos da V2 usam o código do prompt: **RF01** resultados protegidos, **RF02** audiovisual confidencial, **RF03** agente terceirizado (substitui a S5), **RF04** escopo sem política, **RF05** página inicial. No `index.html`, o bloco "V2 · PROMPT MASTER V2" fica antes do roteador, com etiquetas por RF; as edições em código existente levam o comentário `RF0x (V2)`. Nas telas, o selo de solicitação mostra o código (ex.: RF01 · Resultados protegidos). Detalhes em [REFATORACAO-V2.md](REFATORACAO-V2.md).

## Etiquetas no `index.html` (linha · etiqueta · trecho)

Tabela gerada a partir do arquivo em 28/10/2026 (V2).

| Linha | Etiqueta | Trecho |
| --- | --- | --- |
| 287 | ▶ INÍCIO | V2 · RF05 (acesso), RF02 (exibição) · estilos |
| 299 | ■ FIM | V2 · estilos |
| 454 | ▶ INÍCIO | S2 (site) · estilos da página Focus group online |
| 461 | ■ FIM | S2 (site) · estilos |
| 488 | ▶ INÍCIO | S1–S5 · estilos das solicitações da cliente (relatório de 21/10/2026) |
| 549 | ■ FIM | S1–S5 · estilos |
| 550 | ▶ INÍCIO | evolução 27/10/2026 · paginação, seleção em massa, ciclo do convite, importação |
| 563 | ■ FIM | evolução 27/10/2026 |
| 680 | ▶ INÍCIO | S2 (site) · chamada da home para o focus group online |
| 682 | ■ FIM | S2 (site) · chamada da home |
| 699 | ▶ INÍCIO | S2 (site) · destaque do focus group em Serviços |
| 699 | ■ FIM | S2 (site) · destaque |
| 722 | ▶ INÍCIO | S2 (site público) · página "Focus group online" — solicitação da cliente (relatório de 21/10/2026) |
| 728 | ◆ MEIO | S2 (site) · as três etapas do fluxo |
| 735 | ◆ MEIO | S1/S5 (site) · proteção e controle de acesso |
| 744 | ■ FIM | S2 (site público) · página "Focus group online" |
| 798 | ▶ INÍCIO | / ◆ MEIO / ■ FIM. |
| 803 | ▶ INÍCIO | C.1–C.6, B.3, A.3, A.4, E · dados de exemplo novos (sobre o seed anterior). Fictícios, só para o protótipo. |
| 837 | ■ FIM | dados de exemplo novos |
| 839 | ▶ INÍCIO | E.1–E.4, E.8 · perfis, módulos, ações e matriz padrão (proposta para validar com a Sinergia) |
| 845 | ▶ INÍCIO | RF01/RF02/RF03 (V2) · políticas: admin sem "assistir" e sem "solicitar"; cliente solicita resultados; participante e agente sem nenhuma ação de resultado |
| 854 | ■ FIM | RF01/RF02/RF03 (V2) · políticas |
| 855 | ◆ MEIO | E.1–E.4 · perfis e matriz padrão continuam abaixo (sys4-evol.js) |
| 860 | ▶ INÍCIO | Sx   onde a alteração começa |
| 861 | ◆ MEIO | Sx     o miolo (o que aquele pedaço faz) |
| 862 | ■ FIM | Sx      onde a alteração termina |
| 894 | ▶ INÍCIO | S5 · contas: agentes (entrevistadores terceirizados) perdem o login; entram 3 perfis da equipe interna |
| 899 | ◆ MEIO | S5 · equipe interna: transcrição, processamento (parceiro) e assistentes de análise |
| 907 | ■ FIM | S5 · contas |
| 970 | ▶ INÍCIO | S2/S5 · permissões novas: focus group e esteira da equipe interna (agente saiu da matriz) |
| 972 | ■ FIM | S2/S5 · permissões novas |
| 977 | ▶ INÍCIO | S2/S3/S4 · dados de exemplo do focus group (sessões, materiais protegidos e esteira de transcrição) |
| 985 | ◆ MEIO | S2 · uma sessão em cada etapa: Início (agendada), Meio (ao vivo) e Fim (encerrada, na esteira) |
| 999 | ■ FIM | S2/S3/S4 · dados de exemplo |
| 1042 | ▶ INÍCIO | S5 · perfis: "Agente" sai; "Equipe interna" entra (função: transcrição, processamento ou análise) |
| 1049 | ■ FIM | S5 · perfis |
| 1062 | ▶ INÍCIO | E.2 · as capacidades antigas dos menus agora consultam a matriz módulo × ação (sys4-evol.js) |
| 1065 | ■ FIM | E.2 |
| 1071 | ▶ INÍCIO | E.7 · sessão expirada, rota sem permissão e acesso direto: comportamento definido |
| 1080 | ■ FIM | E.7 |
| 1112 | ▶ INÍCIO | R · resultados por pesquisa (28/10/2026): cada tipo de estudo tem as próprias perguntas, n, margem e leitura |
| 1255 | ■ FIM | R · resultados por pesquisa |
| 1281 | ▶ INÍCIO | S5 · login recusado para entrevistadores e terceirizados |
| 1284 | ■ FIM | S5 · login recusado |
| 1425 | ▶ INÍCIO | S5 Controle de acesso rigoroso · solicitação da cliente (relatório de 21/10/2026) |
| 1430 | ◆ MEIO | S5 · recursos de campo agora são geridos pelo administrador (ação "Recursos" em Pesquisas) |
| 1438 | ■ FIM | S5 Controle de acesso rigoroso (bloco da antiga área do Agente) |
| 1605 | ▶ INÍCIO | S1–S4 + D.1–D.5 · focus group (solicitações de 21/10/2026, revistas pela evolução de 27/10/2026) |
| 1617 | ◆ MEIO | S1–S5 · etiquetas visíveis: solicitação da cliente e etapa do fluxo |
| 1623 | ◆ MEIO | S2/D.1–D.2 · utilidades: plataformas aceitas e validação do link (redirecionamento, sem integração técnica) |
| 1641 | ▶ INÍCIO | S1 Proteção anti-vazamento (DRM no navegador) |
| 1657 | ◆ MEIO | S1 · registro e bloqueios (instalados uma vez, valem só onde existe .drm na tela) |
| 1680 | ■ FIM | S1 Proteção anti-vazamento |
| 1682 | ▶ INÍCIO | S2 + D.1 · reuniões: telas do administrador (moderação) |
| 1703 | ◆ MEIO | S2/D.1/D.5 · ETAPA 1 (INÍCIO): agendar a reunião, colar o link e convidar os recrutados |
| 1728 | ◆ MEIO | S1/S3/D.1 · ETAPA 2 (MEIO): o vídeo é no Teams/Meet; aqui só a apresentação protegida dos materiais |
| 1745 | ■ FIM | S2 + D.1 · telas do administrador e apresentação |
| 1747 | ▶ INÍCIO | S2 + D.5 · participante: convite, termo de sigilo, consentimento de gravação e link externo |
| 1766 | ■ FIM | S2 + D.5 · participante |
| 1768 | ▶ INÍCIO | S4 + D.3 · ETAPA 3 (FIM): esteira da equipe interna (transcrição importada, sem captura automática) |
| 1775 | ◆ MEIO | D.3 · leitura do arquivo de transcrição do Teams/Meet (.vtt ou .txt). Nada é inventado: sem arquivo ou texto, nada entra. |
| 1801 | ■ FIM | S4 + D.3 · esteira |
| 1803 | ▶ INÍCIO | S1–S4 + D · ações dos botões |
| 1823 | ■ FIM | S1–S4 + D · ações dos botões |
| 1824 | ■ FIM | S1–S4 + D.1–D.5 · focus group |
| 1830 | ◆ MEIO | E.5–E.7 · camada central de autorização: toda ação que muda dados passa por exigir() |
| 1842 | ■ FIM | E.1–E.8 · camada de autorização |
| 1844 | ▶ INÍCIO | AC · acessos calculados (refatoração de 28/10/2026) |
| 2106 | ■ FIM | AC · acessos calculados |
| 2110 | ▶ INÍCIO | A.1/A.2 · importação centralizada em Pesquisas (pesquisas por CSV e respostas por arquivo) |
| 2132 | ■ FIM | A.1/A.2 · importação |
| 2134 | ▶ INÍCIO | A.3 · resultados por perfil: painel agregado + respostas detalhadas só para quem pode |
| 2165 | ■ FIM | A.3 · resultados |
| 2167 | ▶ INÍCIO | B.2/B.5 · convites: detalhes com histórico do ciclo de vida e edição enquanto não foram abertos |
| 2182 | ■ FIM | B.2/B.5 · convites |
| 2184 | ▶ INÍCIO | B.3/B.4 · documentos do projeto (tipos configuráveis; obrigatoriedade desligada até a regra ser confirmada) |
| 2191 | ■ FIM | B.3/B.4 · documentos |
| 2193 | ▶ INÍCIO | C.1–C.5, C.7 · cadastros com paginação, filtros, ordenação e seleção (individual, página, conjunto filtrado) |
| 2241 | ■ FIM | C.1–C.5, C.7 · cadastros |
| 2243 | ▶ INÍCIO | C.6 · dispositivo usado ao responder (pergunta na revisão do participante; também vem na importação) |
| 2245 | ■ FIM | C.6 |
| 2247 | ▶ INÍCIO | A.4, D.2, D.4, D.5, E.4 · Integrações: o que é real, o que é só link e o que falta |
| 2258 | ■ FIM | A.4, D.2, D.4, D.5 · Integrações |
| 2260 | ▶ INÍCIO | A–E · ações novas |
| 2288 | ◆ MEIO | E.5 · cada ação que muda dados passa pela checagem central, mesmo se o botão for forjado no navegador |
| 2299 | ■ FIM | A–E · ações novas e camada E.5 |
| 2322 | ▶ INÍCIO | V2 · migração única dos dados (sem trocar a chave do localStorage, como a refatoração de acessos) |
| 2340 | ■ FIM | V2 · migração |
| 2343 | ▶ INÍCIO | RF05 · login de usuário e cadastro em destaque; entrada administrativa discreta (rodapé → #acesso-interno) |
| 2376 | ▶ INÍCIO | RF03 · agente sem login gerado continua recusado (substitui a recusa geral da S5) |
| 2378 | ■ FIM | RF03 · agente sem login |
| 2393 | ■ FIM | RF05 |
| 2396 | ▶ INÍCIO | RF01 · o cliente vê resultados só do que o administrador liberou (todas as pesquisas contratadas ou uma escolhida) |
| 2446 | ■ FIM | RF01 |
| 2449 | ▶ INÍCIO | RF03 · o administrador confere o cadastro do agente, cria o vínculo e gera o login; desativar corta o acesso e mantém o histórico |
| 2564 | ■ FIM | RF03 |
| 2567 | ▶ INÍCIO | RF04 · a checagem automática só sinaliza; quem decide é a revisão humana, sempre com motivo registrado |
| 2605 | ■ FIM | RF04 |
| 2608 | ▶ INÍCIO | RF02 · dados do audiovisual num armazenamento separado (faz o papel do banco), sempre lidos e gravados dentro de uma trava exclusiva entre abas |
| 2632 | ◆ MEIO | RF02 · "API" do audiovisual: cada função confere sessão, vínculo, autorização e estado; a tela só mostra o resultado |
| 2685 | ◆ MEIO | RF02 · telas: participante (check-in, reprodução sem reinício) e administração (autorizações, código do local, registro, limites) |
| 2741 | ■ FIM | RF02 |
| 2743 | ▶ INÍCIO | V2 · execução: migra uma vez, recalcula as contas e restaura também os dados novos ao "Restaurar dados de exemplo" |
| 2746 | ■ FIM | V2 · execução |

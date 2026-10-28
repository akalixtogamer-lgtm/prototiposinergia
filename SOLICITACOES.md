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

## Etiquetas no `index.html` (linha · etiqueta · trecho)

| Linha | Etiqueta | Trecho |
| --- | --- | --- |
| 384 | ▶ INÍCIO | S2 (site) · estilos da página Focus group online |
| 391 | ■ FIM | S2 (site) · estilos |
| 418 | ▶ INÍCIO | S1–S5 · estilos das solicitações da cliente (relatório de 21/10/2026) |
| 479 | ■ FIM | S1–S5 · estilos |
| 480 | ▶ INÍCIO | evolução 27/10/2026 · paginação, seleção em massa, ciclo do convite, importação |
| 493 | ■ FIM | evolução 27/10/2026 |
| 610 | ▶ INÍCIO | S2 (site) · chamada da home para o focus group online |
| 612 | ■ FIM | S2 (site) · chamada da home |
| 629 | ▶ INÍCIO | S2 (site) · destaque do focus group em Serviços |
| 629 | ■ FIM | S2 (site) · destaque |
| 652 | ▶ INÍCIO | S2 (site público) · página "Focus group online" — solicitação da cliente (relatório de 21/10/2026) |
| 658 | ◆ MEIO | S2 (site) · as três etapas do fluxo |
| 665 | ◆ MEIO | S1/S5 (site) · proteção e controle de acesso |
| 674 | ■ FIM | S2 (site público) · página "Focus group online" |
| 733 | ▶ INÍCIO | C.1–C.6, B.3, A.3, A.4, E · dados de exemplo novos (sobre o seed anterior). Fictícios, só para o protótipo. |
| 767 | ■ FIM | dados de exemplo novos |
| 769 | ▶ INÍCIO | E.1–E.4, E.8 · perfis, módulos, ações e matriz padrão (proposta para validar com a Sinergia) |
| 782 | ◆ MEIO | E.1–E.4 · perfis e matriz padrão continuam abaixo (sys4-evol.js) |
| 821 | ▶ INÍCIO | S5 · contas: agentes (entrevistadores terceirizados) perdem o login; entram 3 perfis da equipe interna |
| 826 | ◆ MEIO | S5 · equipe interna: transcrição, processamento (parceiro) e assistentes de análise |
| 830 | ■ FIM | S5 · contas |
| 893 | ▶ INÍCIO | S2/S5 · permissões novas: focus group e esteira da equipe interna (agente saiu da matriz) |
| 895 | ■ FIM | S2/S5 · permissões novas |
| 900 | ▶ INÍCIO | S2/S3/S4 · dados de exemplo do focus group (sessões, materiais protegidos e esteira de transcrição) |
| 908 | ◆ MEIO | S2 · uma sessão em cada etapa: Início (agendada), Meio (ao vivo) e Fim (encerrada, na esteira) |
| 922 | ■ FIM | S2/S3/S4 · dados de exemplo |
| 968 | ▶ INÍCIO | S5 · perfis: "Agente" sai; "Equipe interna" entra (função: transcrição, processamento ou análise) |
| 975 | ■ FIM | S5 · perfis |
| 987 | ▶ INÍCIO | E.2 · as capacidades antigas dos menus agora consultam a matriz módulo × ação (sys4-evol.js) |
| 990 | ■ FIM | E.2 |
| 995 | ▶ INÍCIO | S5 · rotas antigas do Agente ficam bloqueadas para qualquer conta |
| 997 | ■ FIM | S5 · rotas antigas do Agente |
| 998 | ▶ INÍCIO | E.7 · sessão expirada, rota sem permissão e acesso direto: comportamento definido |
| 1007 | ■ FIM | E.7 |
| 1073 | ▶ INÍCIO | S5 · login recusado para entrevistadores e terceirizados |
| 1076 | ■ FIM | S5 · login recusado |
| 1250 | ▶ INÍCIO | S5 Controle de acesso rigoroso · solicitação da cliente (relatório de 21/10/2026) |
| 1254 | ◆ MEIO | S5 · recursos de campo agora são geridos pelo administrador (ação "Recursos" em Pesquisas) |
| 1262 | ■ FIM | S5 Controle de acesso rigoroso (bloco da antiga área do Agente) |
| 1437 | ▶ INÍCIO | S1–S4 + D.1–D.5 · focus group (solicitações de 21/10/2026, revistas pela evolução de 27/10/2026) |
| 1449 | ◆ MEIO | S1–S5 · etiquetas visíveis: solicitação da cliente e etapa do fluxo |
| 1455 | ◆ MEIO | S2/D.1–D.2 · utilidades: plataformas aceitas e validação do link (redirecionamento, sem integração técnica) |
| 1473 | ▶ INÍCIO | S1 Proteção anti-vazamento (DRM no navegador) |
| 1489 | ◆ MEIO | S1 · registro e bloqueios (instalados uma vez, valem só onde existe .drm na tela) |
| 1512 | ■ FIM | S1 Proteção anti-vazamento |
| 1514 | ▶ INÍCIO | S2 + D.1 · reuniões: telas do administrador (moderação) |
| 1535 | ◆ MEIO | S2/D.1/D.5 · ETAPA 1 (INÍCIO): agendar a reunião, colar o link e convidar os recrutados |
| 1560 | ◆ MEIO | S1/S3/D.1 · ETAPA 2 (MEIO): o vídeo é no Teams/Meet; aqui só a apresentação protegida dos materiais |
| 1577 | ■ FIM | S2 + D.1 · telas do administrador e apresentação |
| 1579 | ▶ INÍCIO | S2 + D.5 · participante: convite, termo de sigilo, consentimento de gravação e link externo |
| 1598 | ■ FIM | S2 + D.5 · participante |
| 1600 | ▶ INÍCIO | S4 + D.3 · ETAPA 3 (FIM): esteira da equipe interna (transcrição importada, sem captura automática) |
| 1607 | ◆ MEIO | D.3 · leitura do arquivo de transcrição do Teams/Meet (.vtt ou .txt). Nada é inventado: sem arquivo ou texto,  |
| 1633 | ■ FIM | S4 + D.3 · esteira |
| 1635 | ▶ INÍCIO | S1–S4 + D · ações dos botões |
| 1655 | ■ FIM | S1–S4 + D · ações dos botões |
| 1656 | ■ FIM | S1–S4 + D.1–D.5 · focus group |
| 1662 | ◆ MEIO | E.5–E.7 · camada central de autorização: toda ação que muda dados passa por exigir() |
| 1674 | ■ FIM | E.1–E.8 · camada de autorização |
| 1676 | ▶ INÍCIO | E.2/E.3/E.8 · tela da matriz módulo × ação por perfil |
| 1684 | ■ FIM | E.2/E.3/E.8 · matriz |
| 1686 | ▶ INÍCIO | A.1/A.2 · importação centralizada em Pesquisas (pesquisas por CSV e respostas por arquivo) |
| 1708 | ■ FIM | A.1/A.2 · importação |
| 1710 | ▶ INÍCIO | A.3 · resultados por perfil: painel agregado + respostas detalhadas só para quem pode |
| 1736 | ■ FIM | A.3 · resultados |
| 1738 | ▶ INÍCIO | B.2/B.5 · convites: detalhes com histórico do ciclo de vida e edição enquanto não foram abertos |
| 1753 | ■ FIM | B.2/B.5 · convites |
| 1755 | ▶ INÍCIO | B.3/B.4 · documentos do projeto (tipos configuráveis; obrigatoriedade desligada até a regra ser confirmada) |
| 1762 | ■ FIM | B.3/B.4 · documentos |
| 1764 | ▶ INÍCIO | C.1–C.5, C.7 · cadastros com paginação, filtros, ordenação e seleção (individual, página, conjunto filtrado) |
| 1812 | ■ FIM | C.1–C.5, C.7 · cadastros |
| 1814 | ▶ INÍCIO | C.6 · dispositivo usado ao responder (pergunta na revisão do participante; também vem na importação) |
| 1816 | ■ FIM | C.6 |
| 1818 | ▶ INÍCIO | A.4, D.2, D.4, D.5, E.4 · Integrações: o que é real, o que é só link e o que falta |
| 1829 | ■ FIM | A.4, D.2, D.4, D.5 · Integrações |
| 1831 | ▶ INÍCIO | A–E · ações novas |
| 1860 | ◆ MEIO | E.5 · cada ação que muda dados passa pela checagem central, mesmo se o botão for forjado no navegador |
| 1870 | ■ FIM | A–E · ações novas e camada E.5 |

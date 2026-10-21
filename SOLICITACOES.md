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

## Etiquetas no `index.html` (linha · etiqueta · trecho)

| Linha | Etiqueta | Trecho |
| --- | --- | --- |
| 381 | ▶ INÍCIO | S2 (site) · estilos da página Focus group online |
| 388 | ■ FIM | S2 (site) · estilos |
| 415 | ▶ INÍCIO | S1–S5 · estilos das solicitações da cliente (relatório de 21/10/2026) |
| 476 | ■ FIM | S1–S5 · estilos |
| 592 | ▶ INÍCIO | S2 (site) · chamada da home para o focus group online |
| 594 | ■ FIM | S2 (site) · chamada da home |
| 611 | ▶ INÍCIO | S2 (site) · destaque do focus group em Serviços |
| 611 | ■ FIM | S2 (site) · destaque |
| 634 | ▶ INÍCIO | S2 (site público) · página "Focus group online" — solicitação da cliente (relatório de 21/10/2026) |
| 640 | ◆ MEIO | S2 (site) · as três etapas do fluxo |
| 647 | ◆ MEIO | S1/S5 (site) · proteção e controle de acesso |
| 656 | ■ FIM | S2 (site público) · página "Focus group online" |
| 744 | ▶ INÍCIO | S5 · contas: agentes (entrevistadores terceirizados) perdem o login; entram 3 perfis da equipe interna |
| 749 | ◆ MEIO | S5 · equipe interna: transcrição, processamento (parceiro) e assistentes de análise |
| 753 | ■ FIM | S5 · contas |
| 816 | ▶ INÍCIO | S2/S5 · permissões novas: focus group e esteira da equipe interna (agente saiu da matriz) |
| 818 | ■ FIM | S2/S5 · permissões novas |
| 823 | ▶ INÍCIO | S2/S3/S4 · dados de exemplo do focus group (sessões, materiais protegidos e esteira de transcrição) |
| 831 | ◆ MEIO | S2 · uma sessão em cada etapa: Início (agendada), Meio (ao vivo) e Fim (encerrada, na esteira) |
| 845 | ■ FIM | S2/S3/S4 · dados de exemplo |
| 891 | ▶ INÍCIO | S5 · perfis: "Agente" sai; "Equipe interna" entra (função: transcrição, processamento ou análise) |
| 898 | ■ FIM | S5 · perfis |
| 915 | ▶ INÍCIO | S5 · rotas antigas do Agente ficam bloqueadas para qualquer conta |
| 917 | ■ FIM | S5 · rotas antigas do Agente |
| 989 | ▶ INÍCIO | S5 · login recusado para entrevistadores e terceirizados |
| 992 | ■ FIM | S5 · login recusado |
| 1180 | ▶ INÍCIO | S5 Controle de acesso rigoroso · solicitação da cliente (relatório de 21/10/2026) |
| 1184 | ◆ MEIO | S5 · recursos de campo agora são geridos pelo administrador (ação "Recursos" em Pesquisas) |
| 1192 | ■ FIM | S5 Controle de acesso rigoroso (bloco da antiga área do Agente) |
| 1368 | ▶ INÍCIO | S1–S4 · bloco novo das solicitações da cliente (relatório de 21/10/2026) |
| 1378 | ◆ MEIO | S1–S5 · etiquetas visíveis: solicitação da cliente e etapa do fluxo |
| 1384 | ◆ MEIO | S2 · utilidades do focus group |
| 1399 | ▶ INÍCIO | S1 Proteção anti-vazamento (DRM no navegador) |
| 1415 | ◆ MEIO | S1 · registro e bloqueios (instalados uma vez, valem só onde existe .drm na tela) |
| 1438 | ■ FIM | S1 Proteção anti-vazamento |
| 1440 | ▶ INÍCIO | S2 Ambiente de focus group · telas do administrador (moderação) |
| 1461 | ◆ MEIO | S2 · ETAPA 1 (INÍCIO): agendar sessão e convidar os recrutados |
| 1481 | ◆ MEIO | S2/S3 · ETAPA 2 (MEIO): sala ao vivo — vídeo, chat e apresentação de materiais |
| 1513 | ■ FIM | S2 · telas do administrador e sala |
| 1515 | ▶ INÍCIO | S2 · participante: convites para debates e entrada na sala (com termo de sigilo) |
| 1534 | ■ FIM | S2 · participante |
| 1536 | ▶ INÍCIO | S4 Integração · ETAPA 3 (FIM): esteira da equipe interna e insights nos resultados do cliente |
| 1560 | ■ FIM | S4 Integração |
| 1562 | ▶ INÍCIO | S1–S4 · ações dos botões |
| 1583 | ■ FIM | S1–S4 · ações dos botões |
| 1584 | ■ FIM | S1–S4 · bloco novo das solicitações da cliente |

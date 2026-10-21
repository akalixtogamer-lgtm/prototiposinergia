# Sinergia Surveys — site e sistema (protótipo navegável)

Site institucional e sistema de pesquisas da Sinergia Research & Intelligence, montados a partir do mapa de navegação e do protótipo consolidado do Figma. Tudo roda no navegador: os dados de exemplo ficam salvos no `localStorage` de quem está usando, e cada pessoa vê a sua própria cópia. Nada é enviado para servidor.

## Estrutura

```
index.html                 site completo (HTML, CSS e JS num arquivo só)
assets/logo-sinergia.png   logo
SOLICITACOES.md            mapa das etiquetas ▶ INÍCIO / ◆ MEIO / ■ FIM das solicitações da cliente
```

## Login e permissões

O login tem duas entradas:

- **Administrador**: gerencia pesquisas, projetos, convites, resultados, cadastros, usuários e permissões.
- **Usuário**: navega como **Equipe interna**, **Cliente Empresa** e/ou **Participante**, conforme o que o administrador marcar em *Usuários e permissões*. Quem tem mais de uma permissão escolhe o perfil ao entrar e troca pelo menu lateral ("Navegar como").

Na aba *Permissões por perfil*, o administrador também liga ou desliga funções de cada perfil (por exemplo, esconder os insights de focus group do cliente).

Entrevistadores e terceirizados (agentes de campo) **não têm acesso** à plataforma: ficam só em Cadastros, e o login recusa o e-mail deles (solicitação S5).

### Contas de demonstração (qualquer senha com 4+ caracteres)

| Conta | Acesso |
|---|---|
| helena@sinergia.com.br | Administrador |
| demo@sinergia.com.br | Usuário · Equipe interna (análise), Cliente e Participante |
| bianca@sinergia.com.br | Usuário · Equipe interna — Transcrição |
| carla@dadosco.com.br | Usuário · Equipe interna — Processamento (parceiro Dados & Co) |
| livia@sinergia.com.br | Usuário · Equipe interna — Assistente de análise |
| joao.tadeu@sinergia.com.br | Usuário · Participante |
| yasmin@sinergia.com.br | Entrevistadora terceirizada: o login é recusado de propósito |
| marina@cinemaalfa.com.br | Usuário · Cliente (Cinema Alfa) |
| ana.ribeiro@email.com | Usuário · Participante |

## Solicitações da cliente (relatório de 21/10/2026)

| Código | Pedido | Onde ver |
|---|---|---|
| S1 | Proteção anti-vazamento | Material na sala: marca d'água com nome e hora, pausa fora da tela, captura/impressão bloqueadas e registradas (*Focus group → Registro de acesso*) |
| S2 | Focus group com chat de vídeo | Administrador: *Focus group*; participante: *Debates*; equipe: *Focus group*; site público: *Focus group* |
| S3 | Apresentar materiais no chat | Controles da moderação dentro da sala |
| S4 | Integração com a plataforma | Aba *Focus group* no projeto, esteira *Transcrição e análise*, insights nos resultados do cliente |
| S5 | Controle de acesso | Agente sem login; perfil Equipe interna com 3 funções |

Fluxo em três etapas, marcado nas telas: **1 · INÍCIO** agendar e convidar → **2 · MEIO** sala ao vivo → **3 · FIM** transcrição e análise. Limite honesto do S1: nenhum site impede foto da tela feita com outro aparelho; a marca d'água individual identifica quem vazou. Na versão real, o vídeo precisa de DRM (Widevine, FairPlay ou PlayReady).

O cadastro de participante no site cria uma conta nova com permissão de Participante. O botão *Restaurar dados de exemplo* (menu do administrador) volta tudo ao estado inicial.

## Telas

| Área | Telas do Figma | Endereço |
|---|---|---|
| Site | Home, Serviços, Cinema, CAT, CIA, Pesquisa aberta, Cadastro | `#home`, `#servicos`, `#cinema`, `#cat`, `#cia`, `#pesquisa`, `#cadastro` |
| Acesso | Login (Administrador / Usuário) e escolha de perfil | `#login`, `#navegar` |
| Administrador | A1 Pesquisas e A2 Nova pesquisa, A3 Resultados, A4 Projetos, A5 Projeto, A9 Clientes, A10 Cliente, A6 Convites, A7 Cadastros, A8 Usuários e permissões | `#adm-pesquisas`, `#adm-resultados`, `#adm-projetos`, `#adm-projeto`, `#adm-clientes`, `#adm-cliente`, `#adm-convites`, `#adm-cadastros`, `#adm-usuarios` |
| Agente | Desativada (S5): entrevistadores e terceirizados não acessam | — |
| Equipe interna | Focus group, Sala (observação), Transcrição e análise, Perfil | `#eq-focus`, `#eq-sala`, `#eq-transcricoes`, `#eq-perfil` |
| Cliente Empresa | K2 Projetos (início), K3 Projeto, K5 Resultado individual, K1 Resultados (todas as pesquisas), K4 Perfil | `#cl-projetos`, `#cl-projeto`, `#cl-resultado`, `#cl-resultados`, `#cl-perfil` |
| Participante | R1 Minhas pesquisas, R2 Preferências, R3 Pergunta com imagens, R4 Revisão, R5 Concluída, R6 Minhas respostas, R7 Perfil | `#pa-pesquisas`, `#pa-preferencias`, `#pa-responder`, `#pa-revisao`, `#pa-concluida`, `#pa-respostas`, `#pa-perfil` |

### Revisão de 21/10/2026

- Breadcrumb em todas as telas (site, login e áreas logadas).
- Alerta visual de prazo nas listas de pesquisas do agente e do participante (vencida, vence em até 3 dias, vence em até 7 dias).
- Formulário de pesquisa: projeto e tipo em lista, local de aplicação online/presencial (ou os dois), agente em campo com ou sem agente (com seleção de agentes) e prazo com início e fim.
- Menu *Clientes* no administrador, com os projetos de cada cliente.
- Botão *Importar pesquisas* (CSV `nome;tipo;inicio;fim;meta`) em Projetos e dentro de cada projeto.
- *Recursos* virou uma janela aberta em Detalhes da pesquisa (agente).
- Cliente Empresa entra por Projetos e vê o resultado individual de cada pesquisa; *Resultados* soma todas.
- Participante recebe recomendações de pesquisas abertas; o pedido passa por triagem do administrador em Convites.
- Cadastros com data de cadastro e filtro por tipo de pesquisa.

Os dados ficam no navegador com a chave `sinergia-sistema-v2`; quem abriu a versão anterior recebe os dados novos automaticamente.

As áreas logadas exigem login; um endereço de outra área redireciona para a área permitida.

## Publicar no GitHub Pages

1. Crie um repositório no GitHub e envie `index.html` e a pasta `assets` para a raiz.
2. No repositório, abra **Settings → Pages**.
3. Em **Source**, escolha **Deploy from a branch**, branch `main`, pasta `/ (root)` e clique em **Save**.
4. Em um ou dois minutos o site fica em `https://SEU-USUARIO.github.io/NOME-DO-REPOSITORIO/`.

## Sobre o acesso

- Em contas gratuitas, o GitHub Pages só publica repositórios **públicos**: qualquer pessoa com o link consegue abrir. O arquivo pede aos buscadores para não indexar a página (`noindex`), mas isso não é uma proteção de acesso.
- Para restringir a algumas pessoas: deixe o repositório **privado** e adicione-as como colaboradoras (Settings → Collaborators). Elas baixam e abrem o `index.html` no navegador, sem precisar de servidor.
- Páginas privadas com controle de acesso exigem GitHub Enterprise Cloud.

## Testar localmente

Abra `index.html` direto no navegador. As fontes vêm do Google Fonts, então é preciso estar on-line para vê-las; sem internet o site usa fontes de reserva.

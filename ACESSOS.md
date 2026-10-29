# Refatoração de acessos — 28/10/2026

Usuários, permissões automáticas e arquitetura de autorização. As permissões deixaram de ser marcadas à mão, usuário por usuário: o sistema calcula o acesso a partir dos **vínculos** de cada conta e das **políticas** de cada papel.

Branch: `refatoracao-acessos` (pull request para `main`; o site publicado só muda depois do merge).

## Etapa 1 — Diagnóstico (antes da mudança)

**Tecnologia.** Site estático num único `index.html` (HTML, CSS e JavaScript puro), publicado no GitHub Pages. Não existe servidor nem banco: os dados ficam no `localStorage` de cada navegador (chave `sinergia-sistema-v4`). O login aceita qualquer senha com 4+ caracteres. Testes: pytest + Playwright.

**De onde vinham as permissões.**

1. Conta: `admin` (sim/não) + checkboxes `perms` (Equipe, Cliente, Participante) + `funcao`, `empresa`, `codigo`.
2. Sessão: quem tinha mais de um perfil escolhia um por vez ("Navegar como"). Os privilégios não se somavam.
3. Matriz por perfil (`S.perm2`), editável pelo administrador na aba "Permissões por perfil".
4. Aplicação: `guard()` nas rotas, `pode()` em menus e botões, `exigir()` nas ações que alteram dados; escopo de cliente e participante conferido tela a tela.

**Riscos encontrados.**

| Risco | Detalhe |
| --- | --- |
| Ampliação silenciosa | Marcar "Cliente" sem empresa definia a primeira empresa da lista (Cinema Alfa). Marcar "Equipe" definia a função Transcrição. Marcar "Participante" criava um cadastro sem aviso |
| Checkbox como fonte da verdade | Nada conferia se havia um vínculo real por trás; sem situação de conta, origem ou validade |
| Auditoria parcial | Só acessos negados; quem deu ou tirou perfil, quem virou administrador e quem mudou a matriz não ficava registrado |
| Administrador sem proteção | Era possível remover a própria conta e o último administrador |
| Conflito de vínculos | A conta de demonstração do Rafael era assistente de análise (vê respostas de todos os clientes) e cliente da Cinema Alfa, sem regra |
| Dado legado | Matriz antiga `S.matrix` no seed, sem uso, ao lado de `S.perm2` |
| Vazamento (achado nos testes novos) | O breadcrumb do cliente mostrava o nome de uma pesquisa de outra empresa quando o endereço era forçado |
| Sem servidor | Toda regra roda no navegador; quem edita o `localStorage` altera os dados (limite estrutural, ver "Limites") |

## Etapa 2 — Arquitetura

```
Login (identidade) → situação da conta → vínculos válidos → papel da sessão
→ política do papel (código, só leitura) → permissões efetivas + escopo
→ guard() em cada tela / exigir() em cada ação → permitido ou negado (negado vai para a auditoria)
```

**Conceitos separados.**

| Conceito | Onde fica |
| --- | --- |
| Identidade | Conta (`S.users`): nome, e-mail, telefone, `bloqueado` |
| Vínculo | `u.vinculos[]`: `tipo` (admin, equipe, cliente, participante), `ref` (função, empresa ou código), `situacao` (ativo, convite, aprovacao, revisao, revogado; expirado é calculado pela `validade`), `origem`, `desde`, `validade`, `motivo`, `aprovadoPor` |
| Papel | Tipo de um vínculo válido; um por sessão |
| Política | `POLITICAS` no código (congelada): perfil → ações permitidas. Seis perfis: admin, transcricao, processamento, analise, cliente, participante |
| Permissões efetivas e escopo | Calculadas por `avaliarConta()` / `explicar()`; os campos antigos (`admin`, `perms`, `empresa`, `codigo`, `funcao`) viram reflexo dos vínculos e são sobrescritos a cada leitura (`me()` → `projetar()`) |
| Auditoria | `S.auditoria`: `tipo` alteracao ou negado, quem, perfil, ação, alvo, motivo |

**Regras (R1–R13).** Negação por padrão; conta suspensa não acessa; só vínculo ativo e dentro da validade conta; administrador só com aprovação de **outro** administrador; equipe recebe a política da função; cliente vê só a própria empresa; participante vê só o próprio código; um papel por sessão e equipe + cliente vai para revisão; usuários e integrações só com administrador; entrevistadores e terceirizados de campo sem conta (S5); acesso recalculado em toda rota e ação; toda mudança de acesso auditada; administrador não reduz a própria proteção. A tela *Arquitetura de acessos* lista cada regra com a função onde é aplicada.

**Matriz de papéis e capacidades** (tirada de `POLITICAS`; a mesma da tela):

| Papel | Gerenciar usuários | Clientes e cadastros | Gerenciar projetos | Pesquisas | Convites | Reuniões | Resultados | Processar dados | Integrações |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Administrador | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Equipe · Transcrição | — | — | — | — | — | ✓ | — | ✓ | — |
| Equipe · Processamento (parceiro) | — | — | — | — | — | ✓ | — | ✓ | — |
| Equipe · Assistente de análise | — | — | — | — | — | ✓ | ✓ | ✓ | — |
| Cliente Empresa | — | — | — | — | — | — | ✓ (só a empresa) | — | — |
| Participante | — | — | — | — | — | ✓ (só convidado) | — | — | — |

Matriz completa módulo × ação: [PERMISSOES.md](PERMISSOES.md).

## Etapa 3 — Protótipo (Figma)

Arquivo "Sinergia — Protótipo Consolidado", página Protótipo, seção **"Refatoração de acessos · 28/10/2026"**:

- **REF · A8** e **REF · EV-E1**: cópias das telas antigas, com faixa de referência. As originais continuam nas seções delas.
- **AC-01 · Usuários e acessos**: indicadores, busca e filtros, tabela com situação, papel, vínculo, acesso calculado (fundo tracejado: informação calculada, não campo), origem e atualização.
- **AC-02 · Detalhes do usuário**: vínculos com situação e origem, acesso efetivo (bloco "calculado pelo sistema · só leitura"), restrições e motivos, ações do administrador (bloco separado, com borda de destaque) e histórico.
- **AC-03 · Arquitetura de acessos**: fluxo, matriz, regras, auditoria, diagnóstico e estado verificado.
- **AC-04 · Estados**: sucesso, erro, vazio, acesso negado, sem vínculo válido, precisa de revisão, conta suspensa e confirmação com motivo.
- Componentes novos (página Componentes): **Linha de usuário · acessos**.
- Fluxo clicável "Refatoração de acessos · 28/10/2026": Detalhes → AC-02 → Ver diagnóstico → AC-03; abas e Fechar voltam para AC-01.

## Etapa 4 — Implementação

**Arquivos alterados.**

| Arquivo | Mudança |
| --- | --- |
| `index.html` | Módulo "AC · acessos calculados" (serviço central: vínculos, migração, políticas, cálculo, explicação, auditoria, telas); `me()` recalcula o acesso; `pode()` usa `POLITICAS`; login aceita convite, recusa conta suspensa e explica pendências; cadastro público cria vínculo de participante; tela *Usuários e acessos* com abas Usuários, Arquitetura de acessos e Auditoria; checkboxes, matriz editável e formulário com empresa padrão removidos; breadcrumb do cliente sem nome de outra empresa; três contas de demonstração novas |
| `tests/test_acessos.py` | 17 testes novos (abaixo) |
| `tests/test_autorizacao.py` | Teste da matriz editável virou "matriz só leitura e política vem do código"; teste do cliente sem dados individuais agora adultera a cópia gravada e confere que nada libera |
| `ACESSOS.md`, `PERMISSOES.md`, `README.md`, `REVERSAO.md` | Documentação |

**Migração controlada** (`migrarAcessos`, roda uma vez ao carregar):

1. Lê `admin` e os checkboxes de cada conta.
2. Cria um vínculo por item, com origem "Migração 28/10/2026".
3. Só fica **ativo** o que tem referência válida (função reconhecida, empresa cadastrada, código com cadastro). O resto vai para **em revisão**, com o motivo; nenhuma empresa, função ou código é escolhido pelo sistema.
4. Equipe interna + cliente na mesma conta: o vínculo de cliente vai para revisão (R8).
5. Guarda os valores antigos em `u.legado` (reversão) e registra cada conta na auditoria.
6. Ninguém ganha acesso que não tinha. A validação antes da ativação definitiva é o próprio pull request: o `main` continua na versão anterior até o merge.

**Novas contas de demonstração.**

| Conta | Para mostrar |
| --- | --- |
| marcos@sinergia.com.br | Segundo administrador: aprova nomeações (R4) |
| otavio@ciabeta.com | Convite pendente: o acesso de Cliente (Cia Beta) vale ao entrar |
| paulo@cinemadelta.com.br | Conta suspensa: o login é recusado |
| demo@sinergia.com.br | Agora entra como Equipe ou Participante; o vínculo de Cliente está em revisão (R8) até um administrador confirmar |

## Etapa 5 — Validação

Comando: `pytest -q tests` (Chromium headless via Playwright). Última execução: **55 de 55 aprovados** (38 anteriores, com 2 adaptados, + 17 novos).

| Cenário pedido | Teste |
| --- | --- |
| Sem vínculo válido não recebe acesso | `test_sem_vinculo_valido_nao_entra`, `test_checkboxes_sumiram_e_campos_antigos_nao_dao_acesso` |
| Cliente A não acessa Cliente B | `test_cliente_nao_ve_outro_cliente` |
| Participante fora da administração | `test_participante_fora_da_administracao` |
| Equipe só com a função prevista | `test_equipe_so_capacidades_da_funcao` |
| Não eleva privilégio pelo navegador | `test_elevacao_pelo_navegador_nao_funciona`, `test_E6_*` |
| "Chamada direta" respeita as regras | `test_acoes_de_acesso_forjadas_sao_negadas`, `test_E5_acao_forjada_e_bloqueada` |
| Alteração e revogação atualizam o acesso | `test_revogacao_pelo_administrador_tira_o_acesso` |
| Sessão não guarda privilégio após revogação | `test_sessao_perde_privilegio_apos_revogacao` |
| Múltiplos vínculos com regra explícita | `test_multiplos_vinculos` |
| Ações críticas auditáveis | `test_acoes_criticas_auditadas` |
| Nomeação de administrador e proteção do próprio administrador | `test_nomeacao_de_admin_precisa_de_outro_admin`, `test_admin_nao_se_suspende_nem_remove_o_ultimo` |
| Migração sem ampliar acesso | `test_migracao_nao_amplia_acesso` |
| Convite só vale no primeiro acesso | `test_convite_vale_so_no_primeiro_acesso` |
| Estados (vazio, erro, negado) | `test_estados_da_tela` |
| Arquitetura e diagnóstico só explicam | `test_arquitetura_e_diagnostico_so_explicam` |

Não há etapa de compilação: o projeto é HTML estático. A checagem de sintaxe do script e a suíte rodaram sem erros de JavaScript (o `conftest.py` falha qualquer teste com erro no console).

## Limites e riscos residuais

- **Sem backend.** O pedido exige o servidor como autoridade final. Este protótipo não tem servidor; o serviço central faz esse papel dentro do navegador. Ele ignora os campos que os testes adulteram (`admin`, `perms`, `empresa`, matriz gravada, modo da sessão), mas quem edita o próprio `localStorage` consegue reescrever os vínculos. Na versão real, `avaliarConta()`, `vincValido()`, `POLITICAS` e `exigir()` precisam rodar na API, e o navegador só exibe o resultado.
- **Identidade simulada.** Qualquer senha com 4+ caracteres entra; aceitar o convite no primeiro login só faz sentido com autenticação real (senha definida pelo convidado, ou login social/SSO).
- **Entrevistadores e terceirizados** seguem sem conta (decisão S5). Se um dia receberem acesso, devem entrar como vínculo com validade e escopo de pesquisa.
- **Políticas** são proposta inicial para validar com a Sinergia (mesma matriz de 27/10/2026).
- **Auditoria** guardada no navegador (400 registros), sem integridade garantida; em produção, registro só de escrita no servidor.
- **Validade** é conferida na data; não há aviso automático antes de expirar.

## Reversão

Ver [REVERSAO.md](REVERSAO.md), seção "Refatoração de acessos".

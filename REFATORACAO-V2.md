# Prompt Master V2 — implementação da refatoração (28/10/2026)

Implementação dos requisitos RF01–RF05 sobre o sistema existente, seguindo o plano de arquitetura aprovado. Nada foi recriado do zero: o trabalho parte da refatoração de acessos (PR #1, branch `refatoracao-acessos`, commit `7e0fbbd`) e reaproveita o serviço central de autorização dela (vínculos, `POLITICAS`, `guard`, `exigir`, auditoria).

**Limite principal, declarado desde o plano:** o Sinergia não tem servidor (decisão D-06 pendente). Por decisão da Sinergia em 28/10, esta entrega é a **Trilha P**: as regras rodam no navegador, num bloco que faz o papel do servidor. Os testes provam as regras nesse papel. Quem controla o próprio navegador ainda consegue editar os dados locais; em produção, as mesmas funções precisam rodar numa API.

## Decisões recebidas antes de implementar (28/10/2026)

| Tema | Decisão | Efeito |
| --- | --- | --- |
| Servidor | Só o protótipo (Trilha P) | Garantias "no servidor" ficam registradas como bloqueadas por D-06 |
| Agente terceirizado (conflito C-1) | O agente entra como usuário; o administrador pega os dados, cadastra como agente e gera o login de agente | RF03 substitui a S5 |
| Cliente e resultados (conflito C-2) | O cliente vê por solicitação: todas as pesquisas que contratou ou só uma que escolher | Fluxo de pedido e liberação (RF01) |
| GitHub | Branch nova + pull request, sem merge | PR empilhado sobre o PR #1 |

## Etapa 1 — Diagnóstico antes da edição

| Item | Estado inicial |
| --- | --- |
| Base | Branch `refatoracao-acessos` (PR #1 aberto), commit `7e0fbbd`; `main` em `9c057e7` |
| Estrutura | `index.html` único (HTML, CSS e JS), `tests/` com pytest + Playwright, documentação em `.md` |
| Autenticação | E-mail cadastrado + qualquer senha com 4+ caracteres (simulada) |
| Autorização | Vínculos da conta → papel da sessão → `POLITICAS` (código, só leitura) → `guard()` nas rotas e `exigir()` nas ações |
| "Banco" | Objeto `S` no `localStorage` (`sinergia-sistema-v4`), com migração controlada |
| Armazenamento de arquivos | Nenhum: importações guardavam só nome e tamanho |
| Testes | `pytest -q tests`: **55 de 55** aprovados na base |
| Conflitos com os requisitos | Agente sem login (S5), cliente com resultados sem pedido, nenhuma revisão de pesquisa, status livre no formulário, nenhum fluxo audiovisual individual |

Estratégia: acrescentar um bloco "V2" antes do roteador, com etiquetas por RF, e só editar código existente onde a regra mudou (marcado `RFxx (V2)`). Nenhuma operação destrutiva: dados antigos ficam, o ponto de restauração foi criado antes do primeiro commit.

## Etapa 2 — Permissões

- **Menor privilégio:** políticas novas na fonte única (`permPadrao` → `POLITICAS`, congelada). Ações novas exclusivas do administrador entram em `SO_ADMIN`: revisar e aprovar, publicar, liberar resultados ao cliente, autorizar audiovisual, ver registro audiovisual.
- **Toda ação nova passa por `exigir()`** (sessão válida + política + escopo), inclusive quando o botão ou o formulário é forjado no navegador; negações vão para a auditoria.
- **Cadastro público não concede privilégio:** cria só o vínculo de participante; campos extras forjados no formulário são ignorados (teste `test_cadastro_publico_nao_concede_admin`).
- **Sem elevação pela interface:** o formulário genérico de vínculo não oferece "agente" e recusa envio forjado; vínculo de agente não muda de referência; conta de agente sem código ativo não entra (teste `test_vinculo_de_agente_nao_nasce_por_outro_caminho`).
- **Revogação efetiva:** desativar o login do agente revoga o vínculo e apaga o código; a sessão aberta perde o acesso no próximo clique (R11).
- Matriz completa: [PERMISSOES.md](PERMISSOES.md).

## Etapa 3 — Resultados protegidos (RF01)

| Regra | Como ficou |
| --- | --- |
| Participante não vê resultados | Nenhuma ação `resultados.*` na política; telas de resultado → 403 |
| Agente não vê resultados | Idem; nem dashboards, relatórios ou respostas |
| Exportação, URL direta, ação forjada | Mesma checagem central; tudo negado e registrado |
| Cliente | Vê o agregado só das pesquisas liberadas. Pede em *Resultados* (todas as contratadas ou uma); o administrador aprova, recusa ou revoga em *Resultados → Pedidos de clientes*, com motivo obrigatório para recusar e revogar. "Todas" libera as pesquisas publicadas no momento da aprovação (menor privilégio) |
| Perfis internos | Assistente de análise: consolidados, respostas por código e exportação (matriz provisória, DP-01). Transcrição e processamento: nenhuma categoria |
| Erro sem dado confidencial | Página 403 e telas de recusa não mostram nome de pesquisa de outra empresa, números nem cliente |

## Etapa 4 — Agente terceirizado (RF03)

1. Em *Cadastros → Agentes*, o administrador clica em **Gerar login**, confirma que conferiu os dados (e uma validade opcional) e recebe um **código de acesso de 8 caracteres**, mostrado uma vez só. O sistema guarda apenas o resumo do código.
2. O agente entra pela tela **Entrar**, com o e-mail e o código. Ele vê só **Minhas pesquisas**: cria rascunho, edita, envia arquivos e manda para revisão. Ele não publica.
3. **Campos autorizados (provisório, DP-14):** nome, projeto, tema, tipo de estudo, objetivo, local e modos de aplicação, período e meta. Qualquer outro campo do formulário é ignorado, como status, cliente ou autor.
4. **Pesquisas de outro autor** retornam "não existe ou não é sua", e a tentativa é registrada.
5. **Desativar login** exige motivo. O histórico fica: pesquisas, arquivos e auditoria continuam ligados ao nome do agente. O cadastro de um agente com histórico não pode ser excluído. O substituto recebe login próprio e não herda pesquisas.

**Validação de arquivo (regras provisórias até DP-07):**

| Verificação | Regra |
| --- | --- |
| Extensão | CSV, XLSX ou PDF |
| Tipo declarado | Precisa conferir com a extensão |
| Conteúdo real | PDF começa com `%PDF-` e termina com `%%EOF`; XLSX é ZIP com `[Content_Types].xml` e `xl/`; CSV é texto UTF-8 sem bytes nulos, com cabeçalho e dados |
| Segurança | CSV com célula começando com `=`, `+`, `@` ou `-` não numérico (injeção de fórmula) é recusado |
| Tamanho e quantidade | Até 10 MB por arquivo, até 10 por pesquisa, arquivo vazio recusado |
| Nome | Até 120 caracteres, sem `/ \ : * ? " < > |` |
| Integridade | SHA-256 do conteúdo; o mesmo arquivo duas vezes na pesquisa é recusado |
| Limite | Não há antivírus nem armazenamento real: o protótipo guarda só os metadados. Na versão real, o arquivo vai para armazenamento privado com varredura |

## Etapa 5 — Autorização individual e reprodução única (RF02)

**Fluxo.** O responsável pelas autorizações concede ao participante uma autorização para um conteúdo, com validade obrigatória e sem valor padrão (DP-03). Na Sinergia, o participante abre *Exibições presenciais* no celular e digita o **código do local**, que vale 15 minutos e é gerado pelo responsável (provisório, DP-06). O sistema confere identidade, autorização, validade, revogação, dispositivo e código, e só então cria a **sessão** e entrega um **token só daquela aba**. Ao tocar **Iniciar**, a troca de estado acontece dentro de uma trava e entrega um **ticket de uso único** para o primeiro trecho. A exibição não tem pausa nem reinício; no fim, a sessão fica **Consumida**.

**Estados e transições.**

| Estado | Entra quando | Sai para |
| --- | --- | --- |
| AUTORIZADA | Check-in aceito | INICIADA (início aceito), EXPIRADA, REVOGADA |
| INICIADA | Início aceito na trava | CONSUMIDA (fim), INTERROMPIDA (conexão perdida ou sem sinal por 8 s depois do primeiro trecho), AUTORIZADA (falha **antes** do primeiro trecho: não conta como reprodução), REVOGADA |
| INTERROMPIDA | Queda depois do início | CONSUMIDA (o responsável confirma) ou REVOGADA. Estado de espera: não fixa a política de DP-04 e não deixa o usuário reproduzir de novo |
| CONSUMIDA, EXPIRADA, REVOGADA | — | Finais |

**Proteções.**

| Caso | Mecanismo |
| --- | --- |
| Requisições simultâneas, abas duplicadas | Dados do audiovisual numa chave própria (`sinergia-av-v1`), lidos e gravados sempre dentro de `navigator.locks.request('sinergia-av', exclusive)`: trava entre abas da mesma origem com leitura fresca. A troca AUTORIZADA → INICIADA só acontece uma vez |
| Reenvio da mesma requisição | Chave de idempotência por pedido: a mesma chave recebe a mesma resposta, sem novo início |
| Recarga da página, outra aba | Token guardado só na aba que fez o check-in (`sessionStorage`); depois do início, o estado não é mais AUTORIZADA |
| Reuso de token ou link | Token recusado se ausente, de outra aba ou substituído; ticket de entrega de uso único |
| Nova exibição | Uma sessão por autorização; outra exibição exige nova autorização (provisório, DP-05) |
| Revogação e expiração | Conferidas em todo check-in, início e sinal; sessões abertas viram REVOGADA ou EXPIRADA |
| Frontend não decide | As telas só mostram o resultado das funções `av*`, que conferem tudo |

**Registro** (sem token, sem código, sem e-mail): id interno do usuário, conteúdo, sessão, id do evento, horário do servidor do protótipo, estado anterior → novo e detalhe. Eventos registrados: check-in recusado, sessão criada, início aceito, primeiro trecho, fim, falha antes do início, interrupção, tentativa repetida, requisição repetida, token recusado, ticket recusado, autorização concedida e revogada, código do local gerado.

**Celular compatível (DP-12).** O sistema confere o que o navegador informa (`userAgentData.mobile`, ou agente de usuário móvel com toque). Isso pode ser falsificado e **não prova presença física**; a presença vem do código do local.

**Limites, também mostrados na tela *Medidas e limites*.** Nenhum site impede filmar a tela com outro aparelho. A marca d'água com o código do participante identifica a origem de um vazamento. Na versão real, o conteúdo fica em armazenamento privado, com link curto assinado e DRM de hardware (Widevine L1, FairPlay). O protótipo não tem arquivo de vídeo: a exibição é simulada.

**Responsável pelas autorizações (C-4).** O responsável é configurável e está provisoriamente com a conta Helena Prado, porque ainda falta confirmar quem é a Claudia. Só essa conta concede, revoga, gera o código do local e decide interrupções. Os outros administradores só veem o registro, e nenhum administrador assiste.

## Etapa 6 — Exclusão de pesquisas políticas (RF04)

- Pesquisa de agente: Rascunho → Enviada → **Em revisão** → Devolvida (volta a rascunho), Rejeitada ou Aprovada → **Ativa**, e a publicação é feita só pelo administrador.
- A checagem automática **só sinaliza**: tema declarado "Política, eleições ou governo" e termos no nome e na descrição. Os termos são comparados sem acento e por palavra inteira. A checagem nunca rejeita nem aprova sozinha, porque a política ainda não foi aprovada (DP-09).
- **Revisão humana:** devolver e rejeitar exigem motivo; aprovar com sinal exige justificativa. O agente vê o motivo na própria pesquisa.
- O formulário antigo do administrador não muda a situação de uma pesquisa de agente que ainda não foi publicada, nem por envio forjado.
- Pesquisas criadas pela administração com sinal aparecem só como aviso na tela de revisão (DP-08).

## Etapa 7 — Página inicial (RF05)

- No menu e numa faixa logo abaixo do carrossel, **Entrar** e **Cadastre-se** ganham destaque.
- A tela **Entrar** não tem mais a aba Administrador e traz o atalho "Ainda não tem conta? Cadastre-se".
- O **Acesso interno** (`#acesso-interno`) ficou como link discreto no rodapé. Uma conta sem nomeação de administrador é recusada ali, e a tentativa fica registrada.
- O administrador que tenta a tela comum é orientado a usar o acesso interno. Esconder o link não muda nenhuma permissão: a rota de administrador continua conferindo a conta.
- Acessibilidade: rótulos nos campos e alcance por teclado. Em telas de 360 px não há rolagem lateral na home, no login, no acesso interno e no cadastro.

## Etapa 8 — Dados, integridade e auditoria

| Estrutura | Onde | Integridade e concorrência |
| --- | --- | --- |
| Pedidos de resultado (`S.solicRes`) | `sinergia-sistema-v4` | Um pedido pendente igual por cliente; decisão só a partir de "Pendente"; ids das pesquisas liberadas guardados na aprovação |
| Vínculo de agente, `codigoHash` | `S.users[].vinculos` | Nasce só pelo fluxo de Cadastros; revogado nunca é apagado |
| Revisão, arquivos, origem e autor da pesquisa | `S.pesquisas[]` | Histórico só cresce; arquivo com hash único por pesquisa |
| Conteúdos, autorizações, sessões, códigos e eventos | `sinergia-av-v1` | Toda leitura e gravação dentro da trava exclusiva; uma sessão por autorização; a idempotência fica na sessão |
| Auditoria | `S.auditoria` | Acessos negados e mudanças, com responsável e motivo |

**Migração.** A migração `migrarV2` roda uma vez, sem trocar a chave (mesmo padrão do PR #1). Ela só acrescenta campos e dados de demonstração e não apaga nada. O audiovisual nasce na chave própria. *Restaurar dados de exemplo* também restaura o audiovisual.

**Retenção.** Ainda não implementada, porque o prazo depende de DP-10. O navegador limita o volume: até 3000 eventos de audiovisual e até 400 registros de auditoria. Na versão real, tudo vira tabela com índice único (sessão ativa por autorização) e auditoria só de inserção, como no plano.

## Etapa 9 — Testes

Comando: `pytest -q tests` (Chromium headless). Última execução: **106 de 106 aprovados** (6 min 25 s). Uma segunda rodada só do audiovisual também aprovou 14 de 14, para conferir que os testes de concorrência e de tempo não são instáveis. Dois testes antigos foram adaptados porque a regra mudou: `test_S5_*` agora espera "login ainda não gerado" e `test_R8_*` libera o cliente antes. O ajudante de login dos testes passou a usar o acesso interno para administradores.

| Item exigido | Testes | Resultado |
| --- | --- | --- |
| 1. Login, cadastro e autorização por perfil | `test_v2_rf05_home.py` (7 casos + 4 larguras), `test_acessos.py`, `test_autorizacao.py` | Aprovado |
| 2. Acesso indevido a resultados (interface e "API") | `test_v2_rf01_resultados.py::test_sem_rota_de_resultado` (4 perfis), `test_exportacao_e_liberacao_forjadas_sao_negadas` (3 perfis) | Aprovado |
| 3. Agente e dados proibidos | `test_v2_rf03_agente.py::test_agente_nao_ve_resultados_nem_pesquisa_de_outro` | Aprovado |
| 4. Upload válido e inválido | `test_upload_valido_e_invalidos` (3 válidos, 10 recusados) | Aprovado |
| 5. Revogação e substituição de agentes | `test_desativar_corta_acesso_e_mantem_historico`, `test_sessao_aberta_perde_acesso_na_desativacao` | Aprovado |
| 6. Autorização individual | `test_sem_autorizacao_ou_codigo_errado_nao_cria_sessao`, `test_responsavel_concede_com_validade_obrigatoria`, `test_so_o_responsavel_autoriza` | Aprovado |
| 7. Uma reprodução por sessão | `test_uma_reproducao_por_sessao` | Aprovado |
| 8. Concorrência e reuso de token | `test_requisicoes_simultaneas_na_mesma_aba`, `test_aba_duplicada_com_token_copiado_disputa_e_so_uma_ganha`, `test_mesma_chave_repetida_recebe_mesma_resposta_e_ticket_nao_reusa`, `test_outra_aba_sem_token_e_recarga_nao_reiniciam` | Aprovado |
| 9. Interrupção e falha | `test_falha_de_rede_antes_do_inicio_nao_consome`, `test_falha_depois_do_inicio_fica_interrompida_e_responsavel_decide`, `test_revogacao_*` | Aprovado |
| 10. Pesquisas políticas | `test_v2_rf04_revisao.py` (5 casos) | Aprovado |
| 11. Acessibilidade e responsividade | `test_responsivo_360px_sem_rolagem_lateral` (4 telas), `test_teclado_alcanca_entrar_e_cadastro` | Aprovado (verificação automática básica; sem auditoria WCAG completa) |
| 12. Regressão | `test_regressao.py` (todas as telas e abas de 7 perfis, inclusive o agente) + os 55 testes anteriores | Aprovado |

**Limites dos testes.** Os testes rodam contra o site estático; não há teste de servidor porque não existe servidor. "Chamada direta" é a ação forjada no navegador. A concorrência real entre aparelhos diferentes só pode ser provada com o banco da Trilha S. Neste ambiente, as fontes do Google não carregam e a página usa as fontes de reserva; isso não afeta os testes.

## Etapa 10 — Organização por grupos

A divisão oficial dos 6 grupos e das cores **não está nos materiais do projeto** (repositório, documentos `.md` e arquivo Figma consolidado). O único dado confirmado é que o Grupo 5 é Azul. Para não inventar responsáveis nem cores, toda alteração fica com grupo e cor **pendentes de validação (DP-11)**.

| ID | Requisito | Alteração | Grupo líder | Apoio | Cor | Arquivos | Dependências | Critério de aceite | Testes | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ALT-01 | RF05 | Home, menu e faixa com Entrar e Cadastre-se | Pendente | Pendente | Pendente | `index.html` | — | Entrar e Cadastre-se visíveis; nada de admin na área principal | rf05 | Implementado e testado |
| ALT-02 | RF05 | Tela Entrar sem aba Admin; acesso interno no rodapé | Pendente | Pendente | Pendente | `index.html`, `tests/conftest.py` | — | Admin só pelo acesso interno; conta comum recusada lá | rf05 | Implementado e testado |
| ALT-03 | RF01 | Políticas sem resultados para participante e agente | Pendente | Pendente | Pendente | `index.html` | DP-01 | 403 e ação negada em toda camada | rf01 | Implementado e testado |
| ALT-04 | RF01 | Pedido de acesso do cliente e liberação pelo admin | Pendente | Pendente | Pendente | `index.html`, `tests/test_resultados.py` | — | Sem liberação, sem números; liberação parcial respeitada | rf01 | Implementado e testado |
| ALT-05 | RF03 | Vínculo e login de agente gerado pelo admin | Pendente | Pendente | Pendente | `index.html`, `tests/test_regressao.py` | C-1 (decidido) | Código válido entra; errado ou ausente não | rf03 | Implementado e testado |
| ALT-06 | RF03 | Área do agente, campos autorizados, upload validado | Pendente | Pendente | Pendente | `index.html` | DP-07, DP-14 | Campos extras ignorados; arquivos inválidos recusados | rf03 | Implementado e testado (regras provisórias) |
| ALT-07 | RF03 | Desativação com histórico; substituto sem herança | Pendente | Pendente | Pendente | `index.html` | — | Sem acesso após desativar; histórico intacto | rf03 | Implementado e testado |
| ALT-08 | RF04 | Checagem de sinal, revisão humana, publicação | Pendente | Pendente | Pendente | `index.html` | DP-08, DP-09 | Nada rejeitado ou publicado automaticamente; motivo obrigatório | rf04 | Implementado e testado (política provisória) |
| ALT-09 | RF02 | Armazenamento com trava, estados, idempotência, token, ticket | Pendente | Pendente | Pendente | `index.html` | D-06, DP-03–06, DP-12 | Um início por sessão em toda corrida testada | rf02 | Implementado e testado (navegador) |
| ALT-10 | RF02 | Telas do responsável e do participante | Pendente | Pendente | Pendente | `index.html` | C-4 | Só o responsável concede; admin não assiste | rf02 | Implementado e testado |
| ALT-11 | Todos | Migração V2 e restauração | Pendente | Pendente | Pendente | `index.html` | — | Dados antigos preservados | regressão | Implementado e testado |
| ALT-12 | Todos | Documentação e Figma | Pendente | Pendente | Pendente | `*.md`, Figma | DP-11 | Rastreabilidade RF → tela → teste | — | Concluído |

## Etapa 11 — Entrega

**Arquivos.**

| Arquivo | Situação |
| --- | --- |
| `index.html` | Modificado: bloco V2 (RF01–RF05) antes do roteador, políticas, perfil agente, rotas `ag-*`, filtros de pesquisa publicada, rodapé e estilos |
| `tests/test_v2_rf01_resultados.py`, `test_v2_rf02_audiovisual.py`, `test_v2_rf03_agente.py`, `test_v2_rf04_revisao.py`, `test_v2_rf05_home.py` | Criados (51 testes) |
| `tests/conftest.py`, `test_regressao.py`, `test_resultados.py` | Modificados (login pelo acesso interno, agente na regressão, cliente liberado) |
| `REFATORACAO-V2.md` | Criado (este relatório) |
| `PERMISSOES.md`, `README.md`, `REVERSAO.md`, `SOLICITACOES.md` | Atualizados |
| Removidos | Nenhum |

**Migrações:** `migrarV2` e `migrarAV`, sem perda de dados. Não há migração de banco, porque não existe banco.

**Figma** ("Sinergia — Protótipo Consolidado", página Protótipo):
- Seção nova "Prompt Master V2 · 28/10/2026 (RF01–RF05)" com 13 telas: V2-RF05a–c, V2-RF01a–b, V2-RF03a–b, V2-RF04, V2-RF02a–d e o quadro V2-90.
- Componentes atualizados: menu do administrador (Revisão de pesquisas, Audiovisual, Usuários e acessos) e menu do participante (Exibições presenciais).
- Componente novo: "Menu lateral / Agente terceirizado (V2)".
- A seção antiga do agente foi renomeada como histórico.

**Como rodar e homologar.**

```
pip install pytest playwright
playwright install chromium
pytest -q tests
```

Roteiro de homologação:

1. **RF05.** Abra `index.html`: a home mostra Entrar e Cadastre-se. Entre como administrador pelo link "Acesso interno", no rodapé.
2. **RF01.** Como cliente, com a conta `marina@cinemaalfa.com.br`, peça acesso a uma pesquisa. Como administrador, aprove em *Resultados → Pedidos de clientes*. Volte como cliente e confira que só aquela pesquisa aparece.
3. **RF03.** Entre como agente: `paulo.sena@campo.com.br`, código `CAMPO26`. Crie uma pesquisa, envie um CSV válido e um PDF falso, e mande para revisão. Como administrador, gere o login da Yasmin e depois desative o do Paulo.
4. **RF04.** Em *Revisão de pesquisas*, rejeite a pesquisa de intenção de voto com motivo e aprove e publique a outra.
5. **RF02.** No celular, ou no modo celular do navegador:
   1. Como administrador, gere o código em *Audiovisual → Código do local*.
   2. Como `ana.ribeiro@email.com`, faça o check-in em *Exibições presenciais* e inicie a exibição.
   3. Recarregue a página e confirme que a exibição não reinicia.
6. Aceite da Sinergia, item a item, com base no quadro da Etapa 9.

**Rollback:** veja [REVERSAO.md](REVERSAO.md). O ponto de restauração é a branch `reversao-pre-v2` (`7e0fbbd`).

## Pendências e riscos

| Código | Pendência | Comportamento provisório |
| --- | --- | --- |
| D-06 | Servidor | Regras no navegador; sem garantia contra quem edita o próprio navegador |
| C-4 | Quem é a Claudia | Responsável configurável, hoje a conta Helena Prado |
| DP-01 | Perfis × categorias de resultado | Matriz de 27/10 (assistente de análise com consolidados e respostas por código) |
| DP-03 | Validade da autorização | Campo obrigatório, sem padrão |
| DP-04 | Interrupção depois do início | Estado INTERROMPIDA; o responsável confirma o consumo |
| DP-05 | Nova exibição do mesmo conteúdo | Exige nova autorização |
| DP-06 | Prova de presença | Código do local de 6 dígitos, válido 15 min |
| DP-07 | Upload | CSV, XLSX e PDF; 10 MB; 10 arquivos |
| DP-08 | Quem revisa | Administrador |
| DP-09 | Política de exclusão | Só sinal + decisão humana com motivo |
| DP-10 | Retenção de registros | Sem prazo; limite de volume no navegador |
| DP-11 | Grupos e cores | Pendente em todas as alterações |
| DP-12 | Celular compatível | Tipo de aparelho informado pelo navegador |
| DP-13 | Participante vê as próprias respostas | Mantido |
| DP-14 | Campos autorizados ao agente | Lista da Etapa 4 |

**Riscos.**
- O protótipo não tem senha real nem servidor: não serve para dados reais nem para vídeo real.
- A ordem de merge importa: primeiro o PR #1, depois este.
- Se o `main` for revertido para a versão anterior com os dados da V2 no navegador, as pesquisas de agente em revisão apareceriam ao cliente. Use *Restaurar dados de exemplo* depois de reverter.

# Plano de reversão

## Ponto de restauração

A branch **`reversao-pre-evolucao`** aponta para o commit `87d64a1`, o último antes da evolução de 27/10/2026 (módulos A–E). Ela não deve receber commits.

## Voltar o site publicado para a versão anterior

```
git fetch origin
git checkout main
git revert --no-edit 87d64a1..HEAD     # cria commits que desfazem a evolução, sem reescrever o histórico
git push origin main
```

O GitHub Pages republica em 1–2 minutos.

## Voltar só um arquivo

```
git checkout reversao-pre-evolucao -- index.html
git commit -m "Restaura index.html anterior à evolução" && git push origin main
```

## Dados no navegador

A evolução usa a chave `sinergia-sistema-v4` no `localStorage`. A versão anterior usa `sinergia-sistema-v3` e ignora a v4. Quem voltar para a versão anterior recebe os dados de exemplo dela automaticamente; nenhum dado real é perdido, porque o protótipo só guarda dados de exemplo no próprio navegador.

## Figma

As telas anteriores continuam no arquivo, na seção "Solicitações da cliente · relatório 21/10/2026 (S1–S5)". As telas da evolução ficam numa seção própria ("Evolução 27/10/2026 · módulos A–E"); para reverter, basta apagar ou ocultar essa seção.

## Refatoração de acessos (28/10/2026)

A refatoração está no branch `refatoracao-acessos` e entra no `main` por pull request. Enquanto o PR não for aceito, nada muda no site publicado.

Depois do merge, para voltar:

```
git fetch origin
git checkout main
git revert --no-edit -m 1 <commit do merge do PR>
git push origin main
```

**Dados no navegador.** A chave continua `sinergia-sistema-v4`. A migração não apaga nada: os campos antigos (`admin`, `perms`, `empresa`, `codigo`, `funcao`) continuam gravados em cada conta, agora como reflexo dos vínculos, e os valores de antes da migração ficam em `legado`. A versão anterior lê os campos antigos e ignora `vinculos`, `legado` e `acessos`. Para voltar exatamente ao estado de antes (inclusive vínculos que a migração mandou para revisão), use *Restaurar dados de exemplo* na versão anterior.

**Figma.** As telas novas ficam na seção "Refatoração de acessos · 28/10/2026"; as telas antigas não foram alteradas (há cópias de referência na própria seção). Para reverter, apague ou oculte a seção.

## Prompt Master V2 (28/10/2026, RF01–RF05)

**Ponto de restauração.** A branch `reversao-pre-v2` aponta para `7e0fbbd`, o último commit da refatoração de acessos (PR #1), base desta implementação. Ela não deve receber commits. O `main` publicado continua em `9c057e7` até os merges.

**Como entra.** A V2 está na branch `refatoracao-v2`, num pull request empilhado sobre o PR #1 (base `refatoracao-acessos`). Ordem: aceitar o PR #1, depois mudar a base do PR da V2 para `main` e aceitar.

**Voltar depois do merge.**

```
git fetch origin
git checkout main
git revert --no-edit -m 1 <commit do merge do PR da V2>
git push origin main
```

**Voltar só um requisito.** O código da V2 está num commit só (os RF dividem o mesmo `index.html`). Para retirar um RF sem desfazer os outros, remova o trecho entre as etiquetas `▶ INÍCIO · RFxx` e `■ FIM · RFxx` do bloco V2 e as linhas marcadas `RFxx (V2)`, rode a suíte e abra outro pull request. O mapa das etiquetas está em `SOLICITACOES.md`.

**Dados no navegador.** A chave continua `sinergia-sistema-v4` (mesmo padrão do PR #1): a migração `migrarV2` acrescenta campos e não apaga nada. A versão anterior ignora `solicRes`, `v2`, `arquivos`, `revisao` e o vínculo de agente (sem papel na versão anterior, a conta fica sem acesso). Atenção: a versão anterior mostraria ao cliente as pesquisas de agente em revisão, porque só escondia "Rascunho". Depois de reverter, use *Restaurar dados de exemplo*. O audiovisual fica em outra chave (`sinergia-av-v1`), que a versão anterior não lê; para limpar, apague essa chave no navegador ou restaure os dados de exemplo na V2 antes de reverter.

**Figma.** As telas da V2 ficam na seção própria "Prompt Master V2 · 28/10/2026 (RF01–RF05)"; telas antigas não foram apagadas. Para reverter, apague ou oculte a seção.

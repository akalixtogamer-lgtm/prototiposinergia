"""V2 · RF02 — autorização individual e reprodução única de filmes e trailers.
Roda num contexto de celular (agente de usuário de iPhone, toque). O armazenamento do audiovisual fica numa chave
separada, lida e gravada dentro de uma trava exclusiva entre abas (Web Locks), que faz o papel da transação do banco.
Cobre: autorização verificada antes de liberar, dispositivo, check-in, uma reprodução por sessão, recarga, abas
duplicadas, requisições simultâneas e repetidas, reuso de token e de ticket, falha de rede antes e depois do início,
revogação, expiração e o que fica registrado (sem token)."""
import json
import pytest
from conftest import App, URL, ADMIN, PARTICIPANTE

IPHONE = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
AVK = 'sinergia-av-v1'


@pytest.fixture
def ctx(browser):
    c = browser.new_context(user_agent=IPHONE, viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
    yield c
    c.close()


def nova_app(ctx, limpar=False):
    page = ctx.new_page(); a = App(page)
    page.on('pageerror', lambda e: a.erros.append('PAGE: ' + str(e)))
    page.on('console', lambda m: a.erros.append('CONSOLE: ' + m.text) if m.type == 'error' and 'ERR_' not in m.text else None)
    page.goto(URL + '#home')
    if limpar: page.evaluate('localStorage.clear()'); page.reload()
    page.wait_for_timeout(300)
    return a


@pytest.fixture
def cel(ctx):
    a = nova_app(ctx, limpar=True)
    a.estado('S.config.avDemoSeg=2')  # exibição curta nos testes
    yield a
    assert not a.erros, '\n'.join(a.erros)


def av(app):
    return app.p.evaluate(f"JSON.parse(localStorage.getItem('{AVK}'))")


def eventos(app, nome):
    return [e for e in av(app)['eventos'] if e['evento'] == nome]


def codigo_local(app):
    app.login(ADMIN, 'admin'); app.ir('adm-audiovisual', 250)
    app.p.click('[data-k="avTab"][data-v="cod"]'); app.p.wait_for_timeout(150)
    app.p.click('[data-act="av-codigo"]'); app.p.wait_for_timeout(300)
    return app.p.inner_text('#av-cod-valor')


def aba_autorizacoes(app):
    app.ir('adm-audiovisual', 250); app.p.click('[data-k="avTab"][data-v="aut"]'); app.p.wait_for_timeout(200)


def checkin(app, codigo):
    app.login(PARTICIPANTE); app.ir('pa-exibicoes', 300)
    app.p.fill('form[data-form="av-checkin"] input[name=codigo]', codigo)
    app.p.click('form[data-form="av-checkin"] button[type=submit]'); app.p.wait_for_timeout(400)


def sessao(app):
    return av(app)['sessoes'][-1]


def test_sem_celular_nao_inicia(app):
    # contexto de computador (fixture app): o check-in é recusado pelo dispositivo
    cod = codigo_local(app); checkin(app, cod)
    assert app.p.locator('[data-av="dispositivo"]').count() == 1 and av(app)['sessoes'] == []


def test_sem_autorizacao_ou_codigo_errado_nao_cria_sessao(cel):
    cod = codigo_local(cel)
    cel.login('joao.tadeu@sinergia.com.br'); cel.ir('pa-exibicoes', 300)
    assert 'não tem autorizações' in cel.main()
    # formulário forjado com a autorização da Ana: o servidor confere o dono da autorização
    cel.p.evaluate("document.body.insertAdjacentHTML('beforeend','<div class=av-card><div class=av-msg></div><form data-form=av-checkin data-aut=au-demo1 id=fx><input name=codigo value=\"'+arguments_cod+'\"><button id=fxb>ok</button></form></div>')".replace('arguments_cod', cod))
    cel.p.click('#fxb'); cel.p.wait_for_timeout(400)
    assert av(cel)['sessoes'] == [] and eventos(cel, 'checkin_recusado')
    checkin(cel, '000000')
    assert cel.p.locator('[data-av="checkin"]').count() == 1 and av(cel)['sessoes'] == []


def test_uma_reproducao_por_sessao(cel):
    checkin(cel, codigo_local(cel))
    assert sessao(cel)['estado'] == 'AUTORIZADA'
    cel.p.click('[data-act="av-iniciar"]'); cel.p.wait_for_timeout(3800)
    assert sessao(cel)['estado'] == 'CONSUMIDA'
    assert cel.p.locator('[data-act="av-iniciar"]').count() == 0
    sid = sessao(cel)['id']
    cel.forjar('av-iniciar', sid=sid); cel.p.wait_for_timeout(300)
    assert sessao(cel)['estado'] == 'CONSUMIDA' and len(eventos(cel, 'inicio_aceito')) == 1
    assert eventos(cel, 'tentativa_repetida')
    # nova exibição exige nova autorização (provisório, DP-05): novo check-in com a mesma autorização é recusado
    cel.ir('pa-exibicoes', 250); assert cel.p.locator('form[data-form="av-checkin"]').count() == 0


def test_requisicoes_simultaneas_na_mesma_aba(cel):
    checkin(cel, codigo_local(cel)); sid = sessao(cel)['id']
    # dois pedidos de início disparados no mesmo instante, com chaves diferentes
    cel.p.evaluate("""sid=>{for(const k of ['a1','a2']){const b=document.createElement('button');b.dataset.act='av-iniciar';b.dataset.sid=sid;b.dataset.idem='k-'+k;document.body.appendChild(b)}
      document.querySelectorAll('button[data-idem^="k-"]').forEach(b=>b.click())}""", sid)
    cel.p.wait_for_timeout(1500)
    assert len(eventos(cel, 'inicio_aceito')) == 1 and len(eventos(cel, 'tentativa_repetida')) >= 1


def test_aba_duplicada_com_token_copiado_disputa_e_so_uma_ganha(cel, ctx):
    checkin(cel, codigo_local(cel)); sid = sessao(cel)['id']
    tok = cel.p.evaluate(f"sessionStorage.getItem('sinergia-av-tok-{sid}')")
    outra = nova_app(ctx); outra.p.evaluate(f"sessionStorage.setItem('sinergia-av-tok-{sid}','{tok}')"); outra.ir('pa-exibicoes', 300)
    js = "sid=>{const b=document.createElement('button');b.dataset.act='av-iniciar';b.dataset.sid=sid;document.body.appendChild(b);b.click()}"
    cel.p.evaluate(js, sid); outra.p.evaluate(js, sid)  # as duas abas pedem quase ao mesmo tempo
    cel.p.wait_for_timeout(1500)
    assert len(eventos(cel, 'inicio_aceito')) == 1


def test_outra_aba_sem_token_e_recarga_nao_reiniciam(cel, ctx):
    checkin(cel, codigo_local(cel)); sid = sessao(cel)['id']
    outra = nova_app(ctx); outra.ir('pa-exibicoes', 300)
    assert outra.p.locator('[data-act="av-iniciar"]').count() == 0  # sem o token desta aba, o botão nem aparece
    outra.forjar('av-iniciar', sid=sid); outra.p.wait_for_timeout(300)
    assert eventos(cel, 'token_recusado') and sessao(cel)['estado'] == 'AUTORIZADA'
    # inicia e recarrega a página no meio da exibição
    cel.estado('S.config.avDemoSeg=30')
    cel.ir('pa-exibicoes', 300); cel.p.click('[data-act="av-iniciar"]'); cel.p.wait_for_timeout(900)
    cel.p.reload(); cel.p.wait_for_timeout(500)
    assert cel.p.locator('[data-act="av-iniciar"]').count() == 0 and 'não é possível reiniciar' in cel.main().lower()
    cel.forjar('av-iniciar', sid=sid); cel.p.wait_for_timeout(300)
    assert len(eventos(cel, 'inicio_aceito')) == 1
    # sem sinal do aparelho depois do início: fica Interrompida (DP-04), nunca volta a Autorizada
    cel.p.wait_for_timeout(8600); cel.ir('pa-pesquisas', 200); cel.ir('pa-exibicoes', 800)
    assert sessao(cel)['estado'] == 'INTERROMPIDA'


def test_mesma_chave_repetida_recebe_mesma_resposta_e_ticket_nao_reusa(cel):
    checkin(cel, codigo_local(cel)); sid = sessao(cel)['id']
    cel.estado('S.config.avDemoSeg=30'); cel.ir('pa-exibicoes', 300)
    js = "sid=>{const b=document.createElement('button');b.dataset.act='av-iniciar';b.dataset.sid=sid;b.dataset.idem='mesma-chave';document.body.appendChild(b);b.click()}"
    cel.p.evaluate(js, sid); cel.p.wait_for_timeout(700)
    cel.p.evaluate(js, sid); cel.p.wait_for_timeout(700)  # reenvio da mesma requisição
    assert len(eventos(cel, 'inicio_aceito')) == 1 and eventos(cel, 'requisicao_repetida') and eventos(cel, 'ticket_recusado')


def test_falha_de_rede_antes_do_inicio_nao_consome(cel, ctx):
    checkin(cel, codigo_local(cel))
    ctx.set_offline(True)
    cel.p.click('[data-act="av-iniciar"]'); cel.p.wait_for_timeout(600)
    ctx.set_offline(False)
    s = sessao(cel)
    assert s['estado'] == 'AUTORIZADA' and s['falhasPre'] == 1 and eventos(cel, 'falha_pre_inicio')
    cel.ir('pa-exibicoes', 300); cel.p.click('[data-act="av-iniciar"]'); cel.p.wait_for_timeout(3800)
    assert sessao(cel)['estado'] == 'CONSUMIDA'


def test_falha_depois_do_inicio_fica_interrompida_e_responsavel_decide(cel, ctx):
    checkin(cel, codigo_local(cel)); cel.estado('S.config.avDemoSeg=30'); cel.ir('pa-exibicoes', 300)
    cel.p.click('[data-act="av-iniciar"]'); cel.p.wait_for_timeout(800)
    ctx.set_offline(True); cel.p.wait_for_timeout(1200); ctx.set_offline(False)
    assert sessao(cel)['estado'] == 'INTERROMPIDA'
    cel.ir('pa-exibicoes', 300); assert cel.p.locator('[data-act="av-iniciar"]').count() == 0
    cel.login(ADMIN, 'admin'); aba_autorizacoes(cel)
    cel.p.click('[data-act="av-interrupcao"]'); cel.p.wait_for_timeout(400)
    assert sessao(cel)['estado'] == 'CONSUMIDA' and eventos(cel, 'interrupcao_decidida')


def test_revogacao_e_expiracao(cel):
    cod = codigo_local(cel)
    aba_autorizacoes(cel); cel.p.click('[data-act="av-revogar"]'); cel.p.wait_for_timeout(150)
    cel.p.fill('#mot', 'Participante pediu para sair do estudo'); cel.p.click('#mot-ok'); cel.p.wait_for_timeout(400)
    cel.login(PARTICIPANTE); cel.ir('pa-exibicoes', 300)
    assert cel.p.locator('form[data-form="av-checkin"]').count() == 0  # revogada: sem check-in
    assert 'revogada' in cel.main().lower()
    # expiração: autorização nova com validade já vencida no registro
    cel.p.evaluate(f"""()=>{{const d=JSON.parse(localStorage.getItem('{AVK}'));const a={{...d.autorizacoes[0],id:'au-venc',revogadaEm:null,validaAte:new Date(Date.now()-60000).toISOString()}};d.autorizacoes.push(a);localStorage.setItem('{AVK}',JSON.stringify(d))}}""")
    cel.p.evaluate("document.body.insertAdjacentHTML('beforeend','<div class=av-card><div class=av-msg></div><form data-form=av-checkin data-aut=au-venc id=fx><input name=codigo value=\"%s\"><button id=fxb>ok</button></form></div>')" % cod)
    cel.p.click('#fxb'); cel.p.wait_for_timeout(400)
    assert cel.p.locator('[data-av="expirada"]').count() == 1


def test_revogacao_durante_sessao_autorizada(cel):
    cod = codigo_local(cel); checkin(cel, cod)
    cel.login(ADMIN, 'admin'); aba_autorizacoes(cel); cel.p.click('[data-act="av-revogar"]'); cel.p.wait_for_timeout(150)
    cel.p.fill('#mot', 'Conteúdo retirado do estudo pelo cliente'); cel.p.click('#mot-ok'); cel.p.wait_for_timeout(400)
    assert sessao(cel)['estado'] == 'REVOGADA'


def test_registro_tem_ids_e_horarios_sem_token(cel):
    checkin(cel, codigo_local(cel)); sid = sessao(cel)['id']
    tok = cel.p.evaluate(f"sessionStorage.getItem('sinergia-av-tok-{sid}')")
    cel.p.click('[data-act="av-iniciar"]'); cel.p.wait_for_timeout(3800)
    d = av(cel); s = d['sessoes'][-1]
    assert s['uid'] and s['conteudoId'] == 'ct1' and s['criadaEm'] and s['iniciadaEm'] and s['encerradaEm'] and s['estado'] == 'CONSUMIDA'
    evs = [e for e in d['eventos'] if e['sessaoId'] == sid]
    assert {'sessao_criada', 'inicio_aceito', 'primeiro_trecho', 'fim'} <= {e['evento'] for e in evs}
    assert all(e['id'] and e['t'] and e['uid'] == s['uid'] for e in evs)
    bruto = json.dumps(d)
    assert tok not in bruto and 'ana.ribeiro' not in bruto  # sem token e sem e-mail no registro


def test_so_o_responsavel_autoriza(cel):
    cel.login('marcos@sinergia.com.br', 'admin'); aba_autorizacoes(cel)
    assert cel.p.locator('form[data-form="av-aut"]').count() == 0 and 'Só' in cel.main()
    antes = len(av(cel)['autorizacoes'])
    cel.p.evaluate("document.body.insertAdjacentHTML('beforeend','<form data-form=av-aut id=fx><input name=av-uid value=u5><input name=av-ct value=ct2><input name=av-ate value=2030-01-01T10:00><div id=av-err></div><button id=fxb>ok</button></form>')")
    cel.p.click('#fxb'); cel.p.wait_for_timeout(400)
    assert len(av(cel)['autorizacoes']) == antes
    # o administrador não assiste: a área do participante é negada
    cel.ir('pa-exibicoes', 250); assert cel.hash() == '#negado'


def test_responsavel_concede_com_validade_obrigatoria(cel):
    cel.login(ADMIN, 'admin'); aba_autorizacoes(cel)
    cel.p.select_option('#av-ct', 'ct2'); cel.p.click('form[data-form="av-aut"] button[type=submit]'); cel.p.wait_for_timeout(300)
    assert len(av(cel)['autorizacoes']) == 1  # sem validade, nada é concedido
    cel.p.fill('#av-ate', '2030-01-01T10:00'); cel.p.click('form[data-form="av-aut"] button[type=submit]'); cel.p.wait_for_timeout(400)
    a = av(cel)['autorizacoes'][-1]
    assert a['conteudoId'] == 'ct2' and a['concedidaPorNome'] == 'Helena Prado' and eventos(cel, 'autorizacao_concedida')

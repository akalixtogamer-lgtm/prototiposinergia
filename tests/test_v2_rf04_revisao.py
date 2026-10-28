"""V2 · RF04 (com RF03) — escopo sem política e revisão humana.
A checagem automática só sinaliza (tema declarado e termos no nome e na descrição); nunca rejeita nem publica sozinha.
A revisão humana decide com motivo registrado; só o administrador publica; casos ambíguos ficam na fila."""
from conftest import ADMIN
from test_v2_rf03_agente import AGENTE, CODIGO, nova_pesquisa


def revisar(app, pid, decisao, motivo=''):
    app.ir('adm-revisao', 250); app.p.click(f'[data-act="rv-abrir"][data-id="{pid}"]'); app.p.wait_for_timeout(200)
    if motivo: app.p.fill('#rv-mot', motivo)
    app.p.click(f'.modal [data-act="rv-decidir"][data-d="{decisao}"]'); app.p.wait_for_timeout(250)


def test_sinal_politico_vai_para_revisao_humana(app):
    app.login(AGENTE, senha=CODIGO)
    a = nova_pesquisa(app, nome='Tema declarado como política', tema='Política, eleições ou governo')
    app.p.click('[data-act="ag-enviar"]'); app.p.wait_for_timeout(250)
    b = nova_pesquisa(app, nome='Saída do cinema e voto', desc='Medir intenção de voto para prefeito na saída da sessão.')
    app.p.click('[data-act="ag-enviar"]'); app.p.wait_for_timeout(250)
    c = nova_pesquisa(app, nome='Documentário sobre cinema nacional', desc='Avaliar o trailer de um documentário sobre a história do cinema.')
    app.p.click('[data-act="ag-enviar"]'); app.p.wait_for_timeout(250)
    assert app.st(f"P('{a}').revisao.sinais.length") >= 1 and app.st(f"P('{b}').revisao.sinais.length") >= 1
    assert app.st(f"P('{c}').revisao.sinais.length") == 0
    # nenhuma decisão automática: todas ficam em revisão
    assert {app.st(f"P('{x}').status") for x in (a, b, c)} == {'Em revisão'}


def test_aprovar_com_sinal_exige_justificativa_e_rejeitar_exige_motivo(app):
    app.login(ADMIN, 'admin')
    revisar(app, 'pg2', 'aprovar')
    assert app.p.locator('#rv-err:visible').count() == 1 and app.st("P('pg2').status") == 'Em revisão'
    app.p.fill('#rv-mot', 'curto'); app.p.click('.modal [data-act="rv-decidir"][data-d="rejeitar"]'); app.p.wait_for_timeout(200)
    assert app.st("P('pg2').status") == 'Em revisão'
    app.p.fill('#rv-mot', 'Intenção de voto é pesquisa eleitoral: fora do escopo da Sinergia.')
    app.p.click('.modal [data-act="rv-decidir"][data-d="rejeitar"]'); app.p.wait_for_timeout(250)
    assert app.st("P('pg2').status") == 'Rejeitada'
    assert app.st("P('pg2').revisao.hist.slice(-1)[0].motivo").startswith('Intenção de voto')
    # o agente vê o motivo de forma compreensível
    app.login(AGENTE, senha=CODIGO); app.estado("S.ui.agPid='pg2'"); app.ir('ag-pesquisa', 250)
    assert 'Rejeitada:' in app.main() and 'fora do escopo' in app.main()


def test_aprovacao_e_publicacao_so_pelo_admin(app):
    app.login(ADMIN, 'admin')
    revisar(app, 'pg1', 'aprovar')  # sem sinal: aprovar sem motivo é permitido
    assert app.st("P('pg1').status") == 'Aprovada'
    app.ir('adm-revisao', 250); app.p.click('[data-act="rv-publicar"][data-id="pg1"]'); app.p.wait_for_timeout(150)
    app.p.click('#cfm'); app.p.wait_for_timeout(250)
    assert app.st("P('pg1').status") == 'Ativa'
    assert [h['acao'] for h in app.st("P('pg1').revisao.hist")][-2:] == ['Aprovada na revisão', 'Publicada']


def test_devolver_permite_ajuste_e_reenvio(app):
    app.login(ADMIN, 'admin'); revisar(app, 'pg1', 'devolver', 'Informe o local exato da aplicação e a amostra.')
    assert app.st("P('pg1').status") == 'Devolvida'
    app.login(AGENTE, senha=CODIGO); app.ir('ag-pesquisas', 250)
    assert 'local exato' in app.main()
    app.estado("S.ui.agPid='pg1'"); app.ir('ag-pesquisa', 250)
    app.p.fill('#agp-local', 'Shopping Tijuca, saída das salas 3 e 4'); app.p.click('form[data-form="ag-pesq"] button[type=submit]'); app.p.wait_for_timeout(250)
    app.p.click('[data-act="ag-enviar"]'); app.p.wait_for_timeout(250)
    assert app.st("P('pg1').status") == 'Em revisão'


def test_formulario_antigo_nao_muda_situacao_de_pesquisa_de_agente(app):
    app.login(ADMIN, 'admin'); app.ir('adm-pesquisas', 250)
    app.forjar('editar-pesquisa', id='pg2'); assert app.hash() == '#adm-revisao'
    # formulário forjado do administrador tentando ativar direto
    app.p.evaluate("document.body.insertAdjacentHTML('beforeend','<form data-form=pesquisa data-id=pg2 id=fx><select name=status><option>Ativa</option></select><button id=fxb>ok</button></form>')")
    app.p.click('#fxb'); app.p.wait_for_timeout(250)
    assert app.st("P('pg2').status") == 'Em revisão'

"""Testes funcionais dos módulos A, B, C e D (evolução de 27/10/2026)."""
from conftest import ADMIN, PARTICIPANTE, TRANSCRICAO

def test_A1_importacao_so_em_pesquisas(app):
    app.login(ADMIN, 'admin')
    app.ir('adm-projetos'); assert 'Importar' not in app.main()
    app.p.click('[data-act="abrir-projeto"]'); app.p.wait_for_timeout(250); assert 'Importar' not in app.main()
    app.ir('adm-pesquisas'); app.p.click('[data-act="importar-abrir"]'); app.p.wait_for_timeout(150)
    assert app.p.locator('.imp-op').count() == 2

def test_A2_importar_respostas_csv(app):
    app.login(ADMIN, 'admin'); antes = app.st("P('p1').resp")
    app.ir('adm-pesquisas'); app.p.click('[data-act="importar-abrir"]'); app.p.click('[data-act="imp-resp-abrir"]'); app.p.wait_for_timeout(150)
    app.p.select_option('#ir-pesq', 'p1'); app.p.click('[data-act="ir-modelo"]'); app.p.click('button[form="f-ir"]'); app.p.wait_for_timeout(250)
    assert app.st("P('p1').resp") == antes + 2
    app.p.click('[data-act="set"][data-v="imp"]'); app.p.wait_for_timeout(150); assert 'linhas coladas' in app.main()

def test_A2_importacao_invalida_mostra_erro(app):
    app.login(ADMIN, 'admin'); app.ir('adm-pesquisas')
    app.p.click('[data-act="importar-abrir"]'); app.p.click('[data-act="imp-resp-abrir"]'); app.p.wait_for_timeout(150)
    app.p.fill('#ir-txt', 'linha;sem;data'); app.p.click('button[form="f-ir"]'); app.p.wait_for_timeout(150)
    assert app.p.is_visible('#ir-err') and 'Nenhuma linha válida' in app.p.inner_text('#ir-err')

def test_A3_respostas_detalhadas_com_filtro(app):
    app.login(ADMIN, 'admin'); app.ir('adm-resultados'); app.p.click('[data-act="set"][data-v="det"]'); app.p.wait_for_timeout(200)
    app.p.select_option('[data-key="admDetD"]', 'Cedido pela Sinergia'); app.p.wait_for_timeout(200)
    col = app.p.locator('#part-det-adm tbody tr td:nth-child(5)').all_inner_texts()
    assert col and all(c == 'Cedido pela Sinergia' for c in col)
    assert 'P-' in app.p.inner_text('#part-det-adm') and '@' not in app.p.inner_text('#part-det-adm')  # só código, sem e-mail

def test_B3_B4_documentos_opcionais_e_configuraveis(app):
    app.login(ADMIN, 'admin'); app.ir('adm-projetos'); app.p.click('[data-act="abrir-projeto"]'); app.p.wait_for_timeout(200)
    app.p.click('[data-act="set"][data-v="documentos"]'); app.p.wait_for_timeout(150)
    t = app.main()
    for d in ['Briefing do cliente', 'Termo de confidencialidade', 'Proposta ou contrato', 'Questionário ou roteiro']: assert d in t
    assert 'Obrigatório' not in t
    app.p.click('[data-act="doc-config"]'); app.p.click('[data-act-change="doc-obrig"][data-id="d2"]'); app.p.wait_for_timeout(150); app.p.click('.modal-bg [data-act="close"]')
    app.ir('adm-projetos'); app.p.click('[data-act="novo-projeto"]'); app.p.fill('#pnome', 'Projeto teste'); app.p.fill('#pdesc', 'x')
    app.p.click('button[form="f-proj"]'); app.p.wait_for_timeout(150)
    assert app.p.is_visible('#pj-err') and 'Termo de confidencialidade' in app.p.inner_text('#pj-err')
    app.p.set_input_files('[data-pdoc="d2"]', files=[{'name': 'nda.pdf', 'mimeType': 'application/pdf', 'buffer': b'%PDF-1.4'}])
    app.p.click('button[form="f-proj"]'); app.p.wait_for_timeout(200)
    assert app.st("S.projetos[0].nome") == 'Projeto teste' and app.st("S.projetos[0].docs.d2.arq") == 'nda.pdf'

def test_B5_ciclo_e_historico_do_convite(app):
    app.login(ADMIN, 'admin'); app.ir('adm-convites')
    cid = app.st("S.convites.find(c=>c.status==='Enviado').id")
    app.p.click(f'[data-act="reenviar"][data-id="{cid}"]'); app.p.wait_for_timeout(150)
    app.p.click(f'[data-act="conv-det"][data-id="{cid}"]'); app.p.wait_for_timeout(150)
    assert app.p.locator('.modal-bg .ciclo li.on').count() == 1 and 'Reenviado' in app.p.inner_text('.modal-bg')

def test_C1_C4_paginacao_e_selecao_em_massa(app):
    app.login(ADMIN, 'admin'); app.ir('adm-cadastros')
    total = app.st("S.participantes.length"); assert total > 10
    assert f'Mostrando 1–10 de {total}' in app.main()
    app.p.check('[data-act-change="sel-pag"]'); app.p.wait_for_timeout(150)
    assert '10 selecionado(s)' in app.p.inner_text('.selbar')
    app.p.click('[data-act="sel-filtrados"]'); app.p.wait_for_timeout(150)
    assert f'{total} selecionado(s)' in app.p.inner_text('.selbar')
    app.p.click('[data-act="bulk-conv"]'); app.p.wait_for_timeout(150)
    assert 'convite(s)' in app.p.inner_text('#bc-ok'); app.p.click('.modal-bg [data-act="close"]')
    app.p.select_option('[data-key="cadReg"]', 'Zona Sul'); app.p.wait_for_timeout(200)
    assert app.p.locator('.selbar').count() == 0 and 'seleção foi limpa' in app.main()
    n = app.st("S.participantes.filter(x=>x.regiao==='Zona Sul').length"); assert 0 < n < total
    assert set(app.p.locator('#part-cad tbody tr td:nth-child(4)').all_inner_texts()) == {'Zona Sul'}

def test_C2_filtro_por_projeto(app):
    app.login(ADMIN, 'admin'); app.ir('adm-cadastros')
    app.p.select_option('[data-key="cadProj"]', 'pj1'); app.p.wait_for_timeout(200)
    cods = app.p.locator('#part-cad tbody tr td:nth-child(2)').all_inner_texts()
    assert cods and app.st("S.convites.filter(c=>c.status!=='Cancelado'&&P(c.pid)&&P(c.pid).projeto==='pj1').map(c=>c.cod)") and all(app.st(f"S.convites.some(c=>c.cod==='{c}'&&c.status!=='Cancelado'&&P(c.pid)&&P(c.pid).projeto==='pj1')") for c in cods)

def test_C6_dispositivo_obrigatorio_no_envio(app):
    app.login(PARTICIPANTE); app.ir('pa-pesquisas')
    app.p.locator('[data-act="pa-start"]').first.click(); app.p.wait_for_timeout(250)
    if app.hash() == '#pa-preferencias':
        app.p.locator('[data-act="pref-gen"]').first.click(); app.p.click('[data-act="pref-ini"]'); app.p.wait_for_timeout(250)
    for _ in range(10):
        if app.hash() == '#pa-revisao': break
        app.p.locator('[data-act="pa-ans"]').first.click(); app.p.click('[data-act="pa-next"]'); app.p.wait_for_timeout(150)
    assert app.hash() == '#pa-revisao'
    app.p.click('[data-act="pa-send"]'); app.p.wait_for_timeout(150)
    assert app.hash() == '#pa-revisao' and app.p.is_visible('#disp-err')
    app.p.check('input[name="disp"][value="Cedido pelo local de aplicação"]'); app.p.click('[data-act="pa-send"]'); app.p.wait_for_timeout(250)
    assert app.hash() == '#pa-concluida' and app.st("S.respostasDet.at(-1).dispositivo") == 'Cedido pelo local de aplicação'

def test_D1_reuniao_so_por_link_externo(app):
    app.login(ADMIN, 'admin'); app.ir('adm-focus'); app.p.click('[data-act="fg-nova"]'); app.p.wait_for_timeout(150)
    app.p.fill('#fgnome', 'Teste link'); app.p.fill('#fgdata', '2026-11-05'); app.p.check('[name="cv:P-1027"]'); app.p.check('[name="cv:P-1031"]')
    app.p.fill('#fglink', 'https://zoom.us/j/123'); app.p.click('button[form="f-fg"]'); app.p.wait_for_timeout(150)
    assert 'Link inválido' in app.p.inner_text('#fg-err')
    app.p.fill('#fglink', 'https://meet.google.com/abc-defg-hij'); app.p.click('button[form="f-fg"]'); app.p.wait_for_timeout(200)
    a = app.p.locator('a[data-ext="reuniao"]').first
    assert a.get_attribute('target') == '_blank' and 'noopener' in a.get_attribute('rel')
    assert app.st("S.focus[0].link") == 'https://meet.google.com/abc-defg-hij'

def test_D_sem_chat_nem_video_simulado(app):
    app.login(ADMIN, 'admin'); fid = app.st("S.focus.find(f=>f.status==='Em andamento').id")
    app.entrar_sala(fid)
    t = app.main(); assert 'Transcrição ao vivo: indisponível' in t
    assert app.p.locator('.chat-form, video').count() == 0

def test_D3_transcricao_nao_e_gerada(app):
    app.login(ADMIN, 'admin'); fid = app.st("S.focus.find(f=>f.status==='Em andamento').id")
    app.entrar_sala(fid)
    app.p.click('[data-act="fg-encerrar"]'); app.p.click('#cfm'); app.p.wait_for_timeout(200)
    assert app.st(f"FG('{fid}').transcricao.status") == 'Aguardando transcrição' and app.st(f"FG('{fid}').transcricao.texto") == ''
    app.login(TRANSCRICAO); app.ir('eq-transcricoes'); app.p.click(f'[data-act="eq-acao"][data-id="{fid}"]'); app.p.wait_for_timeout(150)
    app.p.click('#tx-ok'); app.p.wait_for_timeout(100); assert app.p.is_visible('#tx-err')
    app.p.set_input_files('#tx-file', files=[{'name': 'reuniao.vtt', 'mimeType': 'text/vtt', 'buffer': 'WEBVTT\n\n00:00:01.000 --> 00:00:04.000\n<v Moderadora>Bem-vindos.\n'.encode()}])
    app.p.wait_for_timeout(200); app.p.click('#tx-ok'); app.p.wait_for_timeout(200)
    assert app.st(f"FG('{fid}').transcricao.status") == 'Transcrita' and 'Moderadora: Bem-vindos.' in app.st(f"FG('{fid}').transcricao.texto")

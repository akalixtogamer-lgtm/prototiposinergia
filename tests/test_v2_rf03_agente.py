"""V2 · RF03 — perfil de agente terceirizado.
O administrador confere o cadastro do agente, gera o login (vínculo de agente + código de acesso); o agente
estrutura pesquisas, envia arquivos validados e manda para revisão; não vê resultados nem pesquisas de outros
agentes, não publica; desativar o login corta o acesso e mantém o histórico; o substituto não herda nada."""
import io, zipfile
import pytest
from conftest import ADMIN

AGENTE = 'paulo.sena@campo.com.br'
CODIGO = 'CAMPO26'


def gerar_login(app, ag_id):
    app.login(ADMIN, 'admin'); app.ir('adm-cadastros', 200)
    app.p.click('[data-k="cadTab"][data-v="agentes"]'); app.p.wait_for_timeout(200)
    app.p.click(f'[data-act="ag-gerar"][data-id="{ag_id}"]'); app.p.wait_for_timeout(150)
    app.p.click('#ag-go'); app.p.wait_for_timeout(100)
    assert app.p.locator('#ag-err:visible').count() == 1  # sem conferir os dados não gera
    app.p.check('#ag-ok'); app.p.click('#ag-go'); app.p.wait_for_timeout(250)
    codigo = app.p.inner_text('#ag-cod'); app.p.click('.modal [data-act="close"]')
    return codigo


def nova_pesquisa(app, nome='Pesquisa de campo do agente', tema='Cinema e audiovisual', desc='Avaliar sessão de pré-estreia.'):
    app.ir('ag-pesquisas', 250); app.p.click('[data-act="ag-nova"]'); app.p.wait_for_timeout(250)
    app.p.fill('#agp-nome', nome); app.p.select_option('#agp-tema', tema); app.p.fill('#agp-desc', desc)
    app.p.fill('#agp-ini', '2026-12-01'); app.p.fill('#agp-fim', '2026-12-10'); app.p.fill('#agp-meta', '40')
    app.p.click('form[data-form="ag-pesq"] button[type=submit]'); app.p.wait_for_timeout(300)
    return app.st(f"S.pesquisas.find(p=>p.nome==='{nome}').id")


def subir(app, tmp_path, nome, conteudo):
    f = tmp_path / nome; f.write_bytes(conteudo)
    app.p.set_input_files('#ag-up', str(f)); app.p.wait_for_timeout(500)
    return app.p.inner_text('#ag-up-msg')


def xlsx_valido():
    b = io.BytesIO()
    with zipfile.ZipFile(b, 'w') as z:
        z.writestr('[Content_Types].xml', '<?xml version="1.0"?><Types/>'); z.writestr('xl/workbook.xml', '<workbook/>')
    return b.getvalue()


def test_admin_gera_login_e_agente_entra_com_codigo(app):
    codigo = gerar_login(app, 'a3')  # Victor Alves
    assert len(codigo) == 8 and app.st("S.users.find(u=>u.email==='victor@sinergia.com.br').codigoHash") != codigo
    app.login('victor@sinergia.com.br', senha='ERRADO99'); assert 'Código de acesso incorreto' in app.p.inner_text('#l-err')
    app.login('victor@sinergia.com.br', senha=codigo); assert app.hash() == '#ag-pesquisas'
    assert app.st("S.auditoria.some(a=>a.acao==='Login de agente gerado'&&a.alvo==='Victor Alves')")


def test_agente_preenche_so_campos_autorizados(app):
    app.login(AGENTE, senha=CODIGO)
    app.ir('ag-pesquisas', 250); app.p.click('[data-act="ag-nova"]'); app.p.wait_for_timeout(250)
    app.p.fill('#agp-nome', 'Campo com campo forjado'); app.p.fill('#agp-ini', '2026-12-01'); app.p.fill('#agp-fim', '2026-12-05')
    app.p.evaluate("document.querySelector('form[data-form=ag-pesq]').insertAdjacentHTML('beforeend','<input type=hidden name=status value=Ativa><input type=hidden name=cliente value=Outra><input type=hidden name=criadoPor value=u1>')")
    app.p.click('form[data-form="ag-pesq"] button[type=submit]'); app.p.wait_for_timeout(300)
    p = app.st("(({status,criadoPor,origem})=>({status,criadoPor,origem}))(S.pesquisas.find(p=>p.nome==='Campo com campo forjado'))")
    assert p == {'status': 'Rascunho', 'criadoPor': 'u-ag1', 'origem': 'agente'}


def test_upload_valido_e_invalidos(app, tmp_path):
    app.login(AGENTE, senha=CODIGO); pid = nova_pesquisa(app)
    assert 'aceito' in subir(app, tmp_path, 'amostra.csv', 'codigo;idade\nP-1;30\nP-2;-5\n'.encode())
    assert 'aceito' in subir(app, tmp_path, 'roteiro.pdf', b'%PDF-1.4\n1 0 obj<<>>endobj\n%%EOF\n')
    assert 'aceito' in subir(app, tmp_path, 'base.xlsx', xlsx_valido())
    casos = {
        'programa.exe': (b'MZ\x90\x00', 'Tipo não permitido'),
        'falso.pdf': (b'isto nao e um pdf', 'não é um PDF'),
        'falsa.xlsx': (b'texto qualquer', 'não é uma planilha'),
        'formula.csv': ('nome;valor\n=HYPERLINK("x");1\n'.encode(), 'fórmulas'),
        'vazio.csv': (b'', 'vazio'),
        'binario.csv': (b'a;b\n\x00\x01;2\n', 'binário'),
        'latin1.csv': ('nome;cidade\nJoão;São Paulo\n'.encode('latin-1'), 'UTF-8'),
        'amostra2.csv': ('codigo;idade\nP-1;30\nP-2;-5\n'.encode(), 'já foi enviado'),
    }
    for nome, (conteudo, esperado) in casos.items():
        msg = subir(app, tmp_path, nome, conteudo)
        assert 'recusado' in msg and esperado in msg, f'{nome}: {msg}'
    app.estado("S.config.uploadMaxMB=0.0001")
    app.ir('ag-pesquisa', 250)
    assert 'limite' in subir(app, tmp_path, 'grande.csv', ('a;b\n' + '1;2\n' * 200).encode())
    assert app.st(f"P('{pid}').arquivos.length") == 3
    assert app.st(f"P('{pid}').arquivos.every(a=>/^[0-9a-f]{{64}}$/.test(a.hash))")  # integridade SHA-256
    assert app.st("S.auditoria.filter(a=>a.acao.startsWith('Upload recusado')).length") >= 9


def test_agente_nao_ve_resultados_nem_pesquisa_de_outro(app):
    app.login(AGENTE, senha=CODIGO)
    for r in ['adm-resultados', 'eq-resultados', 'cl-resultados', 'adm-pesquisas', 'adm-revisao']:
        app.ir(r, 200); assert app.hash() == '#negado', r
    # pesquisa de outro autor (criada pela administração), aberta à força
    app.estado("S.ui.agPid='p1'"); app.ir('ag-pesquisa', 250)
    assert 'não é sua' in app.main() and 'Satisfação' not in app.main()
    for acao, dados in [('exp-res', {}), ('rv-publicar', {'id': 'pg1'}), ('rv-decidir', {'id': 'pg1', 'd': 'aprovar'}), ('ag-enviar', {'id': 'p1'}), ('v-novo', {})]:
        app.forjar(acao, **dados)
    assert app.st("P('pg1').status") == 'Em revisão' and app.st("P('p1').status") == 'Ativa'


def test_envio_para_revisao_nao_publica(app):
    app.login(AGENTE, senha=CODIGO); pid = nova_pesquisa(app)
    app.p.click('[data-act="ag-enviar"]'); app.p.wait_for_timeout(300)
    assert app.st(f"P('{pid}').status") == 'Em revisão'
    assert app.p.locator('form[data-form="ag-pesq"] button[type=submit]').count() == 0  # não edita mais
    app.forjar('ag-enviar', id=pid); assert app.st(f"P('{pid}').status") == 'Em revisão'


def test_desativar_corta_acesso_e_mantem_historico(app):
    app.login(AGENTE, senha=CODIGO); pid = nova_pesquisa(app, nome='Histórico do agente substituído')
    app.login(ADMIN, 'admin'); app.ir('adm-cadastros', 200); app.p.click('[data-k="cadTab"][data-v="agentes"]'); app.p.wait_for_timeout(200)
    # excluir o cadastro de agente com histórico é recusado
    app.p.click('[data-act="cad-del"][data-id="a4"]'); app.p.wait_for_timeout(200)
    assert app.st("S.agentes.some(a=>a.id==='a4')")
    app.p.click('[data-act="ag-desativar"][data-id="a4"]'); app.p.wait_for_timeout(150)
    app.p.click('#mot-ok'); assert app.p.locator('#mot-err:visible').count() == 1
    app.p.fill('#mot', 'Contrato encerrado; substituído por Victor Alves'); app.p.click('#mot-ok'); app.p.wait_for_timeout(250)
    app.login(AGENTE, senha=CODIGO); assert app.p.locator('#l-err:visible').count() == 1 and app.hash() == '#login'
    # histórico íntegro: pesquisas e auditoria continuam com o nome do agente
    assert app.st(f"P('{pid}').criadoPorNome") == 'Paulo Sena' and app.st("P('pg1').criadoPorNome") == 'Paulo Sena'
    assert app.st("S.auditoria.some(a=>a.acao==='Login de agente desativado'&&a.motivo.includes('substituído'))")
    # o substituto recebe login próprio e não vê as pesquisas do anterior
    codigo = gerar_login(app, 'a3')
    app.login('victor@sinergia.com.br', senha=codigo); app.ir('ag-pesquisas', 250)
    assert 'Histórico do agente substituído' not in app.main() and 'Recall de trailer' not in app.main()


def test_sessao_aberta_perde_acesso_na_desativacao(app):
    app.login(AGENTE, senha=CODIGO); app.ir('ag-pesquisas', 200)
    # o administrador desativa em outra aba (simulado direto no estado gravado)
    app.estado("const u=S.users.find(x=>x.email==='paulo.sena@campo.com.br');u.vinculos.find(v=>v.tipo==='agente').situacao='revogado'")
    app.ir('ag-pesquisas', 250); assert app.hash() in ('#negado', '#login')
    app.forjar('ag-nova'); assert app.hash() != '#ag-pesquisa'


def test_vinculo_de_agente_nao_nasce_por_outro_caminho(app):
    # o formulário genérico de vínculo não oferece "agente", e um envio forjado é recusado
    app.login(ADMIN, 'admin'); app.ir('adm-usuarios', 250)
    uid = app.st("S.users.find(u=>u.email==='ana.ribeiro@email.com').id")
    app.p.evaluate("uid=>document.body.insertAdjacentHTML('beforeend',`<form data-form=v-novo data-uid=${uid} id=fx><input name=vtipo value=agente><input name=vref value=a1><div id=u-err></div><button id=fxb>ok</button></form>`)", uid)
    app.p.click('#fxb'); app.p.wait_for_timeout(250)
    assert app.st("S.users.find(u=>u.email==='ana.ribeiro@email.com').vinculos.every(v=>v.tipo!=='agente')")
    # vínculo de agente gravado sem código (adulteração) não entra com qualquer senha
    app.estado("S.users.find(u=>u.email==='paulo.sena@campo.com.br').codigoHash=null")
    app.login(AGENTE, senha='qualquer1'); assert 'não tem código ativo' in app.p.inner_text('#l-err')

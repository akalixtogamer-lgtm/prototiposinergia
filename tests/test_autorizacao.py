"""Testes de autorização (módulo E, revistos na refatoração de acessos de 28/10/2026): rotas, ações forjadas, escalada, sessão expirada e matriz só leitura."""
from conftest import ADMIN, PARTICIPANTE, CLIENTE, TRANSCRICAO, ANALISE

def test_E6_escalada_pelo_localStorage_bloqueada(app):
    app.login(PARTICIPANTE)
    app.estado("S.session.mode='admin'")
    app.ir('adm-usuarios', 300)
    assert app.hash() == '#negado' and app.st("S.auditoria[0].rota") == '#adm-usuarios'

def test_E7_rota_direta_sem_permissao(app):
    app.login(PARTICIPANTE); app.ir('eq-transcricoes', 300); assert app.hash() == '#negado'
    app.login(CLIENTE); app.ir('adm-pesquisas', 300); assert app.hash() == '#negado'
    assert 'ERRO 403' in app.p.inner_text('body').upper()

def test_E7_sem_login_vai_para_entrada(app):
    app.ir('adm-pesquisas', 300); assert app.hash() == '#login' and 'Entre com sua conta' in app.p.inner_text('body')

def test_E7_sessao_expirada(app):
    app.login(ADMIN, 'admin'); app.estado("S.session.last=0")  # recarrega já em #adm-pesquisas
    assert app.hash() == '#login' and 'expirou' in app.p.inner_text('body')

def test_E5_acao_forjada_e_bloqueada(app):
    app.login(PARTICIPANTE)
    app.forjar('excluir-pesquisa', id='p1')
    assert app.p.locator('.modal-bg:visible').count() == 0 and app.st("!!P('p1')") and app.st("S.auditoria[0].acao") == 'Pesquisas · Excluir'
    app.forjar('remover-usuario', id='u1')
    assert app.st("S.users.some(u=>u.id==='u1')") and app.st("S.auditoria[0].acao") == 'Usuários · Gerenciar usuários'

def test_E6_so_admin_gerencia_usuarios_mesmo_com_matriz_adulterada(app):
    app.login(ANALISE); app.estado("S.perm2.analise['usuarios.usuarios']=1;S.perm2.analise['integracoes.integracoes']=1")
    app.forjar('novo-usuario'); assert app.p.locator('.modal-bg:visible').count() == 0
    app.ir('adm-usuarios', 300); assert app.hash() == '#negado'

def test_E2_matriz_so_leitura_e_politica_vem_do_codigo(app):
    """A matriz virou só leitura: não há caixas para marcar, e mexer na cópia gravada no navegador não muda nada."""
    app.login(ADMIN, 'admin'); app.ir('adm-usuarios'); app.p.click('[data-act="set"][data-v="arquitetura"]'); app.p.wait_for_timeout(200)
    assert app.p.locator('.matrix input').count() == 0 and app.p.locator('[data-act="salvar-mx2"]').count() == 0
    app.login(ANALISE); app.estado("S.perm2.analise['resultados.detalhes']=0")
    app.ir('eq-resultados'); assert 'Respostas detalhadas' in app.main()

def test_E6_funcao_da_equipe_so_age_na_propria_etapa(app):
    app.login(TRANSCRICAO)
    fid = app.st("S.focus.find(f=>f.transcricao&&f.transcricao.status==='Transcrita').id")
    app.forjar('eq-acao', id=fid)
    assert app.p.locator('.modal-bg:visible').count() == 0 and app.st(f"FG('{fid}').transcricao.status") == 'Transcrita' and app.st("S.auditoria[0].acao") == 'Transcrições · Editar'

def test_A3_cliente_nao_ve_dados_individuais(app):
    app.login(CLIENTE); app.estado("S.perm2.cliente['resultados.detalhes']=1")  # adulterar a cópia gravada não libera nada
    app.ir('cl-resultados')
    assert 'Respostas detalhadas' not in app.main() and 'P-10' not in app.main()

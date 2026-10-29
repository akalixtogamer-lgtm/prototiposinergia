"""Regressão: todas as telas de todos os perfis abrem sem erro; o que já existia (S1–S5) continua."""
import pathlib
from conftest import ADMIN, PARTICIPANTE, CLIENTE, TRANSCRICAO, PROCESSAMENTO, ANALISE

PERFIS = [(ADMIN, 'admin'), (TRANSCRICAO, 'usuario'), (PROCESSAMENTO, 'usuario'), (ANALISE, 'usuario'), (CLIENTE, 'usuario'), (PARTICIPANTE, 'usuario'), ('paulo.sena@campo.com.br', 'usuario')]  # V2: agente terceirizado

def test_todas_as_telas_e_abas_abrem_sem_erro(app):
    visitadas = 0
    for email, aba in PERFIS:
        app.login(email, aba, senha='CAMPO26' if 'campo.com' in email else '1234')
        rotas = list(dict.fromkeys(app.p.evaluate("[...document.querySelectorAll('nav a[href^=\"#\"]')].map(a=>a.getAttribute('href')).filter(h=>/^#(adm|eq|cl|pa|ag)-/.test(h))")))
        assert rotas, email
        for r in rotas:
            app.ir(r[1:]); assert app.hash() == r, (email, r, app.hash())
            for i in range(app.p.locator('.sys-main [role=tab]').count()):
                app.p.locator('.sys-main [role=tab]').nth(i).click(); app.p.wait_for_timeout(120)
            visitadas += 1
    assert visitadas >= 20  # erros de JavaScript são verificados ao fim do teste (fixture)

def test_S5_agente_sem_login_gerado_continua_recusado(app):
    # RF03 (V2) substitui a S5: o agente só entra com o login que o administrador gera; sem isso, continua recusado
    app.login('yasmin@sinergia.com.br'); assert 'ainda não foi gerado' in app.p.inner_text('#l-err')
    app.ir('ag-pesquisas'); assert app.hash() == '#login'

def test_S1_marca_dagua_continua_no_material(app):
    app.login(ADMIN, 'admin'); fid = app.st("S.focus.find(f=>f.status==='Em andamento').id")
    app.entrar_sala(fid)
    mid = app.st(f"FG('{fid}').materiais[0]"); app.p.select_option('#fg-mat', mid); app.p.click('[data-act="fg-apresentar"]'); app.p.wait_for_timeout(250)
    assert 'Helena Prado' in app.p.inner_text('.drm-wm')

def test_site_publico_fala_em_teams_meet(app):
    app.ir('focusgroup'); t = app.p.inner_text('body'); assert 'Teams' in t and 'Meet' in t and 'Sala ao vivo' not in t

def test_etiquetas_inicio_meio_fim_presentes():
    h = (pathlib.Path(__file__).resolve().parent.parent / 'index.html').read_text()
    assert h.count('▶ INÍCIO') == h.count('■ FIM') and h.count('▶ INÍCIO') >= 20

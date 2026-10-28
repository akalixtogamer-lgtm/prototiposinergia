"""Integrações: só o que existe de verdade é dado como funcionando (A.4, D.1–D.5)."""
import pathlib, re
from conftest import ADMIN

def test_A4_link_surveymonkey_validado_e_aberto_em_nova_aba(app):
    app.login(ADMIN, 'admin'); app.ir('adm-pesquisas')
    app.p.click('[data-act="editar-pesquisa"][data-id="p2"]'); app.p.wait_for_timeout(150)
    app.p.fill('#smlink', 'https://exemplo.com/form'); app.p.click('button[form="f-pesq"]'); app.p.wait_for_timeout(150)
    assert 'SurveyMonkey inválido' in app.p.inner_text('#pf-err')
    app.p.fill('#smlink', 'https://www.surveymonkey.com/r/TESTE'); app.p.click('button[form="f-pesq"]'); app.p.wait_for_timeout(200)
    a = app.p.locator('a[data-ext="surveymonkey"][href="https://www.surveymonkey.com/r/TESTE"]')
    assert a.count() == 1 and a.get_attribute('target') == '_blank' and 'noopener' in a.get_attribute('rel')

def test_D2_formatos_de_link_aceitos(app):
    app.login(ADMIN, 'admin'); app.ir('adm-focus')
    casos = [('Google Meet', 'https://meet.google.com/abc-defg-hij', True), ('Google Meet', 'http://meet.google.com/abc-defg-hij', False),
             ('Microsoft Teams', 'https://teams.microsoft.com/l/meetup-join/x', True), ('Microsoft Teams', 'https://teams.evil.com/x', False),
             ('Google Meet', 'https://zoom.us/j/1', False)]
    for plat, link, ok in casos:
        app.p.click('[data-act="fg-nova"]'); app.p.wait_for_timeout(120)
        app.p.fill('#fgnome', 'Link ' + link); app.p.fill('#fgdata', '2026-11-05'); app.p.select_option('#fgplat', plat); app.p.fill('#fglink', link)
        app.p.check('[name="cv:P-1027"]'); app.p.check('[name="cv:P-1031"]'); app.p.click('button[form="f-fg"]'); app.p.wait_for_timeout(150)
        criado = app.st(f"S.focus.some(f=>f.link==={link!r})")
        assert criado is ok, (plat, link)
        if not ok: app.p.click('.modal-bg [data-act="close"]'); app.p.wait_for_timeout(100)

def test_integracoes_declara_o_que_nao_existe(app):
    app.login(ADMIN, 'admin'); app.ir('adm-integracoes'); t = app.main()
    assert t.count('Não implementado') >= 2 and 'Indisponível' in t and 'Funcionando' in t

def test_sem_credenciais_no_repositorio():
    raiz = pathlib.Path(__file__).resolve().parent.parent
    padrao = re.compile(r'(api[_-]?key|secret|bearer\s+[a-z0-9]|sk-[a-z0-9]{10}|ghp_[a-z0-9]{10}|client_secret|access_token)', re.I)
    achados = [f'{p.name}:{m.group(0)}' for p in raiz.rglob('*') if p.is_file() and p.suffix in {'.html', '.md', '.js', '.json', '.py'} and '.git' not in p.parts and p.name != 'test_integracoes.py'
               for m in padrao.finditer(p.read_text(errors='ignore'))]
    assert not achados, achados

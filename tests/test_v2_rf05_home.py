"""V2 · RF05 — página inicial e acesso administrativo.
Login de usuário e cadastro em destaque; acesso administrativo fora do destaque (link discreto no rodapé);
a ocultação é só de interface: a permissão continua conferida pela conta e pela sessão em cada rota e ação.
Também cobre o item 1 da Etapa 9 (login, cadastro e autorização por perfil) e o item 11 (acessibilidade e responsividade)."""
import pytest
from conftest import ADMIN, PARTICIPANTE, CLIENTE


def test_home_prioriza_entrar_e_cadastro(app):
    app.ir('home')
    faixa = app.p.locator('.acesso-faixa')
    assert faixa.count() == 1
    assert faixa.locator('a[href="#login"]').is_visible() and faixa.locator('a[href="#cadastro"]').is_visible()
    nav = app.p.inner_text('#nav')
    assert 'Entrar' in nav and 'Cadastre-se' in nav and 'Administrador' not in nav
    # nenhum elemento de acesso administrativo na área principal da home
    assert 'Administrador' not in app.p.inner_text('#view') and app.p.locator('#view a[href="#acesso-interno"]').count() == 0


def test_acesso_interno_so_no_rodape(app):
    app.ir('home')
    assert app.p.locator('#footer a[href="#acesso-interno"]').count() == 1
    app.ir('login')
    t = app.p.inner_text('#view')
    assert 'Administrador' not in t and app.p.locator('[data-tab="admin"]').count() == 0
    assert app.p.locator('#view a[href="#cadastro"]').count() >= 1


def test_admin_entra_so_pelo_acesso_interno(app):
    app.login(ADMIN)  # tela Entrar comum
    assert 'acesso interno' in app.p.inner_text('#l-err')
    app.login(ADMIN, 'admin')
    assert app.hash() == '#adm-pesquisas'


def test_ocultar_nao_muda_permissao(app):
    # conhecer o endereço do acesso interno não dá privilégio: conta sem nomeação é recusada e a tentativa fica registrada
    app.login(PARTICIPANTE, 'admin')
    assert 'não é de administrador' in app.p.inner_text('#l-err')
    assert app.st("S.auditoria.some(a=>a.acao.includes('acesso interno sem nomeação'))")
    app.login(PARTICIPANTE); app.ir('adm-usuarios', 300)
    assert app.hash() == '#negado'


def test_cadastro_publico_nao_concede_admin(app):
    app.ir('cadastro')
    campos = app.p.locator('form[data-form="cadastro"] input:visible').count()
    assert campos >= 2
    app.p.fill('#p-nome', 'Teste Público'); app.p.fill('#p-mail', 'novo.publico@exemplo.com'); app.p.fill('#p-cid', 'Rio de Janeiro')
    app.p.select_option('#p-idade', index=1); app.p.fill('#p-senha', 'senha-teste')
    # campo forjado tentando pedir privilégio no formulário público
    app.p.evaluate("document.querySelector('form[data-form=cadastro]').insertAdjacentHTML('beforeend','<input type=hidden name=admin value=1><input type=hidden name=perfil value=admin>')")
    app.p.click('form[data-form="cadastro"] button[type=submit]'); app.p.wait_for_timeout(400)
    tipos = app.st("(S.users.find(u=>u.email==='novo.publico@exemplo.com')||{vinculos:[]}).vinculos.map(v=>v.tipo).join(',')")
    assert tipos == 'participante'
    app.login('novo.publico@exemplo.com', 'admin')
    assert 'não é de administrador' in app.p.inner_text('#l-err')


@pytest.mark.parametrize('rota', ['home', 'login', 'acesso-interno', 'cadastro'])
def test_responsivo_360px_sem_rolagem_lateral(app, rota):
    app.p.set_viewport_size({'width': 360, 'height': 780}); app.ir(rota, 300)
    largura = app.p.evaluate('document.documentElement.scrollWidth')
    assert largura <= 361, f'{rota}: largura {largura}px em tela de 360px'
    if rota == 'home':
        assert app.p.locator('.acesso-faixa a[href="#login"]').is_visible()


def test_teclado_alcanca_entrar_e_cadastro(app):
    app.ir('home'); app.p.focus('body')
    vistos = []
    for _ in range(40):
        app.p.keyboard.press('Tab')
        vistos.append(app.p.evaluate("(document.activeElement.getAttribute('href')||'')+'|'+document.activeElement.textContent.trim()"))
    assert any(v.startswith('#login|') for v in vistos) and any(v.startswith('#cadastro|') for v in vistos)
    # os campos do login têm rótulo associado
    app.ir('login')
    assert app.p.locator('label[for="l-mail"]').count() == 1 and app.p.locator('label[for="l-senha"]').count() == 1


def test_cliente_e_participante_entram_pela_tela_comum(app):
    app.login(CLIENTE); assert app.hash() == '#cl-projetos'
    app.login(PARTICIPANTE); assert app.hash() == '#pa-pesquisas'

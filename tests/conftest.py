"""Base dos testes automatizados (Playwright + pytest).
Rodar na raiz do repositório:  pip install pytest playwright && playwright install chromium && pytest -q tests
Os testes abrem o index.html local; nenhum dado real é usado (contas e participantes são fictícios do protótipo)."""
import pathlib, pytest
from playwright.sync_api import sync_playwright

URL = (pathlib.Path(__file__).resolve().parent.parent / 'index.html').as_uri()
SENHA = '1234'  # senha de demonstração do protótipo: qualquer valor é aceito; não é credencial real

@pytest.fixture(scope='session')
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch(); yield b; b.close()

class App:
    def __init__(self, page): self.p = page; self.erros = []
    def ir(self, rota, espera=250): self.p.goto(URL + '#' + rota); self.p.wait_for_timeout(espera)
    def hash(self): return self.p.evaluate('location.hash')
    def login(self, email, aba='usuario', senha=SENHA):
        # RF05 (V2): o administrador entra pelo acesso interno (link discreto no rodapé); os demais pela tela Entrar
        rota = 'acesso-interno' if aba == 'admin' else 'login'
        self.ir(rota, 200)
        if self.p.locator('[data-act="logout"]').count(): self.p.click('[data-act="logout"]'); self.p.wait_for_timeout(200); self.ir(rota, 200)
        self.p.fill('#l-mail', email); self.p.fill('#l-senha', senha)
        self.p.click('form[data-form=login] button[type=submit]'); self.p.wait_for_timeout(350)
    def st(self, expr):
        """Lê o estado salvo pelo sistema (o código roda isolado numa função; o teste só enxerga o que foi salvo)."""
        return self.p.evaluate("e=>(new Function('S','const P=id=>S.pesquisas.find(p=>p.id===id),FG=id=>S.focus.find(f=>f.id===id);return ('+e+')'))(JSON.parse(localStorage.getItem('sinergia-sistema-v4')))", expr)
    def forjar(self, acao, **dados):
        """Simula um botão forjado no navegador (ex.: criado pelo console) e clica nele."""
        self.p.evaluate("([a,d])=>{const b=document.createElement('button');b.type='button';b.dataset.act=a;Object.assign(b.dataset,d);b.id='forjado';document.body.appendChild(b)}", [acao, dados])
        self.p.click('#forjado'); self.p.wait_for_timeout(200)
        self.p.evaluate("document.getElementById('forjado')?.remove()")
    def entrar_sala(self, fid):
        self.ir('adm-focus'); self.p.click(f'[data-act="fg-entrar"][data-id="{fid}"]'); self.p.wait_for_timeout(300)
    def estado(self, fn):
        """Altera o estado salvo no navegador (simula adulteração do localStorage) e recarrega."""
        self.p.evaluate("f=>{const k='sinergia-sistema-v4';const s=JSON.parse(localStorage.getItem(k));(new Function('S',f))(s);localStorage.setItem(k,JSON.stringify(s))}", fn)
        self.p.reload(); self.p.wait_for_timeout(300)
    def liberar_resultados_cliente(self, email='marina@cinemaalfa.com.br'):
        """RF01 (V2): o cliente só vê resultados liberados. Simula um pedido 'todas as pesquisas' já aprovado pelo administrador."""
        self.estado(f"const u=S.users.find(x=>x.email==='{email}'),emp=u.vinculos.find(v=>v.tipo==='cliente').ref;S.solicRes.push({{id:'sr-t',uid:u.id,nome:u.nome,empresa:emp,escopo:'todas',pid:'',status:'Aprovada',criada:'',decididaPor:'Helena Prado',decididaEm:'',pids:S.pesquisas.filter(p=>p.cliente===emp&&['Ativa','Pausada','Encerrada'].includes(p.status)).map(p=>p.id)}})")
    def main(self): return self.p.inner_text('.sys-main') if self.p.locator('.sys-main').count() else self.p.inner_text('body')

@pytest.fixture
def app(browser):
    page = browser.new_page(viewport={'width': 1366, 'height': 860})
    a = App(page)
    page.on('pageerror', lambda e: a.erros.append('PAGE: ' + str(e) + ' @ ' + page.url + ' ' + (getattr(e,'stack','') or '')[:300]))
    page.on('console', lambda m: a.erros.append('CONSOLE: ' + m.text) if m.type == 'error' and 'ERR_' not in m.text else None)
    page.goto(URL + '#home'); page.evaluate('localStorage.clear()'); page.reload(); page.wait_for_timeout(300)
    yield a
    page.close()
    assert not a.erros, 'Erros de JavaScript: ' + '\n'.join(a.erros)

ADMIN = 'helena@sinergia.com.br'
PARTICIPANTE = 'ana.ribeiro@email.com'
CLIENTE = 'marina@cinemaalfa.com.br'
TRANSCRICAO = 'bianca@sinergia.com.br'
PROCESSAMENTO = 'carla@dadosco.com.br'
ANALISE = 'livia@sinergia.com.br'

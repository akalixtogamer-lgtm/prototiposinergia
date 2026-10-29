"""Refatoração de acessos (28/10/2026): permissões calculadas a partir de vínculos e políticas, negação por padrão,
isolamento entre clientes e participantes, revogação, múltiplos vínculos, auditoria e estados da tela.
Lembrete honesto: o protótipo não tem servidor. "Chamada direta" aqui é um botão forjado no navegador, que passa pela
mesma checagem central (exigir) que uma API real precisaria repetir."""
from conftest import ADMIN, PARTICIPANTE, CLIENTE, TRANSCRICAO, ANALISE

ADMIN2 = 'marcos@sinergia.com.br'
RAFAEL = 'demo@sinergia.com.br'
CONVIDADO = 'otavio@ciabeta.com'
SUSPENSO = 'paulo@cinemadelta.com.br'


def uid(app, email):
    return app.st(f"S.users.find(u=>u.email==='{email}').id")


def vid(app, email, tipo):
    return app.st(f"S.users.find(u=>u.email==='{email}').vinculos.find(v=>v.tipo==='{tipo}').id")


def abrir_detalhes(app, email):
    app.ir('adm-usuarios'); app.p.click(f'[data-act="usr-det"][data-id="{uid(app, email)}"] >> nth=0'); app.p.wait_for_timeout(200)


def confirmar_motivo(app, texto='Teste automatizado da refatoração'):
    app.p.fill('#mot', texto); app.p.click('#mot-ok'); app.p.wait_for_timeout(250)


def erro_login(app, email, aba='usuario'):
    app.login(email, aba)
    return app.p.inner_text('#l-err') if app.p.locator('#l-err:visible').count() else ''


# 1. Sem vínculo válido não há acesso
def test_sem_vinculo_valido_nao_entra(app):
    app.estado("S.users.push({id:'ux',nome:'Sem Vínculo',email:'sem@exemplo.com',vinculos:[],bloqueado:false})")
    assert 'nenhum vínculo ativo' in erro_login(app, 'sem@exemplo.com')
    assert 'suspensa' in erro_login(app, SUSPENSO)


def test_checkboxes_sumiram_e_campos_antigos_nao_dao_acesso(app):
    app.login(ADMIN, 'admin'); app.ir('adm-usuarios')
    assert app.p.locator('[data-act-change="perm"]').count() == 0 and 'ACESSO CALCULADO' in app.main().upper()
    # gravar perms/admin à mão não vale: o sistema recalcula pelos vínculos
    app.estado("S.users.push({id:'uy',nome:'Forjado',email:'forjado@exemplo.com',admin:true,perms:['equipe','cliente','participante'],empresa:'Cinema Alfa',funcao:'Assistente de análise',codigo:'P-1027',vinculos:[]})")
    assert 'não é de administrador' in erro_login(app, 'forjado@exemplo.com', 'admin')
    assert 'nenhum vínculo ativo' in erro_login(app, 'forjado@exemplo.com')


# 2. Cliente A não acessa dados do Cliente B
def test_cliente_nao_ve_outro_cliente(app):
    app.login(CLIENTE); app.ir('cl-projetos')
    assert 'Consumo de streaming' not in app.main() and 'Lançamentos 2026' in app.main()
    app.estado("S.ui.resPid='p2'"); app.ir('cl-resultado')
    assert 'Hábitos de consumo — Streaming' not in app.main()
    # trocar a empresa gravada no navegador não muda o escopo: ele vem do vínculo
    app.estado("S.users.find(u=>u.email==='marina@cinemaalfa.com.br').empresa='Cia Beta'"); app.ir('cl-projetos')
    assert 'Consumo de streaming' not in app.main()


# 3. Participante não acessa áreas administrativas nem dados de outros
def test_participante_fora_da_administracao(app):
    app.login(PARTICIPANTE)
    for rota in ('adm-cadastros', 'adm-usuarios', 'eq-resultados', 'cl-projetos'):
        app.ir(rota, 250); assert app.hash() == '#negado', rota
    app.ir('pa-pesquisas'); assert '@' not in app.main()


# 4. Equipe interna recebe só o que a função prevê
def test_equipe_so_capacidades_da_funcao(app):
    app.login(TRANSCRICAO); app.ir('eq-resultados', 250); assert app.hash() == '#negado'
    app.login(ANALISE); app.ir('eq-resultados'); assert app.hash() == '#eq-resultados'
    app.forjar('nova-pesquisa'); assert app.p.locator('.modal-bg:visible').count() == 0


# 5. Não dá para elevar o próprio privilégio no navegador
def test_elevacao_pelo_navegador_nao_funciona(app):
    app.login(PARTICIPANTE)
    app.estado("const u=S.users.find(x=>x.email==='ana.ribeiro@email.com');u.admin=true;u.perms=['equipe','cliente','participante'];S.perm2.participante['usuarios.usuarios']=1;S.session.mode='admin'")
    app.ir('adm-usuarios', 300); assert app.hash() == '#negado'
    assert app.st("S.users.find(x=>x.email==='ana.ribeiro@email.com').admin") is False


# 6. "Chamada direta" (botão forjado) respeita as regras
def test_acoes_de_acesso_forjadas_sao_negadas(app):
    v = None
    app.login(ANALISE)
    m = uid(app, 'marina@cinemaalfa.com.br'); v = vid(app, 'marina@cinemaalfa.com.br', 'cliente')
    for acao, dados in (('conta-suspender', {'uid': m}), ('v-revogar', {'uid': m, 'vid': v}), ('adm-solicitar', {'uid': uid(app, ANALISE)})):
        app.forjar(acao, **dados)
        assert app.p.locator('.modal-bg:visible').count() == 0, acao
        assert app.st("S.auditoria[0].tipo") == 'negado'
    assert app.st(f"S.users.find(u=>u.id==='{m}').bloqueado") is False


# 7. Revogar um vínculo atualiza o acesso
def test_revogacao_pelo_administrador_tira_o_acesso(app):
    app.login(ADMIN, 'admin'); abrir_detalhes(app, 'marina@cinemaalfa.com.br')
    app.p.click('.modal [data-act="v-revogar"]'); app.p.wait_for_timeout(150); confirmar_motivo(app, 'Contrato encerrado')
    assert app.st("S.users.find(u=>u.email==='marina@cinemaalfa.com.br').vinculos[0].situacao") == 'revogado'
    assert 'nenhum vínculo ativo' in erro_login(app, CLIENTE)


# 8. A sessão aberta não mantém privilégio depois da revogação
def test_sessao_perde_privilegio_apos_revogacao(app):
    app.login(CLIENTE); app.ir('cl-projetos'); assert app.hash() == '#cl-projetos'
    app.estado("S.users.find(u=>u.email==='marina@cinemaalfa.com.br').vinculos.forEach(v=>v.situacao='revogado')")
    app.ir('cl-projetos', 300); assert app.hash() == '#negado'
    app.login(ADMIN, 'admin'); app.estado("S.users.find(u=>u.email==='helena@sinergia.com.br').bloqueado=true")
    app.ir('adm-pesquisas', 300); assert app.hash() == '#negado'


# 9. Múltiplos vínculos seguem regra explícita (um papel por sessão; equipe + cliente vai para revisão)
def test_multiplos_vinculos(app):
    assert app.st("S.users.find(u=>u.email==='demo@sinergia.com.br').vinculos.find(v=>v.tipo==='cliente').situacao") == 'revisao'
    app.login(RAFAEL); assert app.hash() == '#navegar'
    assert 'Cliente Empresa' not in app.p.inner_text('.choose')
    app.ir('cl-projetos', 300); assert app.hash() == '#negado'
    app.p.goto(app.p.url.split('#')[0] + '#navegar'); app.p.wait_for_timeout(200)
    app.p.click('[data-act="switch"][data-role="participante"]'); app.p.wait_for_timeout(250)
    assert 'Resultados' not in app.p.inner_text('.sys-side nav')  # papel de participante não herda o da equipe
    # o administrador confirma a revisão com motivo; só então o papel de cliente passa a valer
    app.login(ADMIN, 'admin'); abrir_detalhes(app, RAFAEL)
    app.p.click('.modal [data-act="v-confirmar"]'); app.p.wait_for_timeout(150); confirmar_motivo(app, 'Analista também é contato do cliente; separação de dados confirmada')
    app.login(RAFAEL); assert 'Cliente Empresa' in app.p.inner_text('.choose')


# 10. Ações críticas ficam na auditoria (com responsável e motivo) e pedem confirmação
def test_acoes_criticas_auditadas(app):
    app.login(ADMIN, 'admin'); abrir_detalhes(app, TRANSCRICAO)
    app.p.click('.modal [data-act="conta-suspender"]'); app.p.wait_for_timeout(150)
    app.p.click('#mot-ok'); app.p.wait_for_timeout(150)
    assert app.p.is_visible('#mot-err')  # sem motivo, não suspende
    confirmar_motivo(app, 'Afastamento temporário')
    a = app.st("S.auditoria[0]")
    assert a['acao'] == 'Conta suspensa' and a['quem'] == 'Helena Prado' and a['motivo'] == 'Afastamento temporário'
    assert 'suspensa' in erro_login(app, TRANSCRICAO)


# R4 e R13: nomeação de administrador com quatro olhos; o administrador não reduz a própria proteção
def test_nomeacao_de_admin_precisa_de_outro_admin(app):
    app.login(ADMIN, 'admin'); abrir_detalhes(app, ANALISE)
    app.p.click('.modal [data-act="adm-solicitar"]'); app.p.wait_for_timeout(150); confirmar_motivo(app, 'Coordenação de análise')
    app.p.click('.modal [data-act="v-aprovar"]'); app.p.wait_for_timeout(250)
    assert app.p.locator('#mot').count() == 0 and 'não é de administrador' in erro_login(app, ANALISE, 'admin')
    app.login(ADMIN2, 'admin'); abrir_detalhes(app, ANALISE)
    app.p.click('.modal [data-act="v-aprovar"]'); app.p.wait_for_timeout(150); confirmar_motivo(app, 'Aprovado pela diretoria')
    app.login(ANALISE, 'admin'); assert app.hash() == '#adm-pesquisas'


def test_admin_nao_se_suspende_nem_remove_o_ultimo(app):
    app.login(ADMIN, 'admin'); abrir_detalhes(app, ADMIN)
    assert app.p.locator('.modal [data-act="conta-suspender"]').is_disabled() and app.p.locator('.modal [data-act="remover-usuario"]').is_disabled()
    app.p.click('.modal [data-act="close"] >> nth=0'); app.p.wait_for_timeout(150)
    app.forjar('conta-suspender', uid=uid(app, ADMIN)); assert app.st("S.users.find(u=>u.email==='helena@sinergia.com.br').bloqueado") is False
    app.estado("S.users=S.users.filter(u=>u.email!=='marcos@sinergia.com.br')")
    app.forjar('v-revogar', uid=uid(app, ADMIN), vid=vid(app, ADMIN, 'admin'))
    assert app.st("S.users.find(u=>u.email==='helena@sinergia.com.br').vinculos[0].situacao") == 'ativo'


# Migração: nenhuma ampliação silenciosa; casos ambíguos vão para revisão; valores antigos guardados
def test_migracao_nao_amplia_acesso(app):
    app.estado("delete S.acessos;S.users.forEach(u=>{delete u.vinculos});S.users.find(u=>u.id==='u3').empresa='';S.users.find(u=>u.id==='u6').funcao='Cargo inventado'")
    app.ir('home', 300)  # a migração roda ao carregar
    v = app.st("S.users.find(u=>u.id==='u3').vinculos[0]")
    assert v['situacao'] == 'revisao' and v['ref'] == ''  # sem empresa: não escolhe a primeira da lista
    assert app.st("S.users.find(u=>u.id==='u6').vinculos[0].situacao") == 'revisao'
    assert app.st("S.users.find(u=>u.id==='u3').legado.perms[0]") == 'cliente'
    assert 'nenhum vínculo ativo' in erro_login(app, CLIENTE) or 'ainda não foi liberado' in erro_login(app, CLIENTE)


# Convite: conta nasce sem acesso; vale quando a pessoa entra
def test_convite_vale_so_no_primeiro_acesso(app):
    app.login(ADMIN, 'admin'); app.ir('adm-usuarios'); app.p.click('[data-act="novo-usuario"]'); app.p.wait_for_timeout(150)
    app.p.fill('#unome', 'Nova Cliente'); app.p.fill('#umail', 'nova@ciabeta.com')
    app.p.click('button[form="f-usr"]'); app.p.wait_for_timeout(150)
    assert 'Escolha o tipo' in app.p.inner_text('#u-err')
    app.p.select_option('#vtipo', 'cliente'); app.p.click('button[form="f-usr"]'); app.p.wait_for_timeout(150)
    assert 'não escolhe por você' in app.p.inner_text('#u-err')  # empresa obrigatória, sem padrão
    app.p.select_option('#vref', 'Cia Beta'); app.p.click('button[form="f-usr"]'); app.p.wait_for_timeout(200)
    assert app.st("S.users.find(u=>u.email==='nova@ciabeta.com').perms.length") == 0
    app.login('nova@ciabeta.com'); assert app.hash() == '#cl-projetos' and 'Consumo de streaming' in app.main()


# 11 e 12. Telas sem dados indevidos e estados de vazio, erro e acesso negado
def test_estados_da_tela(app):
    app.login(ADMIN, 'admin'); app.ir('adm-usuarios')
    app.p.fill('[data-key="usrQ"]', 'ninguém com esse nome'); app.p.wait_for_timeout(200)
    assert 'Nenhum usuário com esses filtros' in app.main()
    app.forjar('usr-det', id='nao-existe'); assert 'Usuário não encontrado' in app.p.inner_text('.modal')
    app.login(CLIENTE); app.ir('adm-usuarios', 250); assert app.hash() == '#negado' and 'ERRO 403' in app.p.inner_text('body').upper()


def test_arquitetura_e_diagnostico_so_explicam(app):
    app.login(ADMIN, 'admin'); app.ir('adm-usuarios'); app.p.click('[data-act="set"][data-v="arquitetura"]'); app.p.wait_for_timeout(200)
    t = app.main()
    for s in ('Fluxo de autorização', 'Matriz de papéis', 'Regras de autorização', 'Auditoria', 'Diagnóstico de acesso', 'Estado da arquitetura'):
        assert s.upper() in t.upper(), s
    app.p.select_option('#dg-u', uid(app, CLIENTE)); app.p.wait_for_timeout(200)
    app.p.select_option('#dg-k', 'resultados.detalhes'); app.p.wait_for_timeout(200)
    assert 'Acesso negado' in app.p.inner_text('#part-diag')
    antes = app.st("JSON.stringify(S.users)")
    app.p.select_option('#dg-k', 'resultados.resultados'); app.p.wait_for_timeout(200)
    assert 'Acesso permitido' in app.p.inner_text('#part-diag') and app.st("JSON.stringify(S.users)") == antes

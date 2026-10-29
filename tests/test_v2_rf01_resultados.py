"""V2 · RF01 — resultados protegidos.
Participante e agente não acessam resultados por tela, endereço direto, exportação ou ação forjada; o cliente só vê
resultados agregados que o administrador liberou depois de um pedido (todas as pesquisas contratadas ou só uma);
a resposta de erro não traz dado confidencial. Limite honesto: sem servidor, "chamada direta" é a ação forjada no
navegador, que passa pela mesma checagem central (exigir) que a API real precisa repetir (D-06)."""
import pytest
from conftest import ADMIN, PARTICIPANTE, CLIENTE, TRANSCRICAO, PROCESSAMENTO, ANALISE

AGENTE = 'paulo.sena@campo.com.br'
CODIGO_AGENTE = 'CAMPO26'
ROTAS_RESULTADO = ['adm-resultados', 'eq-resultados', 'cl-resultados', 'cl-resultado']


def entrar(app, quem):
    if quem == AGENTE: app.login(AGENTE, senha=CODIGO_AGENTE)
    else: app.login(quem)


@pytest.mark.parametrize('quem', [PARTICIPANTE, AGENTE, TRANSCRICAO, PROCESSAMENTO])
def test_sem_rota_de_resultado(app, quem):
    entrar(app, quem)
    for r in ROTAS_RESULTADO:
        app.ir(r, 250)
        assert app.hash() in ('#negado', '#login'), f'{quem} abriu {r}'
        corpo = app.p.inner_text('#view')
        # a resposta de erro não traz nome de pesquisa, número ou cliente
        assert 'Satisfação — Lançamento Filme A' not in corpo and 'Respondentes' not in corpo


@pytest.mark.parametrize('quem', [PARTICIPANTE, AGENTE, CLIENTE])
def test_exportacao_e_liberacao_forjadas_sao_negadas(app, quem):
    entrar(app, quem)
    antes = app.st("S.auditoria.filter(a=>a.tipo==='negado').length")
    app.forjar('exp-res')
    app.forjar('sr-decidir', id='qualquer', d='aprovar')
    depois = app.st("S.auditoria.filter(a=>a.tipo==='negado').length")
    assert depois >= antes + 2
    assert app.st("S.solicRes.filter(x=>x.status==='Aprovada').length") == 0


def test_categorias_por_perfil_interno(app):
    # assistente de análise: resultados e respostas detalhadas (matriz provisória, DP-01)
    app.login(ANALISE); app.ir('eq-resultados', 300)
    assert app.hash() == '#eq-resultados' and 'Respostas detalhadas' in app.main()
    # transcrição: nenhuma categoria de resultado
    app.login(TRANSCRICAO); app.ir('eq-resultados', 300); assert app.hash() == '#negado'
    # cliente: sem respostas detalhadas mesmo depois da liberação
    app.login(CLIENTE); app.liberar_resultados_cliente(); app.ir('cl-resultados', 300)
    assert 'Respostas detalhadas' not in app.main()


def test_cliente_sem_liberacao_nao_ve_numeros(app):
    app.login(CLIENTE); app.ir('cl-resultados', 300)
    t = app.main()
    assert 'Nenhum resultado liberado' in t and 'Pedir acesso aos resultados' in t
    assert app.p.locator('#part-clr').count() == 0
    # resultado individual da própria empresa: só o aviso e o pedido
    app.estado("S.ui.resPid='p1'"); app.ir('cl-resultado', 300)
    assert 'ainda não foram liberados' in app.main() and 'quanto você gostou' not in app.main()
    # pesquisa de outra empresa: nem o nome aparece
    app.estado("S.ui.resPid='p2'"); app.ir('cl-resultado', 300)
    assert 'Hábitos de consumo — Streaming' not in app.p.inner_text('body')


def pedir(app, escopo, pid=None):
    app.ir('cl-resultados', 300)
    app.p.check(f'form[data-form="sol-res"] input[value="{escopo}"]')
    if pid: app.p.select_option('#sr-pid', pid)
    app.p.click('form[data-form="sol-res"] button[type=submit]'); app.p.wait_for_timeout(250)


def decidir(app, decisao, motivo=''):
    app.ir('adm-resultados', 200); app.p.click('[data-k="resTab"][data-v="sol"]'); app.p.wait_for_timeout(200)
    app.p.click(f'[data-act="sr-decidir"][data-d="{decisao}"] >> nth=0'); app.p.wait_for_timeout(150)
    if motivo: app.p.fill('#mot', motivo)
    app.p.click('#mot-ok'); app.p.wait_for_timeout(250)


def test_pedido_de_uma_pesquisa_libera_so_ela(app):
    app.login(CLIENTE); pedir(app, 'uma', 'p1')
    assert app.st("S.solicRes[0].status") == 'Pendente'
    app.login(ADMIN, 'admin'); decidir(app, 'aprovar')
    assert app.st("S.solicRes[0].pids.join()") == 'p1'
    app.login(CLIENTE); app.ir('cl-resultados', 300)
    assert '1 pesquisa' in app.main()
    app.estado("S.ui.resPid='p1'"); app.ir('cl-resultado', 300); assert 'quanto você gostou' in app.main()
    app.estado("S.ui.resPid='p6'"); app.ir('cl-resultado', 300); assert 'ainda não foram liberados' in app.main()


def test_recusa_exige_motivo_e_revogacao_tira_o_acesso(app):
    app.login(CLIENTE); pedir(app, 'todas')
    app.login(ADMIN, 'admin'); decidir(app, 'recusar')  # sem motivo
    assert app.p.locator('#mot-err:visible').count() == 1 and app.st("S.solicRes[0].status") == 'Pendente'
    app.p.fill('#mot', 'Contrato ainda sem cláusula de entrega de resultados'); app.p.click('#mot-ok'); app.p.wait_for_timeout(250)
    assert app.st("S.solicRes[0].status") == 'Recusada'
    app.login(CLIENTE); app.ir('cl-resultados', 300); assert 'cláusula de entrega' in app.main()
    # novo pedido aprovado e depois revogado
    pedir(app, 'todas'); app.login(ADMIN, 'admin'); decidir(app, 'aprovar')
    app.login(CLIENTE); app.ir('cl-resultados', 300); assert app.p.locator('#part-clr').count() == 1
    app.login(ADMIN, 'admin'); decidir(app, 'revogar', 'Fim do contrato com o cliente neste ciclo')
    app.login(CLIENTE); app.ir('cl-resultados', 300); assert app.p.locator('#part-clr').count() == 0
    assert app.st("S.auditoria.some(a=>a.acao==='Revogar acesso')")


def test_liberacao_todas_nao_inclui_pesquisas_publicadas_depois(app):
    app.login(CLIENTE); app.liberar_resultados_cliente()
    # uma pesquisa nova da mesma empresa publicada depois da aprovação fica fora (menor privilégio)
    app.estado("S.pesquisas.push({...S.pesquisas.find(p=>p.id==='p1'),id:'p-nova',nome:'Pesquisa nova publicada depois',status:'Ativa'})")
    app.estado("S.ui.resPid='p-nova'"); app.ir('cl-resultado', 300)
    assert 'ainda não foram liberados' in app.main()


def test_participante_ve_so_as_proprias_respostas(app):
    # DP-13 (pendente): o participante mantém o histórico das próprias respostas, sem agregado de ninguém
    app.login(PARTICIPANTE); app.ir('pa-respostas', 300)
    t = app.main()
    assert 'Respondentes' not in t and 'margem de erro' not in t.lower()

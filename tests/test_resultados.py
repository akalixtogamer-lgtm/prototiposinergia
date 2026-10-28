"""Resultados por pesquisa (28/10/2026): cada tipo de estudo mostra as próprias perguntas, os números fecham e os filtros ficam claros."""
import re
from conftest import ADMIN, CLIENTE


def _n(txt):
    return [int(x) for x in re.findall(r'\d+', txt)]


def test_R1_visao_geral_mostra_cada_pesquisa_com_indicador_e_n(app):
    app.login(ADMIN, 'admin'); app.ir('adm-resultados')
    linhas = app.p.locator('.res-row')
    assert linhas.count() == app.st('S.pesquisas.length')
    txt = app.p.inner_text('.res-row >> nth=0')
    assert 'SATISFAÇÃO COM FILME' in txt.upper() and 'Nota média do filme' in txt and 'n = 124' in txt


def test_R2_cada_tipo_de_estudo_tem_perguntas_proprias(app):
    app.login(ADMIN, 'admin'); app.ir('adm-resultados')
    esperado = {'p1': 'quanto você gostou do filme', 'p3': 'Depois do trailer', 'p4': 'faixa de idade', 'p6': 'Avalie a sessão', 'p9': 'ideia do filme'}
    for pid, pergunta in esperado.items():
        app.p.click(f'.res-row [data-v="{pid}"]'); app.p.wait_for_timeout(200)
        assert pergunta in app.main(), pid
        app.p.click('[data-act="set"][data-v=""]'); app.p.wait_for_timeout(200)


def test_R3_numeros_fecham_com_o_n_da_pesquisa(app):
    app.login(ADMIN, 'admin'); app.ir('adm-resultados')
    app.p.click('.res-row [data-v="p1"]'); app.p.wait_for_timeout(200)
    semanas = sum(_n(t)[0] for t in app.p.locator('.vb > span').all_inner_texts())
    assert semanas == 124
    # cada pergunta de escolha soma o n inteiro (contagem ao lado do percentual)
    for painel in app.p.locator('.qpanel').all():
        cont = [int(x) for x in painel.locator('.bars.n b small').all_inner_texts() if x.isdigit()]
        if cont: assert sum(cont) == 124


def test_R4_filtro_de_aplicacao_visivel_com_estado_vazio_e_limpar(app):
    app.login(ADMIN, 'admin'); app.ir('adm-resultados')
    app.p.click('[data-k="admModo"][data-v="Online"]'); app.p.wait_for_timeout(200)
    assert 'aplicação online' in app.main()
    assert all('Online' in t for t in app.p.locator('.res-row .info .small').all_inner_texts())
    app.p.click('[data-act="res-limpar"]'); app.p.wait_for_timeout(200)
    assert app.p.locator('.res-row').count() == app.st('S.pesquisas.length')


def test_R5_pesquisa_sem_respostas_explica_o_motivo(app):
    app.login(ADMIN, 'admin'); app.ir('adm-resultados')
    app.p.click('.res-row [data-v="p2"]'); app.p.wait_for_timeout(200)
    t = app.main()
    assert 'Ainda não há resultados' in t and 'Prazo venceu' in t


def test_R6_botao_resultados_da_lista_abre_a_pesquisa(app):
    app.login(ADMIN, 'admin'); app.ir('adm-pesquisas')
    app.p.click('[data-act="resultado"][data-id="p3"]'); app.p.wait_for_timeout(300)
    assert app.hash() == '#adm-resultados' and 'Avaliação de trailer' in app.p.inner_text('.res-head')


def test_R7_respostas_detalhadas_com_colunas_da_pesquisa(app):
    app.login(ADMIN, 'admin'); app.ir('adm-resultados'); app.p.click('[data-act="set"][data-v="det"]'); app.p.wait_for_timeout(200)
    app.p.select_option('[data-key="admDetP"]', 'p1'); app.p.wait_for_timeout(200)
    cab = app.p.inner_text('#part-det-adm thead')
    assert 'Nota do filme' in cab.title() or 'NOTA DO FILME' in cab.upper()


def test_R8_cliente_ve_resultado_sem_dados_internos(app):
    app.login(CLIENTE); app.ir('cl-resultados')
    t = app.main()
    assert 'Entrevistas em campo' not in t and 'Campo atrasado' not in t
    app.p.click('.res-row [data-v="p1"]'); app.p.wait_for_timeout(200)
    assert 'quanto você gostou do filme' in app.main()

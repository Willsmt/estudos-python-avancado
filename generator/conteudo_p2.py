# -*- coding: utf-8 -*-
"""Conteudo parte 2: Aulas 6-9 e Exercicio final."""

from gerar_apostila import (
    para, bullets, code, nota, atencao, exercicio, tabela, chapter,
    Spacer, PageBreak, Paragraph,
    st_h2, st_h3, st_body,
)


def aula6():
    s = chapter("Aula 6", "TDD (Test Driven Development)")
    s.append(para(
        "TDD inverte a ordem: escreve-se o teste antes do codigo. Isso forca voce a "
        "pensar na interface (o que a funcao recebe e devolve) antes da implementacao, "
        "e evita testes que so confirmam o que o codigo ja faz."
    ))
    s.append(para("O ciclo Red-Green-Refactor", st_h2))
    s.append(tabela(
        ["Fase", "O que fazer"],
        [
            ["RED", "Escreve um teste que falha (a feature ainda nao existe)."],
            ["GREEN", "Escreve o codigo minimo para passar (nao precisa ser bonito)."],
            ["REFACTOR", "Limpa o codigo mantendo os testes verdes."],
        ],
        col_widths=[2.6 * 28, 9.4 * 28],
    ))

    s.append(para("RED: teste que falha primeiro", st_h3))
    s.append(code(
        "import pytest\n"
        "from datetime import datetime\n"
        "from scheduling import is_slot_available\n\n"
        "def test_slot_disponivel_sem_conflito():\n"
        "    assert is_slot_available(datetime(2026,7,10,14,0), []) is True\n\n"
        "def test_slot_indisponivel_com_conflito():\n"
        "    existentes = [datetime(2026,7,10,14,0)]\n"
        "    assert is_slot_available(datetime(2026,7,10,14,0), existentes) is False"
    ))
    s.append(para("GREEN: codigo minimo para passar", st_h3))
    s.append(code(
        "def is_slot_available(horario, existing_bookings):\n"
        "    return horario not in existing_bookings"
    ))
    s.append(para("REFACTOR: so depois de verde", st_h3))
    s.append(code(
        "from datetime import timedelta\n\n"
        "def is_slot_available(horario, existing_bookings, duracao_minutos=30):\n"
        "    fim_novo = horario + timedelta(minutes=duracao_minutos)\n"
        "    for existente in existing_bookings:\n"
        "        fim_existente = existente + timedelta(minutes=duracao_minutos)\n"
        "        if horario < fim_existente and fim_novo > existente:\n"
        "            return False\n"
        "    return True"
    ))
    s.append(nota(
        "Se o refactor mudar o comportamento, os testes RED originais acusam na hora. "
        "Essa e a garantia central do TDD: refatorar sem medo."
    ))

    s.append(para("AAA: estrutura de um bom teste", st_h2))
    s.append(code(
        "def test_slot_indisponivel_com_conflito():\n"
        "    # Arrange\n"
        "    existentes = [datetime(2026,7,10,14,0)]\n"
        "    novo = datetime(2026,7,10,14,0)\n"
        "    # Act\n"
        "    resultado = is_slot_available(novo, existentes)\n"
        "    # Assert\n"
        "    assert resultado is False"
    ))

    s.append(para("Fixtures: eliminando repeticao", st_h2))
    s.append(code(
        "@pytest.fixture\n"
        "def horario_base():\n"
        "    return datetime(2026, 7, 10, 14, 0)\n\n"
        "def test_slot_disponivel(horario_base):\n"
        "    assert is_slot_available(horario_base, []) is True"
    ))

    s.append(para("Unitario vs integracao", st_h2))
    s.append(tabela(
        ["Tipo", "O que valida", "Velocidade"],
        [
            ["Unitario", "Uma funcao isolada, sem dependencias externas", "Rapido (ms)"],
            ["Integracao", "Fluxo real, com banco/API de verdade", "Mais lento"],
        ],
        col_widths=[2.4 * 28, 7.1 * 28, 2.5 * 28],
    ))
    s.append(nota(
        "A mecanica e a mesma no Vitest que voce ja usa no Trimote — muda a sintaxe "
        "(pytest no lugar de vitest), nao o habito de test-first com RED visivel."
    ))
    s.append(exercicio([
        "Escreva o teste RED de uma funcao soma(a, b) antes de implementa-la.",
        "Implemente o codigo GREEN minimo para o teste acima passar.",
        "Explique por que escrever o teste depois do codigo tende a produzir testes fracos.",
        "Escreva 3 casos de teste (incluindo bordas) para uma funcao que valida CPF.",
    ]))
    return s


def aula7():
    s = chapter("Aula 7", "Binary Search")
    s.append(para(
        "Binary search encontra um elemento em um array <b>ordenado</b> descartando "
        "metade do espaco de busca a cada passo. A ordenacao previa e a premissa que "
        "sustenta o algoritmo."
    ))
    s.append(para("Implementacao iterativa", st_h2))
    s.append(code(
        "def binary_search(arr, target):\n"
        "    esquerda, direita = 0, len(arr) - 1\n"
        "    while esquerda <= direita:\n"
        "        meio = (esquerda + direita) // 2\n"
        "        if arr[meio] == target:\n"
        "            return meio\n"
        "        elif arr[meio] < target:\n"
        "            esquerda = meio + 1\n"
        "        else:\n"
        "            direita = meio - 1\n"
        "    return -1"
    ))
    s.append(para("Passo a passo — buscando 4 em [1,3,4,7,9,11,13]", st_h3))
    s.append(code(
        "1a: esq=0 dir=6 meio=3 -> arr[3]=7  (7>4, vai p/ esquerda: dir=2)\n"
        "2a: esq=0 dir=2 meio=1 -> arr[1]=3  (3<4, vai p/ direita:  esq=2)\n"
        "3a: esq=2 dir=2 meio=2 -> arr[2]=4  (4==4, retorna indice 2)"
    ))

    s.append(para("O bug classico do meio", st_h2))
    s.append(code(
        "meio = esquerda + (direita - esquerda) // 2   # evita overflow"
    ))
    s.append(nota(
        "Em linguagens com inteiro de tamanho fixo (Java, C++), esquerda + direita pode "
        "estourar o limite do int. Em Python nao ha esse problema (int e ilimitado), mas "
        "e pergunta classica de entrevista — vale entender o porque."
    ))

    s.append(para("Complexidade: aplicando Big O", st_h2))
    s.append(tabela(
        ["Algoritmo", "Complexidade", "Por que"],
        [
            ["Busca linear", "O(n)", "Pior caso: percorre o array todo"],
            ["Binary search", "O(log n)", "Cada passo descarta metade do espaco"],
        ],
        col_widths=[3.0 * 28, 3.0 * 28, 6.0 * 28],
    ))
    s.append(para(
        "Com 1 milhao de elementos: busca linear pode levar 1 milhao de comparacoes; "
        "binary search leva no maximo ~20 (log2 de 1.000.000 ~ 19,9)."
    ))

    s.append(para("bisect: a versao de producao", st_h2))
    s.append(code(
        "from bisect import bisect_left\n\n"
        "arr = [1, 3, 4, 7, 9, 11, 13]\n"
        "i = bisect_left(arr, 4)\n"
        "if i < len(arr) and arr[i] == 4:\n"
        "    print(f'Encontrado no indice {i}')"
    ))
    s.append(nota(
        "Em producao voce usa bisect, nao implementa a mao. bisect_left tambem serve "
        "para insercao ordenada — achar onde um valor entra mantendo a ordem."
    ))
    s.append(atencao(
        "Casos de borda (array vazio, primeiro e ultimo elemento) sao onde binary "
        "search mais quebra: esquerda > direita mal tratado causa loop infinito ou "
        "indice invalido. Sempre teste esses casos."
    ))
    s.append(exercicio([
        "Rode o algoritmo a mao buscando o numero 9 em [1,3,4,7,9,11,13]. Anote cada iteracao.",
        "O que a funcao retorna ao buscar um numero que nao existe? Por que?",
        "Por que binary search nao funciona em um array desordenado?",
        "Escreva os testes (RED) para binary_search cobrindo array vazio e elemento ausente.",
    ]))
    return s


def aula8():
    s = chapter("Aula 8", "Bubble Sort")
    s.append(para(
        "Bubble sort compara pares adjacentes e troca se estiverem fora de ordem. A "
        "cada passada, o maior elemento 'borbulha' ate o fim. E didatico, mas raramente "
        "usado em producao."
    ))
    s.append(para("Implementacao", st_h2))
    s.append(code(
        "def bubble_sort(arr):\n"
        "    n = len(arr)\n"
        "    for i in range(n - 1):\n"
        "        for j in range(n - 1 - i):\n"
        "            if arr[j] > arr[j + 1]:\n"
        "                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n"
        "    return arr"
    ))
    s.append(para(
        "n - 1 - i reduz o alcance da varredura a cada passada, porque os i maiores "
        "elementos ja estao fixos no fim."
    ))
    s.append(para("Passo a passo — 1a passada de [6,5,3,1,8,7,2,4]", st_h3))
    s.append(code(
        "[6,5,...] 6>5 troca -> [5,6,3,1,8,7,2,4]\n"
        "         6>3 troca -> [5,3,6,1,8,7,2,4]\n"
        "         6>1 troca -> [5,3,1,6,8,7,2,4]\n"
        "         6>8? nao\n"
        "         8>7 troca -> [5,3,1,6,7,8,2,4]\n"
        "         8>2 troca -> [5,3,1,6,7,2,8,4]\n"
        "         8>4 troca -> [5,3,1,6,7,2,4,8]  (8 chegou ao fim)"
    ))

    s.append(para("Otimizacao: parada antecipada", st_h2))
    s.append(code(
        "def bubble_sort_otimizado(arr):\n"
        "    n = len(arr)\n"
        "    for i in range(n - 1):\n"
        "        trocou = False\n"
        "        for j in range(n - 1 - i):\n"
        "            if arr[j] > arr[j + 1]:\n"
        "                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n"
        "                trocou = True\n"
        "        if not trocou:\n"
        "            break   # ja esta ordenado, para\n"
        "    return arr"
    ))

    s.append(para("Complexidade", st_h2))
    s.append(tabela(
        ["Caso", "Complexidade", "Cenario"],
        [
            ["Melhor", "O(n)", "Array ja ordenado (com otimizacao)"],
            ["Medio", "O(n^2)", "Ordem aleatoria"],
            ["Pior", "O(n^2)", "Ordem inversa"],
        ],
        col_widths=[2.5 * 28, 3.5 * 28, 6.0 * 28],
    ))
    s.append(atencao(
        "Ninguem usa bubble sort em producao. Python ja tem sorted() e .sort(), "
        "implementados com Timsort (O(n log n) garantido, otimizado em C). Bubble "
        "sort existe por valor didatico — em codigo real, sempre sorted()."
    ))
    s.append(code(
        "arr = [6, 5, 3, 1, 8, 7, 2, 4]\n"
        "print(sorted(arr))   # [1,2,3,4,5,6,7,8] — muito mais rapido"
    ))
    s.append(exercicio([
        "Complete a mao a 2a passada do bubble sort sobre [5,3,1,6,7,2,4,8].",
        "O que a flag 'trocou' economiza, e em qual cenario ela mais ajuda?",
        "Por que o alcance do loop interno diminui com n - 1 - i?",
        "Compare a curva O(n^2) do bubble com O(log n) do binary search para n = 1.000.000.",
    ]))
    return s


def aula9():
    s = chapter("Aula 9", "Ferramentas, sites e comunidades")
    s.append(para(
        "Pratica constante e o que consolida a teoria. Abaixo, ferramentas atuais "
        "organizadas por objetivo, para montar uma rotina de treino."
    ))
    s.append(para("Pratica de algoritmos e logica", st_h2))
    s.extend(bullets([
        "<b>LeetCode</b> — referencia em algoritmos e estruturas de dados, do "
        "iniciante ao avancado; foco em preparacao para entrevistas.",
        "<b>HackerRank</b> — desafios em varias categorias (algoritmos, matematica, "
        "IA), com avaliacao automatica do codigo.",
        "<b>Codewars</b> — pratica gamificada via 'kata' que aumentam de dificuldade; "
        "otimo para criar habito diario.",
        "<b>Exercism</b> — open source, com mentoria humana revisando seu codigo.",
        "<b>Beecrowd</b> (ex-URI) — brasileiro, +3000 problemas com enunciado em "
        "portugues; bom para fixar logica sem barreira de idioma.",
        "<b>Codeforces</b> — programacao competitiva, nivel avancado; proximo passo "
        "quando o LeetCode ficar confortavel.",
    ]))
    s.append(para("Foco em Python", st_h2))
    s.extend(bullets([
        "<b>awesome-python</b> (github.com/vinta/awesome-python) — lista curada de "
        "bibliotecas por categoria.",
        "<b>Python Fluente</b> (pythonfluente.com) — referencia em Python idiomatico.",
        "<b>Real Python</b> (realpython.com) — tutoriais aprofundados.",
        "<b>PyBites / Python Morsels</b> — exercicios curtos focados em escrever "
        "Python idiomatico, nao so logica generica.",
    ]))
    s.append(para("Comunidades e foruns (BR)", st_h2))
    s.extend(bullets([
        "<b>TabNews</b> — 'Hacker News brasileiro' de Filipe Deschamps; referencia "
        "de discussao tecnica em portugues.",
        "<b>DIO</b> — bootcamps gratuitos e Discord ativo.",
        "<b>Discord Python Brasil</b> — servidor focado em Python em portugues.",
        "<b>Discord da Rocketseat</b> — categorias por linguagem, banco, agil e IA.",
    ]))
    s.append(para("Preparacao para entrevista", st_h2))
    s.extend(bullets([
        "<b>CodeSignal</b> — exercicios no formato usado em processos seletivos.",
        "<b>Codility</b> — plataforma que as proprias empresas usam para testes tecnicos.",
    ]))
    s.append(nota(
        "Muitos Tech Leads preferem contratar quem e ativo em comunidade ou open "
        "source a analisar curriculos frios. Isso reforca a estrategia de 'build in "
        "public' — mostrar o que voce constroi vale como portfolio."
    ))
    s.append(para("Montando a rotina", st_h2))
    s.append(tabela(
        ["Objetivo", "Ferramenta"],
        [
            ["Fixar logica todo dia, sem pressao", "Codewars, Beecrowd"],
            ["Algoritmos + estrutura de dados serio", "LeetCode, Codeforces"],
            ["Python idiomatico", "PyBites, Python Morsels"],
            ["Tirar duvida / rede de contatos BR", "TabNews, Discord PyBR, DIO"],
            ["Preparar para processo seletivo", "CodeSignal, Codility"],
        ],
        col_widths=[6.5 * 28, 5.5 * 28],
    ))
    s.append(exercicio([
        "Escolha 1 plataforma de pratica e resolva 1 desafio facil por dia nesta semana.",
        "Crie conta no TabNews e leia 3 discussoes tecnicas sobre um tema que voce estuda.",
        "Implemente do zero (sem consultar) o binary_search e o bubble_sort desta apostila.",
    ]))
    return s


def exercicio_final():
    s = chapter("Exercicio final", "Web scraping assincrono")
    s.append(para(
        "Objetivo: implementar um web scraping usando Python e asyncio para analisar "
        "os dados de uma pagina web. Portamos a versao original (que usava "
        "ThreadPoolExecutor + requests) para asyncio + aiohttp."
    ))
    s.append(para("Decisoes de projeto", st_h2))
    s.extend(bullets([
        "Escrita do CSV movida para o final, depois de todas as coroutines "
        "terminarem — elimina a race condition da versao original (cada thread "
        "abria o arquivo em modo append e escrevia direto, sem lock).",
        "Checagem de duplicidade por titulo antes de gravar, ausente na versao "
        "original.",
    ]))
    s.append(nota(
        "Dependencia nova: <b>pip install aiohttp</b> — cliente HTTP assincrono que "
        "substitui o requests (sincrono, que bloqueia a thread durante a espera de rede)."
    ))

    # ------------- PARTE A -------------
    s.append(para("Parte A — o codigo completo", st_h2))
    s.append(code(
        "import asyncio\n"
        "import csv\n"
        "import time\n"
        "from typing import Optional\n\n"
        "import aiohttp\n"
        "from bs4 import BeautifulSoup\n\n"
        "BASE_URL = 'https://havokkmorands.github.io/movie-catalog/'\n"
        "OUTPUT_FILE = 'movies_async.csv'\n"
        "MAX_CONCURRENT_REQUESTS = 10\n"
        "REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=20)\n\n"
        "HEADERS = {\n"
        "    'User-Agent': 'Mozilla/5.0 ... Chrome/124.0.0.0 Safari/537.36',\n"
        "    'Accept-Language': 'en-US,en;q=0.9',\n"
        "}"
    ))
    s.append(code(
        "async def fetch_html(session, url):\n"
        "    try:\n"
        "        async with session.get(url, headers=HEADERS,\n"
        "                                timeout=REQUEST_TIMEOUT) as response:\n"
        "            response.raise_for_status()\n"
        "            return await response.text()\n"
        "    except (aiohttp.ClientError, asyncio.TimeoutError) as error:\n"
        "        print(f'Falha ao acessar {url}: {error}')\n"
        "        return None"
    ))
    s.append(code(
        "def extract_movie_links(html):\n"
        "    soup = BeautifulSoup(html, 'html.parser')\n"
        "    container = soup.find('section', attrs={'data-testid': 'movies-list'})\n"
        "    if container is None:\n"
        "        return []\n"
        "    items = container.find_all('article', attrs={'data-testid': 'movie-item'})\n"
        "    return [\n"
        "        'https://havokkmorands.github.io/' + a['href']\n"
        "        for item in items\n"
        "        if (a := item.find('a', attrs={'data-testid': 'movie-link'}, href=True))\n"
        "    ]"
    ))
    s.append(code(
        "def parse_movie_details(html, movie_link):\n"
        "    soup = BeautifulSoup(html, 'html.parser')\n"
        "    detail = soup.find('section', attrs={'data-testid': 'movie-detail'})\n"
        "    if detail is None:\n"
        "        return None\n\n"
        "    def get_field(testid, prefix=''):\n"
        "        tag = detail.find(attrs={'data-testid': testid})\n"
        "        return tag.get_text(strip=True).replace(prefix, '').strip() if tag else None\n\n"
        "    movie = {\n"
        "        'title':  get_field('movie-title'),\n"
        "        'date':   get_field('movie-release', 'Lancamento:'),\n"
        "        'rating': get_field('movie-rating', 'Nota:'),\n"
        "        'plot':   get_field('movie-synopsis', 'Sinopse:'),\n"
        "    }\n"
        "    return movie if all(movie.values()) else None"
    ))
    s.append(code(
        "async def fetch_movie(session, semaphore, movie_link):\n"
        "    async with semaphore:\n"
        "        html = await fetch_html(session, movie_link)\n"
        "        return parse_movie_details(html, movie_link) if html else None"
    ))
    s.append(code(
        "def save_movies(movies):\n"
        "    seen_titles = set()\n"
        "    unique = []\n"
        "    for movie in movies:\n"
        "        if movie['title'] in seen_titles:\n"
        "            continue\n"
        "        seen_titles.add(movie['title'])\n"
        "        unique.append(movie)\n\n"
        "    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:\n"
        "        writer = csv.writer(f)\n"
        "        writer.writerow(['title', 'date', 'rating', 'plot'])\n"
        "        for m in unique:\n"
        "            writer.writerow([m['title'], m['date'], m['rating'], m['plot']])"
    ))
    s.append(code(
        "async def main():\n"
        "    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)\n"
        "    async with aiohttp.ClientSession() as session:\n"
        "        index_html = await fetch_html(session, BASE_URL)\n"
        "        if index_html is None:\n"
        "            return\n"
        "        movie_links = extract_movie_links(index_html)\n"
        "        tasks = [fetch_movie(session, semaphore, link) for link in movie_links]\n"
        "        results = await asyncio.gather(*tasks)\n"
        "    movies = [m for m in results if m is not None]\n"
        "    save_movies(movies)\n\n"
        "if __name__ == '__main__':\n"
        "    asyncio.run(main())"
    ))

    # ------------- PARTE B -------------
    s.append(para("Parte B — explicacao linha por linha", st_h2))

    s.append(para("Imports", st_h3))
    s.append(tabela(
        ["Import", "Papel"],
        [
            ["asyncio", "Fornece Semaphore, gather, run e o event loop."],
            ["csv", "Escreve CSV tratando virgulas/aspas dentro dos campos."],
            ["time", "Mede o tempo de execucao do script."],
            ["Optional", "Type hint: 'ou str, ou None'. Documenta a intencao."],
            ["aiohttp", "Cliente HTTP assincrono; substituto do requests."],
            ["BeautifulSoup", "Parser de HTML; nao muda entre versao sync e async."],
        ],
        col_widths=[3.0 * 28, 9.0 * 28],
    ))
    s.append(nota(
        "BeautifulSoup nao e async porque parsing de HTML e processamento local, nao "
        "I/O — nao ha o que aguardar."
    ))

    s.append(para("Constantes de configuracao", st_h3))
    s.extend(bullets([
        "<b>MAX_CONCURRENT_REQUESTS = 10</b> — limita quantas requisicoes HTTP ficam "
        "abertas ao mesmo tempo. E o equivalente ao MAX_THREADS da versao original.",
        "<b>REQUEST_TIMEOUT</b> — no aiohttp o timeout e um objeto (ClientTimeout), "
        "que permite granularidade. total=20 e o timeout global da operacao.",
    ]))

    s.append(para("Headers", st_h3))
    s.append(para(
        "O <b>User-Agent</b> faz a requisicao parecer vinda de um navegador. Sem ele, "
        "muitos servidores identificam o User-Agent padrao de bibliotecas (ex: "
        "python-requests) e bloqueiam. O <b>Accept-Language</b> fixa o idioma do "
        "conteudo, evitando resultado inconsistente entre execucoes."
    ))

    s.append(para("fetch_html — a requisicao", st_h3))
    s.extend(bullets([
        "<b>async def</b> — declara coroutine; chamar nao executa, so cria o objeto.",
        "<b>session</b> como parametro — reusa o pool de conexoes TCP; criar sessao "
        "nova a cada chamada desperdicaria esse reaproveitamento.",
        "<b>async with session.get(...)</b> — versao assincrona do with; garante o "
        "fechamento da conexao mesmo em erro, e o await implicito pausa a coroutine "
        "esperando a resposta.",
        "<b>raise_for_status()</b> — levanta excecao em erro HTTP (404, 500); sem "
        "isso, uma pagina de erro seria tratada como valida.",
        "<b>await response.text()</b> — baixar o corpo tambem e I/O, entao precisa "
        "de await.",
        "<b>except especifico</b> — captura ClientError e TimeoutError, nao Exception "
        "generico, para nao esconder bugs do proprio codigo.",
        "<b>return None</b> — em falha, devolve None em vez de derrubar tudo; assim "
        "a falha de um filme nao interrompe os outros.",
    ]))

    s.append(para("extract_movie_links — parse da pagina indice", st_h3))
    s.extend(bullets([
        "Nao e async: so processa uma string ja baixada.",
        "<b>data-testid</b> sao atributos que o site expoe para automacao/testes "
        "(padrao de Cypress/Playwright), reaproveitados aqui para scraping.",
        "<b>Guard clause</b> (if container is None) aborta cedo em vez de quebrar "
        "adiante com AttributeError.",
        "<b>Walrus (:=)</b> na list comprehension atribui e testa na mesma expressao: "
        "so inclui o link se a tag &lt;a&gt; existir e tiver href.",
        "O href e relativo, entao e concatenado com o dominio para virar URL completa.",
    ]))

    s.append(para("parse_movie_details — dados de cada filme", st_h3))
    s.extend(bullets([
        "<b>movie_link</b> serve so para log de erro, nao para logica.",
        "<b>Funcao aninhada get_field</b> — extrai uma vez o padrao 'busca tag -> "
        "pega texto -> remove prefixo -> tira espaco', reusado nos 4 campos.",
        "<b>get_text(strip=True)</b> pega so o texto visivel, sem tags internas.",
        "<b>all(movie.values())</b> — so devolve o filme se TODOS os 4 campos foram "
        "extraidos; se faltou um, descarta o registro (validacao de integridade).",
    ]))

    s.append(para("fetch_movie — controle de concorrencia", st_h3))
    s.extend(bullets([
        "<b>Semaphore</b> e um contador que limita quantas coroutines entram no "
        "bloco ao mesmo tempo. Com Semaphore(10), a 11a fica pausada esperando vaga.",
        "<b>async with semaphore</b> consome uma vaga ao entrar e devolve ao sair "
        "(mesmo em erro). Faz o papel do MAX_THREADS.",
        "O semaforo esta DENTRO desta funcao para limitar requisicoes ABERTAS, nao "
        "tarefas criadas: as 50 tarefas sao criadas de uma vez, mas so 10 fazem "
        "rede ao mesmo tempo.",
    ]))

    s.append(para("save_movies — duplicidade + escrita", st_h3))
    s.extend(bullets([
        "<b>set()</b> para seen_titles: checar 'in set' e O(1); em lista seria O(n). "
        "E o habito certo — estrutura de dados adequada a operacao dominante.",
        "Este e o ponto que resolve a race condition: a escrita so ocorre depois que "
        "todas as coroutines terminaram, num loop sequencial simples.",
        "<b>mode='w'</b> sobrescreve o arquivo (o 'a' original acumulava e duplicava "
        "entre execucoes).",
        "<b>newline=''</b> — exigencia do modulo csv; sem isso, no Windows sairiam "
        "linhas em branco extras.",
        "<b>encoding='utf-8'</b> — garante acentos corretos independente do SO.",
        "<b>writer.writerow</b> trata virgulas/aspas dentro dos campos "
        "automaticamente.",
    ]))

    s.append(para("main — orquestracao", st_h3))
    s.extend(bullets([
        "<b>Semaphore criado uma vez</b> e passado a todas as tarefas: precisa ser o "
        "MESMO objeto, senao nao ha limite real.",
        "<b>ClientSession</b> criada uma vez, reusada por todas as requisicoes, "
        "fechada ao sair do async with.",
        "<b>tasks = [...]</b> — a list comprehension NAO executa nada: so cria os "
        "objetos coroutine.",
        "<b>await asyncio.gather(*tasks)</b> — aqui tudo comeca a rodar "
        "concorrentemente; results volta na MESMA ordem das tarefas.",
        "<b>[m for m in results if m is not None]</b> — descarta os None (falhas) "
        "antes de salvar.",
    ]))

    s.append(para("Bloco de entrada", st_h3))
    s.append(para(
        "<b>if __name__ == '__main__'</b> so roda ao executar o arquivo diretamente. "
        "<b>asyncio.run(main())</b> cria o event loop, roda main() ate o fim e fecha "
        "o loop — e o que 'liga a energia' de todas as coroutines."
    ))

    s.append(para("O que muda vs a versao em threading", st_h2))
    s.append(tabela(
        ["Threading (original)", "Async (esta versao)"],
        [
            ["requests.get() bloqueia a thread", "session.get() com await libera o loop"],
            ["MAX_THREADS + executor.map()", "Semaphore(10) dentro do gather()"],
            ["Cada thread escreve direto (append)", "CSV escrito uma vez, no final"],
            ["Sem checagem de duplicidade", "seen_titles filtra antes de gravar"],
        ],
        col_widths=[6.0 * 28, 6.0 * 28],
    ))
    s.append(atencao(
        "O parse_movie_details roda BeautifulSoup dentro da coroutine — parsing e "
        "CPU-bound e bloqueia o event loop enquanto executa. Para este volume o "
        "impacto e irrelevante (o gargalo e a rede). Se escalar para milhares de "
        "paginas com HTML pesado, mova o parsing para loop.run_in_executor()."
    ))
    s.append(exercicio([
        "Rode o script e confira o movies_async.csv gerado. Quantos filmes vieram?",
        "Mude MAX_CONCURRENT_REQUESTS para 1 e para 50. O tempo total muda? Por que?",
        "Explique com suas palavras por que a versao async nao tem race condition na escrita.",
        "Sugira a mensagem de commit (Conventional Commits) para adicionar este script ao repo.",
    ]))
    return s

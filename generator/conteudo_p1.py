# -*- coding: utf-8 -*-
"""Conteudo parte 1: capa/sumario, glossario e Aulas 1-5."""

from gerar_apostila import (
    para, bullets, code, nota, atencao, exercicio, tabela, chapter,
    Spacer, PageBreak, Paragraph,
    st_h2, st_h3, st_body, st_toc, st_toc_b, st_chapter_eyebrow, st_chapter,
)


def sumario():
    s = [PageBreak(), Paragraph("SUMARIO", st_chapter), Spacer(1, 14)]
    itens = [
        ("Glossario de termos essenciais", True),
        ("Aula 1 — Sincrono, assincrono e processos", True),
        ("Aula 2 — Yield e Generators", True),
        ("Aula 3 — Coroutines e o event loop", True),
        ("Aula 4 — CPU parte 1: multiprocessing", True),
        ("Aula 5 — Threads parte 2", True),
        ("Aula 6 — TDD (Test Driven Development)", True),
        ("Aula 7 — Binary Search", True),
        ("Aula 8 — Bubble Sort", True),
        ("Aula 9 — Ferramentas, sites e comunidades", True),
        ("Exercicio final — Web scraping assincrono", True),
        ("   Parte A: o codigo completo", False),
        ("   Parte B: explicacao linha por linha", False),
    ]
    for txt, bold in itens:
        s.append(Paragraph(txt, st_toc_b if bold else st_toc))
    return s


def glossario():
    s = chapter("Referencia", "Glossario de termos essenciais")
    s.append(para(
        "Este modulo usa muitos termos que se confundem facilmente. Leia este "
        "glossario antes das aulas e volte a ele sempre que precisar. Cada termo "
        "e retomado em profundidade no capitulo correspondente."
    ))

    s.append(para("Concorrencia e paralelismo", st_h2))
    s.append(tabela(
        ["Termo", "O que e", "Analogia"],
        [
            ["Sincrono", "Uma tarefa por vez; cada uma espera a anterior terminar.",
             "Fila unica no caixa"],
            ["Assincrono", "Enquanto uma tarefa espera I/O, outra roda; nao bloqueia.",
             "Garcom que anota varias mesas sem esperar a cozinha"],
            ["Concorrencia", "Varias tarefas em progresso, alternando o uso do recurso.",
             "Um cozinheiro alternando entre panelas"],
            ["Paralelismo", "Varias tarefas rodando de fato ao mesmo tempo.",
             "Varios cozinheiros, um por panela"],
        ],
        col_widths=[2.6 * 28, 5.9 * 28, 3.5 * 28],
    ))

    s.append(para("Unidades de execucao", st_h2))
    s.append(tabela(
        ["Termo", "Definicao"],
        [
            ["Processo", "Instancia de um programa, com memoria propria e isolada."],
            ["Thread", "Unidade de execucao dentro de um processo; compartilha a memoria dele."],
            ["Coroutine", "Funcao que pode pausar (await) e retomar, gerenciada pelo event loop."],
            ["Event loop", "Agendador que decide qual coroutine roda a cada ponto de pausa."],
            ["Task", "Coroutine ja agendada no event loop, rodando concorrentemente."],
        ],
        col_widths=[2.6 * 28, 9.4 * 28],
    ))

    s.append(para("Conceitos-chave", st_h2))
    s.append(tabela(
        ["Termo", "Definicao"],
        [
            ["GIL", "Global Interpreter Lock: trava do CPython que so deixa UMA thread "
                    "executar bytecode Python por vez."],
            ["I/O-bound", "Tarefa limitada por espera externa (rede, disco, banco)."],
            ["CPU-bound", "Tarefa limitada por processamento (calculo, hashing)."],
            ["Generator", "Funcao com yield que produz valores sob demanda, guardando o estado."],
            ["yield", "Pausa a funcao, devolve um valor e preserva o ponto de execucao."],
            ["await", "Suspende a coroutine atual e devolve o controle ao event loop."],
            ["Semaphore", "Contador que limita quantas tarefas entram numa secao ao mesmo tempo."],
            ["Lock", "Garante que so uma thread execute a secao critica por vez."],
            ["Race condition", "Bug por acesso concorrente nao sincronizado ao mesmo dado."],
            ["TDD", "Test Driven Development: escreve o teste antes do codigo."],
            ["Big O", "Notacao que descreve como o custo cresce com o tamanho da entrada."],
            ["IPC", "Inter-Process Communication: troca de dados entre processos isolados."],
        ],
        col_widths=[2.6 * 28, 9.4 * 28],
    ))

    s.append(nota(
        "Regra mental para o modulo inteiro: <b>I/O-bound pede assincrono/threads</b>; "
        "<b>CPU-bound pede multiprocessing</b>. Quase toda decisao de concorrencia "
        "em Python nasce dessa distincao por causa do GIL."
    ))
    return s


def aula1():
    s = chapter("Aula 1", "Sincrono, assincrono e processos")

    s.append(para("Codigo sincrono", st_h2))
    s.append(para(
        "Em codigo sincrono, cada instrucao espera a anterior terminar. A thread "
        "principal fica <b>bloqueada</b> ate a operacao concluir. Se a consulta ao "
        "banco leva 200ms, a aplicacao trava por 200ms naquela linha."
    ))
    s.append(code(
        "def get_product(product_id):\n"
        "    product = Product.objects.get(id=product_id)\n"
        "    return product"
    ))

    s.append(para("Codigo assincrono", st_h2))
    s.append(para(
        "Assincrono libera a thread para outra tarefa enquanto espera. O <b>await</b> "
        "nao e uma espera bloqueante: e um ponto onde a funcao devolve o controle ao "
        "event loop, que pode rodar outra coroutine enquanto o banco nao responde."
    ))
    s.append(code(
        "import asyncio\n\n"
        "async def get_product(product_id):\n"
        "    product = await Product.objects.aget(id=product_id)\n"
        "    return product\n\n"
        "async def main():\n"
        "    product = await get_product(1)\n"
        "    print(product)\n\n"
        "asyncio.run(main())"
    ))
    s.append(nota(
        "Voce ja conhece esse modelo do Node.js: o event loop do JavaScript funciona "
        "no mesmo principio (single-thread, nao bloqueante). A diferenca e que em "
        "Python isso e opt-in: voce declara <b>async def</b> e liga o loop com "
        "<b>asyncio.run()</b>."
    ))

    s.append(para("Processo, thread e o GIL", st_h2))
    s.append(para("Um processo e uma instancia de um programa. As unidades se relacionam assim:"))
    s.append(tabela(
        ["Conceito", "O que e", "Isolamento"],
        [
            ["Processo", "Instancia com memoria propria", "Total"],
            ["Thread", "Execucao dentro de um processo", "Compartilha memoria"],
        ],
        col_widths=[2.6 * 28, 5.9 * 28, 3.5 * 28],
    ))
    s.append(para(
        "O <b>GIL (Global Interpreter Lock)</b> muda tudo em Python: o CPython so "
        "permite que uma thread execute bytecode Python por vez, mesmo em maquina "
        "com varios nucleos. Consequencia pratica:"
    ))
    s.extend(bullets([
        "Threads NAO dao paralelismo real para codigo Python puro (CPU-bound). "
        "Ajudam em I/O, porque a thread libera o GIL enquanto espera.",
        "Para paralelismo real de CPU, use multiplos <b>processos</b> "
        "(multiprocessing): cada processo tem seu proprio interpretador e seu "
        "proprio GIL.",
    ]))

    s.append(para("Guia de decisao", st_h3))
    s.append(tabela(
        ["Cenario", "Ferramenta"],
        [
            ["Muitas requisicoes HTTP / consultas ao banco / I/O de rede", "asyncio"],
            ["I/O legado, sem suporte a async", "threading"],
            ["Processamento pesado de CPU (calculo, hashing, ML)", "multiprocessing"],
        ],
        col_widths=[8.5 * 28, 3.5 * 28],
    ))
    s.append(atencao(
        "Na otica de seguranca: um endpoint sincrono que bloqueia o event loop de uma "
        "API async trava o servico inteiro sob carga. E um vetor comum de DoS acidental "
        "— sem ataque sofisticado nenhum."
    ))
    s.append(exercicio([
        "Explique com suas palavras a diferenca entre bloqueante e nao bloqueante.",
        "Voce precisa baixar 50 paginas web. CPU-bound ou I/O-bound? Qual ferramenta?",
        "Voce precisa calcular o hash SHA-256 de 10.000 arquivos. Qual ferramenta e por que o GIL importa aqui?",
        "Por que threads nao aceleram um loop de calculo puro em Python?",
    ]))
    return s


def aula2():
    s = chapter("Aula 2", "Yield e Generators")
    s.append(para(
        "Generators sao a base para entender async/await. Uma funcao com <b>yield</b> "
        "vira um generator: pausa no yield, devolve um valor e mantem todo o estado "
        "local ate ser chamada de novo."
    ))
    s.append(para("return vs yield", st_h2))
    s.append(code(
        "def get_products_normal():\n"
        "    products = Product.objects.all()\n"
        "    return list(products)      # carrega TUDO na memoria\n\n"
        "def get_products_lazy():\n"
        "    for product in Product.objects.all():\n"
        "        yield product          # devolve um de cada vez, sob demanda"
    ))
    s.append(para(
        "Chamar <b>get_products_lazy()</b> nao executa nada: so cria o objeto "
        "generator. O codigo so roda quando voce itera (next() ou for)."
    ))
    s.append(code(
        "gen = get_products_lazy()\n"
        "print(next(gen))   # executa ate o primeiro yield\n"
        "print(next(gen))   # continua de onde parou"
    ))

    s.append(para("Por que importa: memoria", st_h2))
    s.append(para(
        "Se voce tem uma tabela com 2 milhoes de linhas e faz .all() numa lista, "
        "carrega tudo na RAM. Com generator, processa um registro por vez:"
    ))
    s.append(code(
        "def process_large_dataset(filepath):\n"
        "    with open(filepath) as f:\n"
        "        for line in f:\n"
        "            yield line.strip().split(',')\n\n"
        "for row in process_large_dataset('logs_2026.csv'):\n"
        "    processar(row)   # nunca carrega o arquivo inteiro"
    ))
    s.append(nota(
        "Isso e diretamente util em relatorios financeiros com milhares de transacoes: "
        "um generator evita estourar a memoria do servidor ao gerar o relatorio."
    ))

    s.append(para("Generator expressions", st_h2))
    s.append(code(
        "squares = (x**2 for x in range(1_000_000))   # generator, lazy\n"
        "squares_list = [x**2 for x in range(1_000_000)]  # lista inteira na memoria"
    ))
    s.append(para(
        "Regra pratica: se voce so vai iterar uma vez (sum, for), use generator "
        "expression. Se precisa de indice ou reuso, use lista."
    ))

    s.append(para("send(): a ponte para coroutines", st_h2))
    s.append(para("O yield tambem recebe valor de volta — e isso que a Aula 3 usa:"))
    s.append(code(
        "def accumulator():\n"
        "    total = 0\n"
        "    while True:\n"
        "        value = yield total\n"
        "        total += value\n\n"
        "acc = accumulator()\n"
        "next(acc)            # 'prime': avanca ate o primeiro yield\n"
        "print(acc.send(10))  # total = 10\n"
        "print(acc.send(5))   # total = 15"
    ))
    s.append(para(
        "Esse mecanismo de pausar, receber algo e continuar e literalmente o que "
        "async def + await fazem por baixo dos panos."
    ))
    s.append(exercicio([
        "Escreva um generator contar_ate(n) que produz de 1 ate n usando yield.",
        "Qual a diferenca de memoria entre [x for x in range(10**7)] e (x for x in range(10**7))?",
        "O que acontece se voce chamar next() num generator ja esgotado?",
        "Escreva um generator que le um arquivo e produz apenas as linhas que contem a palavra ERROR.",
    ]))
    return s


def aula3():
    s = chapter("Aula 3", "Coroutines e o event loop")
    s.append(para(
        "async def cria uma <b>coroutine</b>, que e um generator especializado por "
        "baixo dos panos. Chamar a funcao nao executa o corpo — so cria o objeto."
    ))
    s.append(code(
        "async def get_product(product_id):\n"
        "    return await db.fetch(product_id)\n\n"
        "result = get_product(1)\n"
        "print(result)   # <coroutine object ...>  (nao executou ainda)"
    ))

    s.append(para("O que o await faz", st_h2))
    s.extend(bullets([
        "Suspende a coroutine atual no ponto do await.",
        "Devolve o controle ao event loop.",
        "Quando o valor esperado estiver pronto, o event loop retoma a coroutine "
        "de onde parou, com as variaveis locais intactas.",
    ]))
    s.append(code(
        "import asyncio, time\n\n"
        "async def fetch_product(id, delay):\n"
        "    print(f'Buscando produto {id}...')\n"
        "    await asyncio.sleep(delay)   # simula I/O, nao trava a thread\n"
        "    print(f'Produto {id} pronto')\n"
        "    return id\n\n"
        "async def main():\n"
        "    start = time.time()\n"
        "    resultados = await asyncio.gather(\n"
        "        fetch_product(1, 2),\n"
        "        fetch_product(2, 1),\n"
        "    )\n"
        "    print(f'Total: {time.time() - start:.1f}s')\n\n"
        "asyncio.run(main())"
    ))
    s.append(para(
        "O total e ~2s (o maior delay), nao 3s (a soma). As duas coroutines rodam "
        "concorrentemente porque asyncio.sleep libera o event loop."
    ))

    s.append(para("O erro classico: sleep errado", st_h2))
    s.append(code(
        "async def errado():\n"
        "    time.sleep(2)          # BLOQUEIA o event loop inteiro\n\n"
        "async def certo():\n"
        "    await asyncio.sleep(2) # libera o loop para outras coroutines"
    ))
    s.append(atencao(
        "Um unico time.sleep(), uma chamada sincrona de banco ou uma lib HTTP sincrona "
        "dentro de uma rota async do FastAPI/Django trava o servidor para TODOS os "
        "usuarios. E o vetor de DoS acidental mais comum em codigo assincrono."
    ))

    s.append(para("Coroutine, Task e event loop", st_h2))
    s.append(tabela(
        ["Termo", "Papel"],
        [
            ["Coroutine", "A 'receita': objeto de async def, ainda nao agendado."],
            ["Task", "Coroutine agendada (create_task/gather), rodando concorrentemente."],
            ["Event loop", "O agendador que decide qual coroutine roda a cada await."],
        ],
        col_widths=[2.6 * 28, 9.4 * 28],
    ))
    s.append(code(
        "async def main():\n"
        "    task1 = asyncio.create_task(fetch_product(1, 2))\n"
        "    task2 = asyncio.create_task(fetch_product(2, 1))\n"
        "    await task1\n"
        "    await task2"
    ))
    s.append(nota(
        "gather() cria e aguarda varias coroutines de uma vez — o jeito mais comum "
        "quando voce ja sabe todas de antemao. create_task() da mais controle: dispara "
        "algo e deixa voce continuar antes de esperar o resultado."
    ))
    s.append(exercicio([
        "Reescreva duas chamadas sequenciais com await para rodarem concorrentemente com gather.",
        "Por que o corpo de uma coroutine nao executa ao ser chamada sem await?",
        "O que aconteceria com o tempo total se voce trocasse asyncio.sleep por time.sleep no exemplo?",
        "Qual a diferenca entre uma coroutine e uma Task?",
    ]))
    return s


def aula4():
    s = chapter("Aula 4", "CPU parte 1: multiprocessing")
    s.append(para(
        "Aqui asyncio para de ajudar. Async resolve I/O-bound. Para CPU-bound o GIL "
        "trava tudo numa thread — a saida e processos separados, cada um com seu "
        "interpretador e seu proprio GIL."
    ))
    s.append(para("multiprocessing.Process", st_h2))
    s.append(code(
        "from multiprocessing import Process\n\n"
        "def cpu_bound(n):\n"
        "    return sum(i * i for i in range(n))\n\n"
        "if __name__ == '__main__':\n"
        "    p1 = Process(target=cpu_bound, args=(50_000_000,))\n"
        "    p2 = Process(target=cpu_bound, args=(50_000_000,))\n"
        "    p1.start(); p2.start()\n"
        "    p1.join();  p2.join()"
    ))
    s.append(atencao(
        "O <b>if __name__ == '__main__':</b> nao e estilo — e obrigatorio. No Windows "
        "o multiprocessing recria o processo importando o modulo do zero; sem essa "
        "guarda, voce entra em loop infinito de criacao de processos."
    ))

    s.append(para("Recuperando o retorno com Queue", st_h2))
    s.append(para(
        "O return de um processo filho nao volta sozinho ao pai — a memoria e isolada. "
        "Para trazer o resultado, usa-se IPC (Queue, Pipe, Value/Array):"
    ))
    s.append(code(
        "from multiprocessing import Process, Queue\n\n"
        "def cpu_bound(n, queue):\n"
        "    queue.put(sum(i * i for i in range(n)))\n\n"
        "if __name__ == '__main__':\n"
        "    queue = Queue()\n"
        "    p1 = Process(target=cpu_bound, args=(10_000_000, queue))\n"
        "    p1.start(); p1.join()\n"
        "    print(queue.get())"
    ))

    s.append(para("ProcessPoolExecutor: o padrao real", st_h2))
    s.append(code(
        "from concurrent.futures import ProcessPoolExecutor\n\n"
        "def cpu_bound(n):\n"
        "    return sum(i * i for i in range(n))\n\n"
        "if __name__ == '__main__':\n"
        "    with ProcessPoolExecutor() as executor:\n"
        "        resultados = list(executor.map(cpu_bound, [50_000_000, 50_000_000]))\n"
        "    print(resultados)   # retorno automatico, sem Queue manual"
    ))

    s.append(para("Custo e quando NAO usar", st_h2))
    s.append(para(
        "Criar processo tem custo alto: o SO aloca memoria nova e inicializa um "
        "interpretador do zero. So compensa para tarefas pesadas o suficiente."
    ))
    s.append(tabela(
        ["Tarefa", "Ferramenta"],
        [
            ["Calcular hash de milhares de arquivos", "multiprocessing"],
            ["Redimensionar centenas de imagens", "multiprocessing"],
            ["Chamar 100 APIs externas", "asyncio"],
            ["Ler 100 arquivos do disco", "asyncio ou threading"],
        ],
        col_widths=[8.5 * 28, 3.5 * 28],
    ))
    s.append(exercicio([
        "Por que o return de um processo filho nao chega ao processo pai sozinho?",
        "Reescreva o exemplo de Queue usando ProcessPoolExecutor.",
        "Explique por que criar um processo para uma tarefa minima pode ser mais lento que faze-la direto.",
        "Cite duas tarefas do seu dia a dia que seriam CPU-bound e se beneficiariam de multiprocessing.",
    ]))
    return s


def aula5():
    s = chapter("Aula 5", "Threads parte 2")
    s.append(para(
        "Threads nao dao paralelismo de CPU (o GIL impede), mas dao concorrencia real "
        "em I/O: quando uma thread faz I/O, o GIL e liberado e outra thread roda. "
        "Isso resolve um caso que asyncio nao resolve: <b>bibliotecas sincronas sem "
        "versao async</b>."
    ))
    s.append(para("ThreadPoolExecutor: o padrao de producao", st_h2))
    s.append(code(
        "from concurrent.futures import ThreadPoolExecutor\n"
        "import requests\n\n"
        "def fetch_url(url):\n"
        "    return requests.get(url).status_code\n\n"
        "urls = ['https://api1.com', 'https://api2.com', 'https://api3.com']\n\n"
        "with ThreadPoolExecutor(max_workers=5) as executor:\n"
        "    resultados = list(executor.map(fetch_url, urls))"
    ))
    s.append(nota(
        "Use threads quando a lib disponivel e sincrona (requests) e nao ha opcao "
        "async (httpx/aiohttp). Se ha versao async, asyncio escala melhor."
    ))

    s.append(para("Race condition: o problema das threads", st_h2))
    s.append(para(
        "Threads compartilham memoria. Duas threads escrevendo na mesma variavel ao "
        "mesmo tempo corrompem o dado — mesmo com o GIL, porque ele protege o "
        "interpretador, nao a logica da sua aplicacao."
    ))
    s.append(code(
        "contador = 0\n\n"
        "def incrementar():\n"
        "    global contador\n"
        "    for _ in range(1_000_000):\n"
        "        contador += 1   # NAO e atomico: ler + somar + escrever\n\n"
        "# resultado real fica ABAIXO de 2.000.000 e inconsistente"
    ))
    s.append(para(
        "contador += 1 parece uma operacao, mas sao tres passos (ler, somar, escrever). "
        "O GIL pode trocar de thread entre eles, fazendo uma sobrescrever a outra."
    ))

    s.append(para("Lock: resolvendo a race condition", st_h2))
    s.append(code(
        "lock = threading.Lock()\n"
        "contador = 0\n\n"
        "def incrementar():\n"
        "    global contador\n"
        "    for _ in range(1_000_000):\n"
        "        with lock:          # so uma thread por vez neste bloco\n"
        "            contador += 1"
    ))
    s.append(nota(
        "O Lock deve proteger apenas a secao critica, nunca a funcao inteira — senao "
        "voce elimina o ganho de concorrencia. Isso e a versao em memoria do que o "
        "booking_no_overlap (exclusion constraint) resolve no nivel do banco."
    ))

    s.append(para("Comparativo final", st_h2))
    s.append(tabela(
        ["Criterio", "threading", "asyncio", "multiprocessing"],
        [
            ["Paralelismo de CPU", "Nao", "Nao", "Sim"],
            ["Bom para I/O", "Sim", "Sim (escala +)", "Nao"],
            ["Libs sincronas legadas", "Sim", "Nao", "Sim"],
            ["Overhead de criacao", "Medio", "Muito baixo", "Alto"],
            ["Precisa de Lock", "Sim", "Nao", "Nao (mem. isolada)"],
        ],
        col_widths=[3.6 * 28, 2.8 * 28, 2.9 * 28, 2.7 * 28],
    ))
    s.append(exercicio([
        "Por que uma race condition acontece mesmo existindo o GIL?",
        "Onde exatamente o Lock deve ser colocado, e por que nao na funcao inteira?",
        "Quando voce escolheria threading em vez de asyncio para tarefas de I/O?",
        "Relacione o Lock com uma constraint de banco que voce ja usou.",
    ]))
    return s

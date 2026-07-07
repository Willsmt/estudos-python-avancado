# Estudos — Python Avançado

Estudos do módulo **Python Avançado** do curso Desenvolvedor Full Stack Python: programação assíncrona, concorrência (`asyncio`, threads, multiprocessing), TDD e algoritmos clássicos. Inclui uma apostila em PDF para estudo e um projeto prático de web scraping assíncrono.

## Conteúdo do módulo

| Aula            | Tema                                                          |
| --------------- | ------------------------------------------------------------- |
| Glossário       | Termos essenciais de concorrência, execução e conceitos-chave |
| Aula 1          | Síncrono, assíncrono e processos (GIL)                        |
| Aula 2          | Yield e Generators                                            |
| Aula 3          | Coroutines e o event loop                                     |
| Aula 4          | CPU parte 1: multiprocessing                                  |
| Aula 5          | Threads parte 2 (race condition, Lock)                        |
| Aula 6          | TDD (Test Driven Development)                                 |
| Aula 7          | Binary Search                                                 |
| Aula 8          | Bubble Sort                                                   |
| Aula 9          | Ferramentas, sites e comunidades                              |
| Exercício final | Web scraping assíncrono (asyncio + aiohttp)                   |

## Estrutura

```
estudos-python-avancado/
├── docs/
│   └── modulo_python_avancado.pdf   # apostila completa (28 páginas)
├── exercises/
│   └── asyncio_scraper.py           # exercício final: scraper assíncrono
├── generator/
│   ├── gerar_apostila.py            # infraestrutura (estilos, template, capa)
│   ├── conteudo.py                  # monta a story completa
│   ├── conteudo_p1.py               # glossário + aulas 1-5
│   └── conteudo_p2.py               # aulas 6-9 + exercício final
├── .gitignore
├── requirements.txt
└── README.md
```

## Exercício final: web scraping assíncrono

Scraper de um catálogo de filmes usando `asyncio` + `aiohttp`, portado de uma versão original em `ThreadPoolExecutor` + `requests`. Principais decisões:

- **Concorrência controlada** via `asyncio.Semaphore`, limitando requisições HTTP simultâneas.
- **Sem race condition na escrita:** o CSV é gravado uma única vez, após todas as coroutines terminarem.
- **Validação de integridade:** um filme só é salvo se todos os campos forem extraídos; duplicidade por título é filtrada antes da gravação.

### Como rodar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python exercises/asyncio_scraper.py
```

Saída: `movies_async.csv` no diretório de execução.

## Gerando a apostila

O PDF em `docs/` é gerado via ReportLab a partir dos scripts em `generator/`.

```bash
pip install -r requirements.txt
cd generator
python gerar_apostila.py
```

O arquivo é escrito em `docs/modulo_python_avancado.pdf`.

## Stack

`Python` · `asyncio` · `aiohttp` · `BeautifulSoup` · `pytest` · `ReportLab`

## Autor

Willians martins — [github.com/Willsmt](https://github.com/Willsmt)

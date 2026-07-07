"""Scraper assíncrono do catálogo de filmes (versão asyncio).

Reimplementação do scraper original (ThreadPoolExecutor + requests) usando
asyncio + aiohttp para concorrência via I/O não bloqueante.
"""

import asyncio
import csv
import time
from typing import Optional

import aiohttp
from bs4 import BeautifulSoup

BASE_URL = "https://havokkmorands.github.io/movie-catalog/"
OUTPUT_FILE = "movies_async.csv"
MAX_CONCURRENT_REQUESTS = 10
REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=20)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


async def fetch_html(session: aiohttp.ClientSession, url: str) -> Optional[str]:
    try:
        async with session.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT) as response:
            response.raise_for_status()
            return await response.text()
    except (aiohttp.ClientError, asyncio.TimeoutError) as error:
        print(f"Falha ao acessar {url}: {error}")
        return None


def extract_movie_links(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    container = soup.find("section", attrs={"data-testid": "movies-list"})

    if container is None:
        print("Container principal não encontrado.")
        return []

    movie_items = container.find_all("article", attrs={"data-testid": "movie-item"})
    links = [
        "https://havokkmorands.github.io/" + anchor["href"]
        for item in movie_items
        if (anchor := item.find("a", attrs={"data-testid": "movie-link"}, href=True))
    ]

    if not links:
        print("Nenhum link de filme foi encontrado.")

    return links


def parse_movie_details(html: str, movie_link: str) -> Optional[dict]:
    soup = BeautifulSoup(html, "html.parser")
    detail = soup.find("section", attrs={"data-testid": "movie-detail"})

    if detail is None:
        print(f"Detalhe do filme não encontrado: {movie_link}")
        return None

    def get_field(testid: str, prefix: str = "") -> Optional[str]:
        tag = detail.find(attrs={"data-testid": testid})
        return tag.get_text(strip=True).replace(prefix, "").strip() if tag else None

    movie = {
        "title": get_field("movie-title"),
        "date": get_field("movie-release", "Lançamento:"),
        "rating": get_field("movie-rating", "Nota:"),
        "plot": get_field("movie-synopsis", "Sinopse:"),
    }

    return movie if all(movie.values()) else None


async def fetch_movie(
    session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, movie_link: str
) -> Optional[dict]:
    async with semaphore:
        html = await fetch_html(session, movie_link)
        return parse_movie_details(html, movie_link) if html else None


def save_movies(movies: list[dict]) -> None:
    seen_titles = set()
    unique_movies = []

    for movie in movies:
        if movie["title"] in seen_titles:
            print(f"Filme duplicado ignorado: {movie['title']}")
            continue
        seen_titles.add(movie["title"])
        unique_movies.append(movie)

    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["title", "date", "rating", "plot"])
        for movie in unique_movies:
            writer.writerow([movie["title"], movie["date"], movie["rating"], movie["plot"]])
            print(movie["title"], movie["date"], movie["rating"], movie["plot"])

    print(f"{len(unique_movies)} filmes salvos em {OUTPUT_FILE}")


async def main() -> None:
    start_time = time.time()
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession() as session:
        index_html = await fetch_html(session, BASE_URL)
        if index_html is None:
            print("Não foi possível acessar a página principal.")
            return

        movie_links = extract_movie_links(index_html)
        if not movie_links:
            return

        tasks = [fetch_movie(session, semaphore, link) for link in movie_links]
        results = await asyncio.gather(*tasks)

    movies = [movie for movie in results if movie is not None]
    save_movies(movies)

    print("Tempo total:", time.time() - start_time)


if __name__ == "__main__":
    asyncio.run(main())

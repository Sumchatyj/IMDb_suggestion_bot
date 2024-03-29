import asyncio
import random
import re
import ssl

import aiohttp
import certifi
import requests
from bs4 import BeautifulSoup

from .exceptions import RequestException


HEADERS = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                  " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0"
                  " Safari/537.36"
}

CATEGORIES = {
    "Top_250_Movie": "https://www.imdb.com/chart/top/",
}

IMDB_URL = "https://www.imdb.com"

GENRES = [
    'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime',
    'Drama', 'Family', 'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music',
    'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller',
    'War', 'Western'
]

GENRES_MOVIE = {
    'Top_250_Movie': '',
    'Action_Movie': 'Action',
    'Adventure_Movie': 'Adventure',
    'Animation_Movie': 'Animation',
    'Biography_Movie': 'Biography',
    'Comedy_Movie': 'Comedy',
    'Crime_Movie': 'Crime',
    'Drama_Movie': 'Drama',
    'Family_Movie': 'Family',
    'Fantasy_Movie': 'Fantasy',
    'Film-Noir_Movie': 'Film-Noir',
    'History_Movie': 'History',
    'Horror_Movie': 'Horror',
    'Music_Movie': 'Music',
    'Musical_Movie': 'Musical',
    'Mystery_Movie': 'Mystery',
    'Romance_Movie': 'Romance',
    'Sci-Fi_Movie': 'Sci-Fi',
    'Sport_Movie': 'Sport',
    'Thriller_Movie': 'Thriller',
    'War_Movie': 'War',
    'Western_Movie': 'Western',
}

GENRES_MOVIE_LIST = list(GENRES_MOVIE.keys())


class Client:
    """ClientSession class for requests."""
    def __init__(self) -> None:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        conn = aiohttp.TCPConnector(ssl=ssl_context)
        self.session = aiohttp.ClientSession(connector=conn, headers=HEADERS)


class Title_Single:
    """Class for single title in all genres."""
    def __init__(self, client: Client, category: str) -> None:
        self.client = client
        self.category = category
        self.url = ""
        self.poster = ""
        self.title = ""
        self.genres = []
        self.date = ""
        self.duration = ""
        self.rating = ""
        self.storyline = ""
        self.tags = []

    async def _get_url(self) -> None:
        if self.category == "Top_250_Movie":
            url = "https://www.imdb.com/chart/top/"
            response = await self.client.session.get(url)
            if response.status != 200:
                self.session_close()
                raise RequestException(
                    f"request code in _get_url: {response.status}"
                    f"URL: {url}"
                )
            soup = BeautifulSoup(await response.text(), "lxml")
            position = random.randint(0, 249)
            end_url = soup.tbody.find_all(class_="titleColumn")[
                position
            ].a.get("href")
            self.url = IMDB_URL + end_url
        elif self.category in GENRES_MOVIE:
            position = random.randint(1, 250)
            url = (
                f"https://www.imdb.com/search/title/?title_type=feature&"
                f"num_votes=10000,&genres={GENRES_MOVIE[self.category]}&"
                f"sort=user_rating,desc&start={position}"
            )
            response = await self.client.session.get(url)
            if response.status != 200:
                self.session_close()
                raise RequestException(f"request code: {response.status}")
            soup = BeautifulSoup(await response.text(), "lxml")
            end_url = soup.find(
                class_="lister-item mode-advanced"
            ).a.get('href')
            self.url = IMDB_URL + end_url

    async def _get_from_graphql(self, title_id: str) -> None:
        url = (
            f"https://caching.graphql.imdb.com/?operationName=TMD_Storyline"
            f"&variables=%7B%22titleId%22%3A%22{title_id}%22%7D&extensions="
            f"%7B%22persistedQuery%22%3A%7B%22sha256Hash%22%3A%2287f41463a48a"
            f"f95ebba3129889d17181402622bfd30c8dc9216d99ac984f0091%22%2C%22"
            f"version%22%3A1%7D%7D"
        )
        response = await self.client.session.get(
            url, headers={"content-type": "application/json"}
        )
        if response.status != 200:
            self.session_close()
            raise RequestException(
                f"request code in _get_from_graphql: {response.status}"
                f"URL: {url}"
            )
        response_data = await response.json()
        self.storyline = (
            response_data.get("data")
            .get("title")
            .get("summaries")
            .get("edges")[0]
            .get("node")
            .get("plotText")
            .get("plaidHtml")
        )
        self.storyline_format()
        tags_row = (
            response_data.get("data")
            .get("title")
            .get("storylineKeywords")
            .get("edges")
        )
        for tag in tags_row:
            self.tags.append(tag.get("node").get("text"))
        genres_row = (
            response_data.get("data")
            .get("title")
            .get("genres")
            .get("genres")
        )
        for genre in genres_row:
            self.genres.append(genre.get("text"))

    async def get_data(self) -> None:
        await self._get_url()
        title_id = re.split(r"/", self.url)[-2]
        await self._get_from_graphql(title_id)
        response = await self.client.session.get(self.url)
        if response.status != 200:
            self.session_close()
            raise RequestException(
                f"request code in get_data: {response.status}"
                f"URL: {self.url}"
            )
        soup = BeautifulSoup(await response.text(), "lxml")
        poster = soup.find(
            "div",
            class_=(
                "ipc-media ipc-media--poster-27x40 ipc-image-media-ratio"
                "--poster-27x40 ipc-media--baseAlt ipc-media--poster-l "
                "ipc-poster__poster-image ipc-media__img",
            )
        ).img.get("srcset")
        poster = poster.split(" ")
        self.poster = poster[-2]
        self.title = soup.find("div", class_="sc-b5e8e7ce-1 kNhUtn").h1.text
        self.date = soup.find("span", class_="sc-8c396aa2-2 jwaBvf").text
        self.duration = (
            soup.find("span", class_="sc-8c396aa2-2 jwaBvf")
            .parent.find_next_siblings()[-1]
            .text
        )
        self.rating = soup.find("span", class_="sc-7ab21ed2-1 eUYAaq").text

    def storyline_format(self) -> None:
        self.storyline = re.sub(r'&quot;', '"', self.storyline)
        self.storyline = re.sub(r'&#39;', '`', self.storyline)

    async def session_close(self):
        await self.client.session.close()


def get_genres() -> set:
    url = CATEGORIES.get("Top_250_Movie")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    result = []
    genres_row = soup.find_all("li", class_="subnav_item_main")
    for genre in genres_row:
        result.append(genre.text.strip())
    return result


async def main():
    client = Client()
    title = Title_Single(client, "Musical_Movie")
    # await title._get_url()
    # print(title.url)
    await title.get_data()
    # print(title.title)
    await title.session_close()
    # print(list(GENRES_MOVIE.keys()))

if __name__ == "__main__":
    asyncio.run(main())

import requests
from bs4 import BeautifulSoup
import random
import re
import asyncio
import aiohttp
import ssl
import certifi

HEADERS = {
    "Accept-Language": "en-US,en;q=0.5",
}

CATEGORIES = {
    "random_Top_250_Movies": "https://www.imdb.com/chart/top/",
}

IMDB_URL = "https://www.imdb.com"


class Client:
    def __init__(self) -> None:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        conn = aiohttp.TCPConnector(ssl=ssl_context)
        self.session = aiohttp.ClientSession(connector=conn, headers=HEADERS)


class Title_Single:
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

    async def get_url(self) -> None:
        url = CATEGORIES.get(self.category)
        if url is None:
            raise Exception("wrong category")
        if self.category == "random_Top_250_Movies":
            response = await self.client.session.get(url)
            soup = BeautifulSoup(await response.text(), "lxml")
            position = random.randint(0, 249)
            end_url = soup.tbody.find_all(class_="titleColumn")[
                position
            ].a.get("href")
            self.url = IMDB_URL + end_url

    async def get_from_graphql(self, title_id: str) -> None:
        url = (
            f"https://caching.graphql.imdb.com/?operationName=TMD_Storyline&"
            f"variables=%7B%22titleId%22%3A%22{title_id}%22%7D&extensions="
            f"%7B%22persistedQuery%22%3A%7B%22sha256Hash%22%3A%22cbefc9c4a2dbd"
            f"0a5583e223e5bc788946016db709a731c85251fc1b1b7a1afbe%22%2C%22"
            f"version%22%3A1%7D%7D"
        )
        response = await self.client.session.get(
            url, headers={"content-type": "application/json"}
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
        await self.get_url()
        title_id = re.split(r"/", self.url)[-2]
        await self.get_from_graphql(title_id)
        response = await self.client.session.get(self.url)
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
        self.title = soup.find("div", class_="sc-80d4314-1 fbQftq").h1.text
        self.date = soup.find("span", class_="sc-8c396aa2-2 itZqyK").text
        self.duration = (
            soup.find("span", class_="sc-8c396aa2-2 itZqyK")
            .parent.find_next_siblings()[-1]
            .text
        )
        self.rating = soup.find("span", class_="sc-7ab21ed2-1 jGRxWM").text

    def storyline_format(self) -> None:
        self.storyline = re.sub(r'&quot;', '"', self.storyline)
        self.storyline = re.sub(r'&#39;', '`', self.storyline)

    async def session_close(self):
        await self.client.session.close()


def get_genres() -> set:
    url = CATEGORIES.get("random_Top_250_Movies")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    result = []
    genres_row = soup.find_all("li", class_="subnav_item_main")
    for genre in genres_row:
        result.append(genre.text.strip())
    return result


async def main():
    client = Client()
    title = Title_Single(client, "random_Top_250_Movies")
    await title.get_url()
    print(get_genres())
    await title.get_data()
    await title.session_close()
    print(title.storyline)


if __name__ == "__main__":
    asyncio.run(main())

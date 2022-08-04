import requests
from bs4 import BeautifulSoup
import random
import re


HEADERS = {
    "Accept-Language": "en-US,en;q=0.5",
}

CATEGORIES = {
    'random_Top_250_Movies': 'https://www.imdb.com/chart/top/',
}

IMDB_URL = 'https://www.imdb.com'


# class Title():

#     def __init__(self,):
#         self.poster = ''
#         self.title = ''
#         self.genres = []
#         self.date = ''
#         self.duration = ''
#         self.rating = ''
#         self.storyline = ''
#         self.tags = []


FORM = {
    'poster': '',
    'title': '',
    'genres': [],
    'date': '',
    'duration': '',
    'rating': '',
    'storyline': '',
    'tags': [],
}


def get_genres() -> set:
    response = requests.get(CATEGORIES['random_Top_250_Movies'], headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    result = set()
    genres_row = soup.find_all('li', class_='subnav_item_main')
    for genre in genres_row:
        result.add(genre.text.strip())
    return result


def get_storyline_and_tags(title_id: str) -> str:
    url = f'https://caching.graphql.imdb.com/?operationName=TMD_Storyline&variables=%7B%22titleId%22%3A%22{title_id}%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22sha256Hash%22%3A%22cbefc9c4a2dbd0a5583e223e5bc788946016db709a731c85251fc1b1b7a1afbe%22%2C%22version%22%3A1%7D%7D'
    response = requests.get(url, headers={'content-type': 'application/json'}).json()
    storyline = response.get('data').get('title').get('summaries').get('edges')[0].get('node').get('plotText').get('plaidHtml')
    tags = []
    tags_row = response.get('data').get('title').get('storylineKeywords').get('edges')
    for tag in tags_row:
        tags.append(tag.get('node').get('text'))
    return storyline, tags


def get_data_for_random(url: str) -> dict:
    response = requests.get(url, headers=HEADERS)
    title_id = re.split(r'/', url)[-2]
    result = FORM
    soup = BeautifulSoup(response.text, 'lxml')
    poster = soup.find('div', class_='ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--baseAlt ipc-media--poster-l ipc-poster__poster-image ipc-media__img').img.get('srcset')
    poster = poster.split(' ')
    result['poster'] = poster[-2]
    result['title'] = soup.find('div', class_='sc-94726ce4-2 khmuXj').h1.text
    genres = soup.find('div', class_='ipc-chip-list__scroller').find_all('li', class_='ipc-inline-list__item ipc-chip__text')
    for genre in genres:
        result['genres'].append(genre.text)
    result['date'] = soup.find('span', class_='sc-8c396aa2-2 itZqyK').text
    result['duration'] = soup.find('span', class_='sc-8c396aa2-2 itZqyK').parent.find_next_siblings()[-1].text
    result['rating'] = soup.find('span', class_='sc-7ab21ed2-1 jGRxWM').text
    result['storyline'], result['tags'] = get_storyline_and_tags(title_id)
    return result


def get_url_random_from_top_250(category: str) -> str:
    response = requests.get(CATEGORIES[category], headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')
    position = random.randint(0, 249)
    end_url = soup.tbody.find_all(class_="titleColumn")[position].a.get('href')
    result = IMDB_URL + end_url
    return result


def main():
    url = get_url_random_from_top_250('random_Top_250_Movies')
    result = get_data_for_random(url)
    print(result)


if __name__ == '__main__':
    main()

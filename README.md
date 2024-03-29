# IMDb suggestion bot

## Description

This is aiogramm-based telegram bot, which scrapes IMDb and sends to your telegram necessary information about one movie from IMDb Top 250 Movies or IMDb Top 250 Movies by genre. So you can make a decision what movie to see tonight.

Scrapper last update: 08.02.2023

## Getting started

### Dependencies

* Python > 3.7
* aiogramm 2.21
* beautifulsoup4 4.11.0

### Installing

Clone repository and register a telegram bot by using BotFather.

Make your own venv:

```
python3 -m venv venv
```

Install requirements:

```
pip install -r requirements.txt
```

Create in root directory .env file and fill it with telegram bot token like this:

```
TOKEN=<your token>
```

Or you can build Docker image and start bot in container:

```
docker run .
```

### Commands

- /Top_250_Movie
- /movie_genres
- /{genre}_Movie
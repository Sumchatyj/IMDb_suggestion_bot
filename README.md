# IMDb suggestion bot

## Description

This is aiogramm-based telegram bot, which scrapes IMDb and sends to your telegram necessary information about one movie from IMDb Top 250 Movies or IMDb Top 250 Movies by genre (in progress). So you can make a decision what movie to see tonight.

## Getting started

### Dependencies

* Python > 3.7
* aiogramm

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

### Commands

- /random_Top_250_Movies

# Weather & Counter Telegram bot

## How to run

> First, ensure the `.env` file has the following entries with their respective API keys.
> - `OPENAI_API_KEY`
> - `BOT_KEY`
> - `WEATHER_KEY`


### Docker

1. Build image `docker build . -t <image_name>`
2. Run container with environment variables from `.env` file `docker run --env-file .env`

### Native

1. Ensure Python 3.12+ is installed.
2. Ensure [poetry](https://python-poetry.org/docs/#installation) is installed.
3. Run `poetry install` to install dependencies.
4. Run the project with `poetry run main`

## Questions

1. Would it be out of scope to get rid of the buttons and use function calling?
2. If the bot is in a group, should the counter be unique for each user?

## To do

- Dockerize
- Deploy (possibly GCP free tier)

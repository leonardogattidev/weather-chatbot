# Weather & Counter Telegram bot

## How to run

1. Ensure Python 3.12+ is installed.
2. Ensure [poetry](https://python-poetry.org/docs/#installation) is installed.
3. Run `poetry install` to install dependencies.
4. Populate the `OPENAI_API_KEY`, `BOT_KEY` and `WEATHER_KEY` values on an `.env` file with their respective API keys.
5. Run the project with `poetry run main`


## Questions

1. Would it be out of scope to get rid of the buttons and use function calling?
2. If the bot is in a group, should the counter be unique for each user?

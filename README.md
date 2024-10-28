# Weather & Counter Telegram bot

> [!IMPORTANT]
> Bot is deployed on GCP, it's telegram username is `@weathercounterbot`.
> Some latency may be experienced (mostly due to cold starts)

## How to run

> First, ensure the `.env` file has the following entries with their respective API keys.
>
> - `OPENAI_API_KEY`
> - `BOT_KEY`
> - `WEATHER_KEY`

### Docker

1. Build image `docker build . -t <image_name>`
2. Run container with environment variables from `.env` file `docker run --env-file .env <image_name>`

> [!NOTE]
> To use webhooks, you can set the `PORT` and `URL` environment variables, the port needs to be one of 443, 80, 88 or 8443 (only ports supported by Telegram's API), and the URL is the publicly accessible URL of the device (`http(s)://<domain_or_ip>/`)

### Native

1. Ensure Python 3.12+ is installed.
2. Ensure [poetry](https://python-poetry.org/docs/#installation) is installed.
3. Run `poetry install` to install dependencies.
4. Run the project with `poetry run main`

## Considerations

1. Would it be out of scope to get rid of the buttons and use function calling?
   Wouldn't that result in too many chat completions?
2. If the bot is in a group, should the counter be unique for each user?
3. Should the counts be persisted?
4. ~~The current implementation uses polling to get updates from Telegram's API.
   For an event based approach, it's possible to use webhooks instead,
   which would reduce unnecessary resource usage.~~
5. What's worth testing?
   - The counter is the only functionality with fixed, testable, expected behaviours,
     but it's too basic and simple (add tests for the sake of it?).
   - Testing with `python-telegram-bot` [should be possible](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Writing-Tests)

## To do

- [x] Deploy (webhook implementation is required, unless deploying on VPS)

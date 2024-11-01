import logging
import os

from openai import OpenAI
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from chatbot import handlers, weather


def run():
    if (bot_key := os.getenv("BOT_KEY")) is None:
        logging.error("No BOT_KEY environment variable provided. Terminating...")
        return

    app = ApplicationBuilder().token(bot_key).build()

    app.add_handler(CommandHandler("start", handlers.on_start))
    app.add_handler(CallbackQueryHandler(handlers.on_button))
    app.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), handlers.on_message)
    )
    app.add_error_handler(handlers.on_error)

    weather.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    port = int(os.getenv("PORT", "8443"))

    if url := os.getenv("URL"):
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            secret_token="telegram-weather-bot",
            webhook_url=url,
        )
    else:
        logging.warning(
            "No webhook 'URL' environment variable provided. Falling back to polling."
        )
        try:
            app.run_polling()
        except Exception:
            logging.error("Failed to poll Telegram's API", exc_info=True)
            logging.warning(
                "Check the validity of your BOT_KEY, otherwise, Telegram's API could be failing."
            )
            return

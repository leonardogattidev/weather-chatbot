from dotenv import load_dotenv
import os
from .weather import get_weather
from .counter import increment_count, get_count

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    filters,
    MessageHandler,
    CallbackQueryHandler,
)

import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def on_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """on `/start`, it displays buttons for both weather and counter features."""

    button_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("⛅ Check weather", callback_data="weather")],
            [InlineKeyboardButton("🔢 Show count", callback_data="count")],
        ]
    )

    assert (
        update.effective_chat is not None
    ), "expected a chat to be associated with the update"
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=chat_id, text="😁 Hi! Need anything?", reply_markup=button_markup
    )


async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reacts to button presses,
    sets an appropiate `state` depending on the pressed button,
    and displays a status message"""

    assert (
        update.effective_chat is not None
    ), "expected a chat to be associated with the update"
    chat_id = update.effective_chat.id

    query = update.callback_query
    assert query is not None, ""
    await query.answer()
    if query.data == "weather":
        await context.bot.send_message(
            chat_id=chat_id,
            text="What city are you in?",
        )
        if context.user_data is None:
            return
        context.user_data["state"] = "awaiting location"
    elif query.data == "count":
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Count is {get_count(chat_id)}",
        )


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert (
        update.effective_chat is not None
    ), "expected a chat to be associated with the update"
    chat_id = update.effective_chat.id
    increment_count(chat_id)

    if context.user_data is None or "state" not in context.user_data:
        return
    state = context.user_data["state"]

    if state == "awaiting location":
        assert update.message, "`update.message` shouldn't None"
        city_name = update.message.text
        weather_text = get_weather(city_name)
        await update.message.reply_text(weather_text)
        del context.user_data["state"]


def on_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(context.error)


def main() -> None:
    load_dotenv()
    if (bot_key := os.getenv("BOT_KEY")) is None:
        logging.error("No BOT_KEY environment variable provided. Terminating...")
        return

    app = ApplicationBuilder().token(bot_key).build()

    start_handler = CommandHandler("start", on_start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), on_message)
    button_handler = CallbackQueryHandler(on_button)

    app.add_handler(start_handler)
    app.add_handler(button_handler)
    app.add_handler(message_handler)
    app.add_error_handler(on_error)

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


if __name__ == "__main__":
    main()

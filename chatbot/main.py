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

    keyboard = [
        [InlineKeyboardButton("⛅ Check weather", callback_data="weather")],
        [InlineKeyboardButton("🔢 Show count", callback_data="count")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("😁 Hi! Need anything?", reply_markup=reply_markup)


counter = {}


async def on_button(update, context):
    """Reacts to button presses,
    sets an appropiate `state` depending on the pressed button,
    and displays a status message"""

    chat_id = update.effective_chat.id

    query = update.callback_query
    await query.answer()
    if query.data == "weather":
        await context.bot.send_message(
            chat_id=chat_id,
            text="What city are you in?",
        )
        context.user_data["state"] = "awaiting location"
    elif query.data == "count":
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Count is {get_count(chat_id)}",
        )


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    increment_count(chat_id)

    if "state" not in context.user_data:
        return
    state = context.user_data["state"]

    if state == "awaiting location":
        city_name = update.message.text
        weather_text = get_weather(city_name)
        await update.message.reply_text(weather_text)
        del context.user_data["state"]


def main() -> None:
    load_dotenv()
    bot_key = os.getenv("BOT_KEY")

    # TODO: Error handling.
    # - token could be denied/invalid
    # - could fail to connect to Telegram's API
    app = ApplicationBuilder().token(bot_key).build()

    start_handler = CommandHandler("start", on_start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), on_message)
    button_handler = CallbackQueryHandler(on_button)

    app.add_handler(start_handler)
    app.add_handler(button_handler)
    app.add_handler(message_handler)

    port = int(os.getenv("PORT", "8443"))

    if url := os.getenv("URL"):
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            secret_token="&)*(@$!#",
            webhook_url=url,
        )
    else:
        logging.warning(
            "No webhook 'URL' environment variable provided. Falling back to polling."
        )
        app.run_polling()


if __name__ == "__main__":
    main()

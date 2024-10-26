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
        [InlineKeyboardButton("🔢 Count", callback_data="count")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("😁 Hi! Need anything?", reply_markup=reply_markup)


counter = {}


async def on_button(update, context):
    """Reacts to button presses,
    sets an appropiate `state` depending on the pressed button,
    and displays a status message"""

    query = update.callback_query
    await query.answer()
    if query.data == "weather":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="What city are you in?",
        )
        context.user_data["state"] = "awaiting location"
    elif query.data == "count":
        context.user_data["state"] = "counting"
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Counting..."
        )


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "state" not in context.user_data:
        return

    state = context.user_data["state"]
    if state == "awaiting location":
        city_name = update.message.text
        weather_text = get_weather(city_name)
        await update.message.reply_text(weather_text)
    elif state == "counting":
        user_id = update.message.from_user.id
        increment_count(user_id)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Count increased to {get_count(user_id)}",
        )


def main() -> None:
    load_dotenv()

    bot_key = os.getenv("BOT_KEY")
    app = ApplicationBuilder().token(bot_key).build()

    start_handler = CommandHandler("start", on_start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), on_message)
    button_handler = CallbackQueryHandler(on_button)

    app.add_handler(start_handler)
    app.add_handler(button_handler)
    app.add_handler(message_handler)

    app.run_polling()


if __name__ == "__main__":
    main()

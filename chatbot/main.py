from dotenv import load_dotenv
import os
from .weather import get_weather

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
        [InlineKeyboardButton("🔢 Count +1", callback_data="count1")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("😁 Hi! Need anything?", reply_markup=reply_markup)


counter = {}


async def on_button(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    print(f"query.data={query.data}")
    if query.data == "weather":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="What city are you in?",
        )
        context.user_data["awaiting_location"] = True
    elif query.data == "count1":
        if user_id in counter:
            counter[user_id] += 1
        else:
            counter[user_id] = 1
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"count increased to {counter[user_id]}",
        )


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    expects_location = (
        "awaiting_location" in context.user_data
        and context.user_data["awaiting_location"]
    )
    if expects_location:
        city_name = update.message.text
        data = get_weather(city_name)
        print(data)
        await update.message.reply_text(data)
        # await update.message.reply_text(
        #     f"There's {data["weather"][0]["description"]} in {data["name"]}.\n"
        #     f"Temperature is {data["main"]["temp"]}ºC.\n"
        #     f"Wind speed is {data["wind"]["speed"]}m/s, and humidity is {data["main"]["humidity"]}%"
        # )


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

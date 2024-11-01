import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from chatbot import weather


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

    assert context.user_data is not None, "`user_data` shouldn't be None"

    query = update.callback_query
    assert query is not None
    await query.answer()
    if query.data == "weather":
        await context.bot.send_message(
            chat_id=chat_id,
            text="What city are you in?",
        )
        context.user_data["state"] = "awaiting location"
    elif query.data == "count":
        count = context.user_data.get("message_count", 0)
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Count is {count}",
        )


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert context.user_data is not None, "`user_data` shouldn't be None"
    context.user_data["message_count"] = context.user_data.get("message_count", 0) + 1

    if context.user_data is None or "state" not in context.user_data:
        return
    state = context.user_data["state"]

    if state == "awaiting location":
        assert update.message, "`update.message` shouldn't None"
        city_name = update.message.text
        assert city_name, "city_name shouldn't be None"
        weather_text = weather.get_weather(city_name)
        await update.message.reply_text(weather_text)
        del context.user_data["state"]


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.error(context.error)
    if update is not Update:
        pass

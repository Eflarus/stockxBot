import html
import json
import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from stockx_bot.templates.strings import STRINGS as s

from stockx_bot import config


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""

    logging.error("Exception while handling an update:", exc_info=context.error)

    update_str = update.to_dict() if isinstance(update, Update) else str(update)

    message = (

        f"An exception was raised while handling an update\n"

        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"

        "</pre>\n\n"

        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"

        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
    )
    # Finally, send the message
    if config.NOTIFY_ADMIN_ON_ERROR:
        await context.bot.send_message(chat_id=config.DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=s.ERROR_SORRY, parse_mode=ParseMode.HTML)

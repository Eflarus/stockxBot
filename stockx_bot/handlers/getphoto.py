import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Extract the text ID from the command
    text_id = ' '.join(context.args)

    # Assuming the text ID is the file_id of the photo
    file_id = text_id

    # Send the photo by its file_id
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=file_id)

from telegram import Update
from telegram.ext import ContextTypes

from stockx_bot import config
from stockx_bot.handlers.response import send_text_response
from stockx_bot.templates.templates import render_template


async def help_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_text_response(update, context, response=render_template("help.jinja", {"support_tg": config.SUPPORT_TG}))
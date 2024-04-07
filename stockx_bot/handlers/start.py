import logging
import uuid

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from stockx_bot.config import BASE_DIR, DEVELOPER_CHAT_ID
from stockx_bot.handlers.response import send_text_response
from stockx_bot.handlers.utills import notify_admin, save_order, check_promo
from stockx_bot.keyboards.keyboards import default_keyboard_markup, promo_reply_markup, start_keyboard_markup
from stockx_bot.models import ConversationData
from stockx_bot.templates.templates import render_template

logger = logging.getLogger(__name__)

START, PHOTO, SIZE, PROMO = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    context.user_data['conversation_data'] = ConversationData()
    data: ConversationData = context.user_data['conversation_data']
    data.order_id = str(uuid.uuid4())
    data.user_id = update.message.from_user.id
    data.username = update.message.from_user.username
    data.first_name = update.message.from_user.first_name
    data.last_name = update.message.from_user.last_name
    print(update.message.chat_id)
    await send_text_response(
        update, context,
        response=render_template("start.jinja"),
        keyboard=default_keyboard_markup
    )
    return PHOTO


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a size."""
    user = update.message.from_user
    photo_file_id = update.message.photo[-1].file_id
    caption = update.message.caption

    data: ConversationData = context.user_data['conversation_data']

    logger.info(f"Photo of {user.first_name}: {photo_file_id}, {caption}")

    if 10 > len(data.photo_file_ids) > 0:
        data.photo_file_ids.append(photo_file_id)
        if caption is not None:
            data.caption = f"{data.caption} / {caption}"
    else:
        data.photo_file_ids = [photo_file_id]
        data.caption = caption
        await send_text_response(
            update, context,
            response=render_template("order_start.jinja")
        )
    return SIZE


async def no_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a size."""
    data: ConversationData = context.user_data['conversation_data']

    user = update.message.from_user
    caption = update.message.text
    logger.info(f"Photo of {user.first_name}: {caption}")
    data.caption = caption
    await send_text_response(
        update, context,
        response=render_template("order_start.jinja"),
    )
    return SIZE


async def size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the size  and asks for promo."""
    data: ConversationData = context.user_data['conversation_data']
    data.size = update.message.text

    user = update.message.from_user

    logger.info("Size of %s: %s", user.first_name, data.size)
    await send_text_response(
        update, context,
        response=render_template("after_size.jinja"),
        keyboard=promo_reply_markup)
    return PROMO


async def no_promo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    data: ConversationData = context.user_data['conversation_data']
    data.promo = "no promo"
    user = update.callback_query.from_user
    logger.info("No Promo from %s: %s", user.first_name, update.callback_query.data)

    await update.callback_query.edit_message_reply_markup(reply_markup=None)

    await send_text_response(
        update, context,
        response=render_template("order.jinja"),
        keyboard=start_keyboard_markup)

    await save_order(context)
    await notify_admin(context)
    return ConversationHandler.END


async def promo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    data: ConversationData = context.user_data['conversation_data']

    user = update.message.from_user
    logger.info("Promo of %s: %s", user.first_name, update.message.text)
    client_promo = update.message.text.upper()
    if await check_promo(client_promo):
        data.promo = client_promo
        await send_text_response(
            update, context,
            response=render_template("order_w_promo.jinja"),
            keyboard=start_keyboard_markup)

        await save_order(context)
        await notify_admin(context)
        return ConversationHandler.END

    else:
        data.promo = "error promo"
        await send_text_response(
            update, context,
            response=render_template("no_promo.jinja"),
            keyboard=promo_reply_markup)

        return PROMO


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    context.user_data['conversation_data'] = ConversationData()
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await send_text_response(
        update, context,
        response=render_template("cancel.jinja"),
        keyboard=start_keyboard_markup)

    return ConversationHandler.END

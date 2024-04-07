from telegram import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from stockx_bot.templates.strings import STRINGS

default_keyboard = [
    [KeyboardButton(STRINGS.CALL_MNGR), KeyboardButton(STRINGS.HELP)]
]

default_keyboard_markup = ReplyKeyboardMarkup(default_keyboard, resize_keyboard=True)

start_keyboard = [
    [KeyboardButton(STRINGS.NEW_ORDER)],
    [KeyboardButton(STRINGS.CALL_MNGR), KeyboardButton(STRINGS.HELP)]
]

start_keyboard_markup = ReplyKeyboardMarkup(start_keyboard, resize_keyboard=True)

promo_keyboard = [
    [InlineKeyboardButton(STRINGS.AVAILABLE_PROMOS, url="https://t.me/modeservice/7")],
    [InlineKeyboardButton(STRINGS.NO_PROMO, callback_data="no_promo")]
]

promo_reply_markup = InlineKeyboardMarkup(promo_keyboard)

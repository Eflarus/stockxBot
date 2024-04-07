from telegram import InputMediaPhoto
from telegram.ext import ContextTypes

from stockx_bot.config import BASE_DIR, GOOGLE_SPREADSHEET_ID, ADMIN_IDS
from stockx_bot.models import ConversationData

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from stockx_bot.templates.templates import render_template

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name(f"{BASE_DIR}/client_secret.json", scope)
client = gspread.authorize(creds)
# Open the Google Spreadsheet by its name
sheetOrders = client.open_by_key(GOOGLE_SPREADSHEET_ID).get_worksheet(0)
sheetPromos = client.open_by_key(GOOGLE_SPREADSHEET_ID).get_worksheet(1)


async def notify_admin(context: ContextTypes.DEFAULT_TYPE):
    data: ConversationData = context.user_data['conversation_data']
    if len(data.photo_file_ids) == 1:
        for admin_id in ADMIN_IDS:
            await context.bot.send_photo(chat_id=admin_id,
                                         photo=data.photo_file_ids[0],
                                         caption=render_template("notify_new_order.jinja", data=data.to_dict())
                                         )
    elif len(data.photo_file_ids) > 1:
        media_group = []
        for photo_file_id in data.photo_file_ids:
            media_group.append(InputMediaPhoto(media=photo_file_id))
        for admin_id in ADMIN_IDS:
            await context.bot.send_media_group(chat_id=admin_id,
                                               media=media_group,
                                               caption=render_template("notify_new_order.jinja", data=data.to_dict())
                                               )
    else:
        for admin_id in ADMIN_IDS:
            await context.bot.send_message(chat_id=admin_id,
                                           text=render_template("notify_new_order.jinja", data=data.to_dict())
                                           )


async def check_promo(client_promo: str):
    active_promos = sheetPromos.col_values(1)
    return client_promo.upper() in active_promos


async def save_order(context: ContextTypes.DEFAULT_TYPE):
    data: ConversationData = context.user_data['conversation_data']
    sheetOrders.append_row(
        [data.order_id, data.user_id,
         "https://t.me/" + data.username,
         data.first_name, data.last_name,
         str(data.photo_file_ids),
         data.caption,
         data.size,
         data.promo,
         data.created_at.strftime('%d.%m.%Y %H:%M:%S')
         ]
    )

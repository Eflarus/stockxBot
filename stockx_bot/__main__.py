import logging
import pytz
from telegram.constants import ParseMode
from telegram.ext import (
    CommandHandler,
    ApplicationBuilder, Defaults, MessageHandler, filters, ConversationHandler, CallbackQueryHandler,
)

from stockx_bot.handlers import no_photo, photo, no_promo, cancel, get_photo
from stockx_bot.handlers import error_handler, start, promo, size, help_, call_manager
import stockx_bot.config as config
from stockx_bot import handlers
from stockx_bot.db import close_db
from stockx_bot.handlers.start import PHOTO, SIZE, PROMO
from stockx_bot.templates.strings import STRINGS

COMMAND_HANDLERS = {
    "start": handlers.start,
    "help": handlers.help_,
    "error": handlers.error_handler
}

# Enable logging
logging.basicConfig(
    filename=config.LOG_FILE_NAME,
    filemode='a',
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)


def main() -> None:
    """Run the bot."""
    defaults = Defaults(parse_mode=ParseMode.HTML, tzinfo=pytz.timezone('Europe/Moscow'))
    application = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).defaults(defaults).build()

    default_filters = (filters.TEXT &
                       ~filters.COMMAND &
                       ~filters.Regex(f"^({STRINGS.HELP})$") &
                       ~filters.Regex(f"^({STRINGS.CALL_MNGR})$"))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start),
                      MessageHandler(filters.Regex(f"^({STRINGS.NEW_ORDER})$"), start)],
        states={
            PHOTO: [MessageHandler(filters.PHOTO, photo),
                    MessageHandler(default_filters, no_photo)],
            SIZE: [
                MessageHandler(default_filters, size),
                MessageHandler(filters.PHOTO, photo)
            ],
            PROMO: [MessageHandler(default_filters, promo),
                    CallbackQueryHandler(no_promo, pattern="no_promo")],
        },
        fallbacks=[CommandHandler("cancel", cancel),
                   CommandHandler("start", start),
                   MessageHandler(filters.Regex(f"^({STRINGS.HELP})$"), help_),
                   MessageHandler(filters.Regex(f"^({STRINGS.CALL_MNGR})$"), call_manager)],
    )


    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(help_, pattern="help"))
    application.add_handler(MessageHandler(filters.Regex(f"^({STRINGS.HELP})$"), help_))
    application.add_handler(MessageHandler(filters.Regex(f"^({STRINGS.CALL_MNGR})$"), call_manager))
    application.add_handler(CommandHandler('get', get_photo))

    application.add_error_handler(error_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback

        logger.warning(traceback.format_exc())
    finally:
        close_db()

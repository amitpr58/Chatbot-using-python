from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from helpers.handles import facts_to_str
from helpers.utils import (
    start,
    echo,
    add_name,
    add_email,
    add_mobile,
    InputOuestion,
    hello,
    myinfo,
    done,
    end_convo,
)

from key.token import API_KEY

import logging
from typing import Dict

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
Name, Email, Contact, Question = range(4)


bot = ApplicationBuilder().token(API_KEY).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start) , MessageHandler(filters.Regex("(?i)^(hi|hello|hi sir|Hi|Hello|hlo|Hlo|.|..|HI)$"), echo)],
    states={
        Name: [
            MessageHandler(
                filters.TEXT,
                add_name,
            ),
        ],
        Email: [
            MessageHandler(
                filters.TEXT,
                add_email,
            ),
        ],
        Contact: [
            MessageHandler(
                filters.TEXT,
                add_mobile,
            ),
        ],
        Question:[
            MessageHandler(
                filters.TEXT,
                InputOuestion,
            ),
        ]
    },
    fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
)

bot.add_handler(CommandHandler("hello", hello))
bot.add_handler(CommandHandler("myinfo", myinfo))
bot.add_handler(CommandHandler("end", end_convo))
bot.add_handler(conv_handler)

if __name__ == "__main__" : bot.run_polling()
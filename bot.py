from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from src.token import API_KEY, MADEBY

import logging
from typing import Dict


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ["Name", "Branch"],
    ["Email Id", "Contact Number"],
    ["Done"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Simple Hello function"""
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")


async def myinfo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Your Information"""
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text(
        f"Your Information - : {facts_to_str(user_data)}",
        reply_markup=ReplyKeyboardRemove(),
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start Function"""
    await update.message.reply_text(
        f"Hey! {update.effective_user.first_name}! I am GCET support Bot build by - {MADEBY}"
    )
    await update.message.reply_text("I have to ask some question", reply_markup=markup)
    return CHOOSING


async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(
        f"Your {text.lower()}? Yes, I would love to hear about that!"
    )

    return TYPING_REPLY


async def received_information(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    await update.message.reply_text(
        "You can tell me more.",
        reply_markup=markup,
    )

    return CHOOSING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text(
        f"Your Information - : {facts_to_str(user_data)}",
        reply_markup=ReplyKeyboardRemove(),
    )


async def end_convo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Conversation Ended"""
    await update.message.reply_text(
        "Session Ended",
    )
    user_data = context.user_data
    user_data.clear()
    return ConversationHandler.END


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


bot = ApplicationBuilder().token(API_KEY).build()

bot.add_handler(CommandHandler("hello", hello))
bot.add_handler(CommandHandler("myinfo", myinfo))
bot.add_handler(CommandHandler("end", end_convo))

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        CHOOSING: [
            MessageHandler(
                filters.Regex("^(Name|Branch|Name|Branch|Email Id|Contact Number)$"),
                regular_choice,
            ),
            # MessageHandler(filters.Regex("^Something else...$"), custom_choice),
        ],
        TYPING_CHOICE: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                regular_choice,
            )
        ],
        TYPING_REPLY: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                received_information,
            ),
        ],
    },
    fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
)

bot.add_handler(conv_handler)
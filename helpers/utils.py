from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from .handles import facts_to_str

Name, Email, Contact  = range(3)

async def add_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["Name"] = update.message.text
    await update.message.reply_text(
        "Please Enter your E-mail Id",
    )
    return Email

async def add_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["Email"] = update.message.text
    await update.message.reply_text(
        "Enter your Contact Number",
    )
    return Contact

async def add_mobile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["Contact"] = update.message.text
    print(context.user_data)
    return ConversationHandler.END

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Simple Hello function"""
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")
    await update.message.reply_text("What is your full name?")

    return Name

async def myinfo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Your Information"""
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text(
        f"Your Information - : {facts_to_str(user_data)}",
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start Function"""
    await update.message.reply_text(
        f"Hey! {update.effective_user.first_name}! I am GCET support Bot build by - Ved Gupta"
    )
    await update.message.reply_text("Welcome,\nI well connected you to live agent to help with adocking station. \nDon't share any type of Bank detail")
    await update.message.reply_text("What is your name?")

    return Name

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

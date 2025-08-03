import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from ai import get_response
from prompts import summarizer_prompt, tweet_prompt
from search import search_topic
from session import get_session, clear_session

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧠 AI", callback_data="AI"),
         InlineKeyboardButton("💻 Tech", callback_data="Technology")],
        [InlineKeyboardButton("⚽ Sports", callback_data="Sports"),
         InlineKeyboardButton("💰 Finance", callback_data="Finance")],
        [InlineKeyboardButton("🪙 Crypto", callback_data="Crypto Currency"),
         InlineKeyboardButton("🏛️ Architecture", callback_data="Architecture")],
        [InlineKeyboardButton("🎬 Movies", callback_data="Movies"),
         InlineKeyboardButton("📺 TV Series", callback_data="TV Series")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📢 Choose a news category:", reply_markup=reply_markup)

# User taps category
async def handle_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data
    user_id = query.from_user.id
    session = get_session(user_id)

    await query.edit_message_text(f"🔍 Fetching trending news for **{category}**...")

    news_content = search_topic(category)
    if not news_content:
        await query.message.reply_text("❌ No news found. Try again later.")
        clear_session(user_id)
        return

    session["topic"] = category
    session["summary"] = get_response(summarizer_prompt(news_content))
    session["draft"] = get_response(tweet_prompt(session["summary"]))

    await query.message.reply_text(
        f"✍️ Draft Tweet based on recent {category} news:\n\n{session['draft']}\n\nSend feedback or type 'done'."
    )

# Feedback or "done"
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()
    session = get_session(user_id)

    if not session.get("topic"):
        await update.message.reply_text("Please start by selecting a category using /start.")
        return

    if text.lower() == "done":
        await update.message.reply_text(f"✅ Final Tweet:\n\n{session['draft']}")
        clear_session(user_id)
    else:
        revision_prompt = f"Rewrite the following tweet based on this feedback:\n\nTweet:\n{session['draft']}\n\nFeedback:\n{text}"
        session["draft"] = get_response(revision_prompt)
        await update.message.reply_text(f"🔁 Revised Tweet:\n\n{session['draft']}\n\nSend more feedback or type 'done'.")

def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_category))  # ✅ REGISTERED HERE
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    run_bot()

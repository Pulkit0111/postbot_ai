import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from session import get_session, clear_session
from search import search_topic
from ai import get_response
from prompts import summarizer_prompt, tweet_prompt

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to TweetGen Bot!\nSend a topic to generate your first tweet.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()
    session = get_session(user_id)

    if not session["topic"]:
        session["topic"] = text
        await update.message.reply_text("🔎 Searching and summarizing the topic... Please wait.")
        research = search_topic(text)
        if not research:
            await update.message.reply_text("❌ Couldn't find research. Try a different topic.")
            clear_session(user_id)
            return
        session["summary"] = get_response(summarizer_prompt(research))
        session["draft"] = get_response(tweet_prompt(session["summary"]))
        await update.message.reply_text(f"✍️ Draft Tweet:\n\n{session['draft']}\n\nSend feedback or type 'done' to finalize.")
    else:
        if text.lower() == "done":
            await update.message.reply_text(f"✅ Final Tweet:\n\n{session['draft']}")
            clear_session(user_id)
        else:
            prompt = f"Rewrite the following tweet based on this feedback:\n\nTweet:\n{session['draft']}\n\nFeedback:\n{text}"
            session["draft"] = get_response(prompt)
            await update.message.reply_text(f"🔁 Revised Tweet:\n\n{session['draft']}\n\nSend more feedback or type 'done'.")

def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    run_bot()

import os
import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Load ideas from CSV
ideas = pd.read_csv("ideas.csv")["idea"].dropna().tolist()
INDEX_FILE = "current_index.txt"
subscribers = set()

def get_current_index():
    if not os.path.exists(INDEX_FILE):
        return 0
    with open(INDEX_FILE, "r") as f:
        return int(f.read().strip())

def save_current_index(index):
    with open(INDEX_FILE, "w") as f:
        f.write(str(index))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    subscribers.add(chat_id)
    await context.bot.send_message(chat_id=chat_id, text="Привет! Я буду присылать тебе идеи по питанию каждый день 😊")

async def send_daily_idea(app):
    index = get_current_index()
    if index >= len(ideas):
        return
    idea = ideas[index]
    for chat_id in subscribers:
        await app.bot.send_message(chat_id=chat_id, text="🍏 Идея дня:
{idea}")
    save_current_index(index + 1)

async def main():
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_idea, "cron", hour=9, args=[app])
    scheduler.start()

    print("Бот запущен...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

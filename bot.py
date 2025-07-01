import pandas as pd
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import os
# Загрузка идей
ideas = pd.read_csv("ideas.csv")["idea"].tolist()
# Файл для хранения текущего индекса
INDEX_FILE = "current_index.txt"
def get_current_index():
    if not os.path.exists(INDEX_FILE):
        return 0
    with open(INDEX_FILE, "r") as f:
        return int(f.read().strip())
def save_current_index(index):
    with open(INDEX_FILE, "w") as f:
        f.write(str(index))
# Telegram токен
TOKEN = "YOUR_BOT_TOKEN"
bot = Bot(token=TOKEN)
# Список пользователей
subscribers = set()
def start(update, context):
    chat_id = update.effective_chat.id
    subscribers.add(chat_id)
    context.bot.send_message(chat_id=chat_id, text="Привет! Я буду присылать тебе идеи по питанию каждый день 😊")
def send_daily_idea():
    index = get_current_index()
    if index >= len(ideas):
        return  # Все идеи закончились
    idea = ideas[index]
    for chat_id in subscribers:
        bot.send_message(chat_id=chat_id, text=f"🍏 Идея дня:\n{idea}")
    save_current_index(index + 1)
# Настройка планировщика
scheduler = BackgroundScheduler()
scheduler.add_job(send_daily_idea, 'cron', hour=9)  # каждый день в 9:00
scheduler.start()
# Запуск бота
updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
print("Бот запущен...")
updater.start_polling()
updater.idle()
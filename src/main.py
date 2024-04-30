import telebot
from src.config import TOKEN_FOR_DANCE_BOT
from src.utils import create_start_markup

bot = telebot.TeleBot(TOKEN_FOR_DANCE_BOT)


# Обработчик команды start
@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = create_start_markup()
    bot.send_message(message.chat.id, "Привет! Подскажи мне, кто ты?", reply_markup=markup)


# Запуск бота
bot.polling()

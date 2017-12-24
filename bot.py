import config
import pyowm
import telebot
import funcs
import sqlite3

bot = telebot.TeleBot(config.token)
owm = pyowm.OWM(config.appid)

markup = telebot.types.ReplyKeyboardMarkup(True, False)
markup.row('/help')

text_help = 'The bot gets the weather using openweathermap.org. You can write "CityName" or "CityName, Country(2 letters)" for getting current weather.'
text_help2 = 'You can change settings of the forecast using /set with 3 of this parameteres: temeperature, humidity, wind for e.g.: /set temperture wind humidity'


@bot.message_handler(commands=['start'])
def start(message):
    photo = open('D:\PythonProjects\weatherforecast_bot\e123.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)
    bot.send_message(message.chat.id, '''
    Welcome to weatherf_bot! The bot sends you the weather in the city you wrote. If wou want to get more information type /help. And have fun!
    ''', reply_markup=markup)
    conn = sqlite3.connect('bd.sqlite')
    c = conn.cursor()
    t = message.chat.first_name + message.chat.last_name
    c.execute("REPLACE INTO bd (user_id, parameter, name) VALUES ('%s' ,'0', '%s')"%(message.chat.id, t))
    conn.commit()
    c.close()
    conn.close()


@bot.message_handler(commands=['help'])
def help_c(message):
    photo1 = open('D:\PythonProjects\weatherforecast_bot\help1.png', 'rb')
    photo2 = open('D:\PythonProjects\weatherforecast_bot\help2.png', 'rb')
    bot.send_message(message.chat.id, text_help)
    bot.send_photo(message.chat.id, photo1)
    bot.send_message(message.chat.id, text_help2)
    bot.send_photo(message.chat.id, photo2)


@bot.message_handler(commands=['set'])
def set_c(message):
    funcs.set_func(message)


@bot.message_handler(content_types=['text'])
def main_c(message):
    city = message.text
    if city == 'Moscow':
        city = 'Moscow, RU'
    funcs.send_weather(message, city)


if __name__ == '__main__':
    bot.polling(none_stop=True)

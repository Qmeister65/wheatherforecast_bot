import telebot
import config
import pyowm
import sqlite3

bot = telebot.TeleBot(config.token)
owm = pyowm.OWM(config.appid)


def set_func(message):
    conn = sqlite3.connect('bd.sqlite')
    c = conn.cursor()
    try:
        if message.text.split()[1] == 'temperature':                        # temperature = t, humidity = h, wind = w
            par = 0                                                         # t -> parameter = 0
            try:                                                            # t+w+h -> parameter = 1
                if message.text.split()[2] == 'humidity':                   # t+h -> parameter = 2
                    par = 2                                                 # t+w -> parameter = 3
                    try:                                                    # w -> parameter = 4
                        if message.text.split()[3] == 'wind':               # h -> parameter = 5
                            par = 1                                         # w+h -> parameter = 6
                    except:
                        pass
                elif message.text.split()[2] == 'wind':
                    par = 3
                    try:
                        if message.text.split()[3] == 'humidity':
                            par = 1
                    except:
                        pass
            except:
                pass
            c.execute("UPDATE bd SET parameter='%s' WHERE user_id='%s'" % (par, message.chat.id))
        elif message.text.split()[1] == 'wind':
            par = 4
            try:
                if message.text.split()[2] == 'humidity':
                    par = 6
                    try:
                        if message.text.split()[3] == 'temperature':
                            par = 1
                    except:
                        pass
                elif message.text.split()[2] == 'temperature':
                    par = 3
                    try:
                        if message.text.split()[3] == 'humidity':
                            par = 1
                    except:
                        pass
            except:
                pass
            c.execute("UPDATE bd SET parameter='%s' WHERE user_id='%s'" % (par, message.chat.id))
        elif message.text.split()[1] == 'humidity':
            par = 5
            try:
                if message.text.split()[2] == 'temperature':
                    par = 2
                    try:
                        if message.text.split()[3] == 'wind':
                            par = 1
                    except:
                        pass
                elif message.text.split()[2] == 'wind':
                    par = 6
                    try:
                        if message.text.split()[3] == 'temperature':
                            par = 1
                    except:
                        pass
            except:
                pass
            c.execute("UPDATE bd SET parameter='%s' WHERE user_id='%s'"%(par,message.chat.id))
        else:
            bot.send_message(message.chat.id, 'Wrong params of /set')
    except:
        bot.send_message(message.chat.id, 'Wrong params of /set')
    conn.commit()
    c.close()
    conn.close()


def send_weather(message, city):
    print(message.text)
    conn = sqlite3.connect('bd.sqlite')
    c = conn.cursor()
    c.execute("SELECT parameter FROM bd WHERE user_id='%s'"%(message.chat.id))
    par = str(c.fetchone()[0])
    c.close()
    conn.close()
    #city = message.text
    if par == '0':
        get_temperature(message, city)
    if par == '1':
        get_temperature(message, city)
        get_humidity(message, city)
        get_wind(message, city)
    if par == '2':
        get_temperature(message, city)
        get_humidity(message, city)
    if par == '3':
        get_temperature(message, city)
        get_wind(message, city)
    if par == '4':
        get_wind(message, city)
    if par == '5':
        get_humidity(message, city)
    if par == '6':
        get_humidity(message, city)
        get_wind(message, city)


def get_temperature(message, city):
    try:
        w = owm.weather_at_place(city).get_weather().get_temperature('celsius')
        bot.send_message(message.chat.id, "Current temperature in {}: {}".format(city, w['temp']))
    except:
        bot.send_message(message.chat.id, 'There is no such city in the database')


def get_wind(message, city):
    try:
        w = owm.weather_at_place(city).get_weather().get_wind()
        if (w['deg']>=0 and w['deg']<=22.5) or (w['deg']>=337.5 and w['deg']<=360):
            d = 'North'
        if (w['deg']>22.5 and w['deg']<67.5):
            d = 'Northeast'
        if w['deg']>=67.5 and w['deg']<=112.5:
            d = 'East'
        if w['deg']>112.5 and w['deg']<157.5:
            d = 'Southeast'
        if w['deg']>=157 and w['deg']<=202.5:
            d = 'South'
        if w['deg']>202.5 and w['deg']<247.5:
            d = 'Southwest'
        if w['deg']>= 247.5 and w['deg']<= 292.5:
            d = 'West'
        if w['deg']>292.5 and w['deg']<337.5:
            d = 'Northwest'
        bot.send_message(message.chat.id, "Current wind speed in {} is {} m/s from {}({} degrees)".format(city, w['speed'], d, w['deg']))
    except:
        bot.send_message(message.chat.id, 'There is no such city in the database')


def get_humidity(message, city):
    try:
        w = owm.weather_at_place(city).get_weather().get_humidity()
        bot.send_message(message.chat.id, "Current humidity in {} is {}%".format(city, w))
    except:
        bot.send_message(message.chat.id, 'There is no such city in the database')
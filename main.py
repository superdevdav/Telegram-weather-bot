import telebot
import requests

bot = telebot.TeleBot('6434674453:AAGFx9GyUAuEbmrBf8I1nKhRhqVBtYm1wCQ')
API = '2f9bcd486e860e9ede0d2dcaa4a7924f'


@bot.message_handler(commands=['start'])
def start(data):
    bot.send_message(data.chat.id, 'Привет, укажи название города!')


@bot.message_handler(content_types=['text'])
def text(message):
    city = message.text.strip().lower()
    data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if data.status_code == 200:
        temp = int(data.json()["main"]["temp"])
        temp_fells_like = int(data.json()["main"]["feels_like"])
        wind = int(data.json()["wind"]["speed"])
        clouds = data.json()["clouds"]["all"]
        image = 'sunny.jpg' if clouds <= 25 else 'sun and cloud.jpeg' if 25 < clouds < 75 else 'clouds.jpeg'
        file = open('./' + image, 'rb')
        bot.reply_to(message, f'Температура на данный момент {temp}°C 🌤\n'
                              f'Ощущается как {temp_fells_like}°C 🌤\n'
                              f'Ветер {wind} м/с 💨')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, 'Город указан неверно или он вымышленный :(')

bot.polling(none_stop=True)

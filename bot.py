import os
import main
import config
import telebot
import requests

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=["start"])
def hello(message):
    bot.send_message(message.chat.id, f"Привет {message.from_user.first_name} я CITVY BOT!\nЯ помогу вас сделать красивые артворки\nскиньте картинку потом текст и получите готовый картинок")

@bot.message_handler(content_types=["photo"])
def get_photo(message):
    file_id = message.photo[0].file_id
    url = f"https://api.telegram.org/bot{config.token}/getFile?file_id={file_id}"
    response = requests.get(url)
    file_path = response.json()['result']['file_path']
    url = f"https://api.telegram.org/file/bot{config.token}/{file_path}"
    response = requests.get(url)
    with open("image.jpg", "wb") as photo:
        photo.write(response.content)
    config.in_file = "image.jpg"
    config.out_file = "converted.jpg"
    bot.send_message(message.chat.id, "Хорошо! Сейчас пишите текст который будет находится на картинке")

@bot.message_handler(content_types=["text"])
def get_text(message):
    config.text = message.text
    if config.in_file and config.out_file and config.text:
        main.make_artwork(config.in_file, config.out_file, config.text)
        with open(config.out_file, "rb") as photo:
            bot.send_photo(message.chat.id, photo.read())
        os.system(f"rm {config.in_file} {config.out_file}")
        config.in_file = None
        config.out_file = None
        config.text = None

bot.polling()

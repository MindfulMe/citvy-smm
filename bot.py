import os
import main
import config
import telebot
import requests
import evaluate
from PIL import Image

bot = telebot.TeleBot(config.token)

UPLOAD_FOLDER = os.getcwd() + '\\examples\\'
DOWNLOAD_FOLDER = os.getcwd() + '\\examples\\thumbs\\'

@bot.message_handler(commands=["start"])
def hello(message):
    bot.send_message(message.chat.id, f"Hello {message.from_user.first_name} I am CITVY ART BOT from https://citvy.com!\nI will help create an art from photo and apply text over it \nsend a picture as a file and then send a text and get an art image")

@bot.message_handler(content_types=["photo"])
def get_photo(message):
    bot.send_message(message.chat.id, "Please send the picture as a file")

@bot.message_handler(content_types=["document"])
def get_photo(message):
    config.in_file = message.document.file_name
    config.out_file = f"converted_{message.document.file_name}"
    file_id = message.document.file_id
    url = f"https://api.telegram.org/bot{config.token}/getFile?file_id={file_id}"
    response = requests.get(url)
    file_path = response.json()['result']['file_path']
    url = f"https://api.telegram.org/file/bot{config.token}/{file_path}"
    response = requests.get(url)
    with open(UPLOAD_FOLDER + config.in_file, "wb") as photo:
        photo.write(response.content)
    if not config.in_file.lower().endswith(".jpg") and not config.in_file.lower().endswith(".jpeg"):
        im = Image.open(UPLOAD_FOLDER + config.in_file)
        rgb_im = im.convert('RGB')
        new_name = config.in_file.split(".")[0]
        config.in_file = f"{new_name}.jpg"
        rgb_im.save(UPLOAD_FOLDER + config.in_file)
    bot.send_message(message.chat.id, "Cool!  Now type a text that will be on the artwork picture")

@bot.message_handler(content_types=["text"])
def get_text(message):
    config.text = message.text
    if config.in_file and config.out_file and config.text:
        evaluate.ins = UPLOAD_FOLDER + config.in_file
        evaluate.outs = DOWNLOAD_FOLDER + config.out_file
        evaluate.main()
        main.make_artwork(evaluate.outs, evaluate.outs, config.text)
        with open(DOWNLOAD_FOLDER + config.out_file, "rb") as photo:
            bot.send_photo(message.chat.id, photo.read())
        # os.system(f"rm {evaluate.ins} {evaluate.outs} {DOWNLOAD_FOLDER + config.out_file, config.text}") """for UNIX systems [MacOS, Linux]"""
        config.in_file = None
        config.out_file = None
        config.text = None
        evaluate.ins = None
        evaluate.out = None

bot.polling()

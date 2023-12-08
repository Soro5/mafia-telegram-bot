# ДЗ 21.11.2023 - Создать фунцию, добавляющую нового пользователя в БД (параметры: ID, ник, роль); Добавить функцию достающую ID, никнейм и роль + роль как параметр +-
from telebot import TeleBot
from time import sleep
import db

# НАПИСАТЬ 

TOKEN = "6781637378:AAHvXAZVASaljd7ralXD0D-OiIl-jQJvfso"
bot = TeleBot(TOKEN)

is_group = lambda message: message.chat.type in ('group', 'supergroup')

# For game process
night = False

def get_killed(night):
    if not night:
        username_killed = db.citizen_kill()
        return f'Горожане выгнали {username_killed}'
    username_killed = db.mafia_kill()
    return f'Мафия убила {username_killed}'

def game_loop(message):
    global night
    bot.send_message(message.chat.id, "Приветствуем")
    sleep(120)
    while True:
        if not night:
            bot.send_message(message.chat.id, 'Город засыпает. Просыпается мафия >:)')
        else:
            bot.send_message(message.chat.id, 'Город просыпается. Просыпается город')
        night = not night
        sleep(120)

# Commands, written for users
@bot.message_handler(commands=["kick"])
def kick(message):
    username = ' '.join(message.text.split(' ')[1:])
    username = db.count_alive()
    if not night:
        if not username in username:
            bot.send_message(message.chat.id, "Такого человека в игре нет")
            return
        voted = db.vote("citizen_vote", username, message.from_user.id)
        if voted:
            bot.send_message(message.chat.id, "Ваш голос учитан")
            return
        bot.send_message(message.chat.id, "Я надеюсь, y вас нет раздвоения личности...")
        return
    bot.send_message(message.chat.id, "Вам нельзя голосовать ночью")

@bot.message_handler(func=lambda m: m.text.lower() == 'готов играть' and m.chat.type == 'private')
def send_maessage(message):
    bot.send_message(message.chat.id, f'{message.from_user.first_name} играет')
    bot.send_message(message.from_user.id, 'Добро пожаловать в Стикманград')
    db.add_player(message.from_user.id, name=message.from_user.first_name)

# Сделать смену дня и ночи 05.12.2023
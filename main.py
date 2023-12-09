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
    bot.send_message(message.chat.id, "Приветствуем в Стикманграде! у вас 1 минута, чтобы познакомиться")
    sleep(60)
    while True:
        if not night:
            bot.send_message(message.chat.id, 'Город засыпает. Просыпается мафия >:)')
        else:
            bot.send_message(message.chat.id, 'Город просыпается. Просыпается город')
        winner = db.check_winner()
        db.clear(dead=False)
        night = not night
        alive = db.count_alive()
        alive = '\n'.join(alive)
        bot.send_message(message.chat.id, f"В игре:\n{alive}")
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

# Сделать пустой репозиторий на Github, установить соединение с локальным репозиторием (Git) (tip: git remote), клонировать удаленный репозиторий (Github) на pythonanywhere 
# ВАЖНО: Доделать проект и сделать отчет в воскресенье! 
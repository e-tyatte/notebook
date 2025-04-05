from random import choice

import telebot

token = 'Вставить токен'

bot = telebot.TeleBot(token)


RANDOM_TASKS = ['Написать сказку', 'Выучить Python', 'Записаться на курс в Нетологию', 'Посмотреть хорошую комедию']

RANDOM_DATES = ['Послезавтра', '31 декабря', 'Вторник', 'Сегодня']

notebook = dict()


HELP = '''
Список доступных команд:
/start - запуск программы
/show  - напечать все задачи на заданную дату
Введите команду и желаемую дату.
/add - добавить задачу
Введите желаемую дату и новую задачу.
/random - добавить на сегодня случайную задачу
/surprise - добавить задачу "Пойти в гости" на случайную дату
/help - Напечатать справку по программе
'''


def add_note(date, task):
    date = date.lower()
    if notebook.get(date) is not None:
        notebook[date].append(task)
    else:
        notebook[date] = [task]


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['random'])
def random(message):
    task = choice(RANDOM_TASKS)
    add_note('сегодня', task)
    bot.send_message(message.chat.id, f'Задача {task} добавлена на сегодня')

    
@bot.message_handler(commands=['surprise'])
def surprise(message):
    date = choice(RANDOM_DATES)
    add_note(date, 'Пойти в гости')
    bot.send_message(message.chat.id, f'Задача "Пойти в гости" добавлена на {date}')


@bot.message_handler(commands=['add'])
def add(message):
    _, date, tail = message.text.split(maxsplit=2)
    task = ' '.join([tail])
    add_note(date, task)
    bot.send_message(message.chat.id, f'Задача {task} добавлена на дату {date}')


@bot.message_handler(commands=['show'])
def show(message):
    date = message.text.split()[1].lower()
    if date in notebook:
        tasks = ''
        for task in notebook[date]:
            tasks += f'[ ] {task}\n'
    else:
        tasks = 'Такой даты нет'
    bot.send_message(message.chat.id, tasks)


bot.polling(none_stop=True)
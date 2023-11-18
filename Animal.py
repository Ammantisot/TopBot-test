import telebot
from telebot import types
from random import choice
import requests
bot_token = '6895597903:AAHQ7mtGKiK1cKRjY7de_xdQzjCJsod2uFg'

# Создаем объект бота
bot = telebot.TeleBot(token=bot_token)

name = "Капибара"
energy = 70
satiety = 10
happiness = 100
url = 'https://uselessfacts.jsph.pl/api/v2/facts/random'

@bot.message_handler(commands=['start'])
def welkome(message):
    bot.send_message(message.chat.id, 'Привет. Я твой питомец, чтобы начать введи команду /mood')

@bot.message_handler(commands=['mood'])
def button(message):
    mm = types.ReplyKeyboardMarkup(row_width=2)
    item_1 = types.KeyboardButton('/feed')
    item_2 = types.KeyboardButton('/play')
    item_3 = types.KeyboardButton('/sleep')
    item_4 = types.KeyboardButton('/kapibara')
    item_5 = types.KeyboardButton('/motivation')
    item_6 = types.KeyboardButton('/fact')
    item_7 = types.KeyboardButton('/game')
    mm.add(item_1, item_2, item_3, item_4, item_5, item_6, item_7)
    bot.send_message(message.chat.id, 'Выбери любую команду)\nCправка по командам:\n/feed - покормить\n/play - поиграть с питомцем\n/sleep - поспать\n/kapibara - характеристики питомца\n/motivation - мотивация от питомца\n/fact - рандомные факты\n/game - игра в камень - ножницы - бумага', reply_markup=mm)


def feed():
    global satiety, energy
    satiety += 10
    energy += 5


def play():
    global satiety, happiness, energy
    satiety -= 5
    happiness += 10
    energy -= 10

def sleep():

    global satiety, happiness, energy
    satiety -= 5
    happiness -= 5
    energy = 70


def check(message):
    global satiety, happiness, energy
    if satiety <= 0:
        bot.send_message(message.chat.id, f"{name} умер от голода. Не забывайте кормить питомца!")
    elif satiety >= 10:
        bot.send_message(message.chat.id, f"{name} наелся и счастлив")

    if happiness < 0:
        bot.send_message(message.chat.id, f"{name} умер от тоски. С питомцем нужно чаще играть!")
    elif happiness > 100:
        bot.send_message(message.chat.id, f"{name} счастлив как никогда")

    if energy < 70:
        bot.send_message(message.chat.id, f"{name} умрет от истощения")
    elif energy > 70:
        bot.send_message(message.chat.id, f"{name} полон сил и энергии!")


# @bot.message_handler(content_types=['text'])

@bot.message_handler(commands=['feed'])
def feed_handler(message):
    feed()
    bot.send_message(message.chat.id, f"{name} вкусно покушал и теперь его голод сосстовляет {satiety}!")
    check(message)


@bot.message_handler(commands=['sleep'])
def sleep_handler(message):
    sleep()
    bot.send_message(message.chat.id, f"{name} поспал и стал здоровее! Теперь его здоровье состовляет {energy}!")
    check(message)


@bot.message_handler(commands=['play'])
def play_handler(message):
    play()
    bot.send_message(message.chat.id, f"{name} поиграл и теперь его счастье состовляет {happiness}!")
    check(message)

@bot.message_handler(commands=['kapibara'])
def characteristics(message):
    global energy, satiety, happiness
    bot.send_message(message.chat.id, f"Характеристики:\n Сытность - {satiety} \n Энергия - {energy} \n Счастье - {happiness}")

@bot.message_handler(commands=["motivation"])
def motivation(message):
    list = ['Успех - 1% таланта и 99% труда', "Никогда не сдавайся и увидишь, как сдаютя другие", "Неудача – это приправа, которая придает успеху особенный вкус", "Работай усердно, будь добр, и очень скоро произойдут удивительные вещи", "Чтобы начать, нужно перестать говорить и начать делать", "Самое сложное – это решение действовать, остальное – просто упорство", "Единственный способ достичь выдающегося результата и сделать большую работу – это любить то, что ты делаешь", "Возможно, вам придется сражаться в битве более одного раза, чтобы выиграть "]
    bot.send_message(message.chat.id, f'Мотивацию надо поднять! Держи мотивационную речь --- {choice(list)}')


@bot.message_handler(commands=["fact"])
def fact(message):
    bot.send_message(message.chat.id, "Я отправлю тебе факты, а их количество тебе придется ввести самому). Правда они будут на англиском, но у тебя есть преводчик, ну или можешь перевести сам и при этом набраться опыта в изучении англиского языка")
    bot.register_next_step_handler(message, print_fact)
def print_fact(message):
    global url
    count = message.text
    for i in range(int(count)):
        response = requests.get(url)
        print(response)
        data = response.json()['text']
        bot.send_message(message.chat.id, data)

@bot.message_handler(commands=["game"])
def game(message):
    bot.send_message(message.chat.id,
                     "Капибара любит играть в камень - ножницы - бумагу. Чтобы выбрать ножницы введи /scissors, "
                     "чтобы выбрать камень введи /stone, чтобы выбрать бумагу введи /paper")


@bot.message_handler(commands=["scissors"])
def scissors(message):
    if choice(["камень", "ножницы", "бумага"]) == "камень":
        bot.send_message(message.chat.id, "Вы выиграли)")
    elif choice(["камень", "ножницы", "бумага"]) == "ножницы":
        bot.send_message(message.chat.id, f"Вы проиграли", )
    elif choice(["камень", "ножницы", "бумага"]) == "бумага":
        bot.send_message(message.chat.id, "Ничья")


@bot.message_handler(commands=["stone"])
def stone(message):
    if choice(["камень", "ножницы", "бумага"]) == "камень":
        bot.send_message(message.chat.id, "Ничья")
    elif choice(["камень", "ножницы", "бумага"]) == "ножницы":
        bot.send_message(message.chat.id, "Вы выиграли)")
    elif choice(["камень", "ножницы", "бумага"]) == "бумага":
        bot.send_message(message.chat.id, "Вы проиграли(")


@bot.message_handler(commands=["paper"])
def paper(message):
    if choice(["камень", "ножницы", "бумага"]) == "ножницы":
        bot.send_message(message.chat.id, "Вы проиграли(")
    elif choice(["камень", "ножницы", "бумага"]) == "бумага":
        bot.send_message(message.chat.id, "Ничья")
    elif choice(["камень", "ножницы", "бумага"]) == "камень":
        bot.send_message(message.chat.id, "Вы выиграли)")


@bot.message_handler(content_types=["text"])
def nn(message):
    bot.send_message(message.chat.id, "Ты ввел неправильное сообщение, посмотри на команды")


bot.polling(none_stop=True)

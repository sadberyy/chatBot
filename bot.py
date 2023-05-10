import telebot
bot = telebot.TeleBot('5833160364:AAFSP7I_522xMw9HRjNGZcYRIqWDmNMkPCs')

class Do:
    def __init__(self, service, login=None, password=None):
        self.service = service
        self.login = login
        self.password = password

users = {}

def get_user(chat_id):
    if chat_id not in users:
        users[chat_id] = {}
    return users[chat_id]

def set_data(chat_id, service, login, password):
    user = get_user(chat_id)
    site = Do(service, login, password)
    user[service] = site
    return 'Логин и пароль сохранены!'

def del_data(chat_id, service):
    user = get_user(chat_id)
    del user[service]
    return f'Логин и пароль для сайта {service} удалены!'

def get_data(chat_id, service):
    user = get_user(chat_id)
    site = user[service]
    return f'Логин: {site.login}\nПароль: {site.password}'

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Я могу сохранять для Вас логины и пароли для различных сервисов, введите /help чтобы узнать мои возможности')

@bot.message_handler(commands=['help'])
def help_message(message):
    cmmnds = "\n".join([
        "Действия бота:",
        "/start - Старт диалога",
        "/help - Список возможностей бота",
        "/set - Сохранить логин и пароль",
        "/del - Удалить логин и пароль",
        "/get - Показать логин и пароль",
    ])
    bot.send_message(message.chat.id, cmmnds)

@bot.message_handler(commands=['set'])
def set_message(message):
    bot.send_message(message.chat.id, "Введите сервис для сохранения логина и пароля:")
    bot.register_next_step_handler(message, set_login)

def set_login(message):
    service = message.text
    bot.send_message(message.chat.id, f'Введите логин для <u>{service}</u>:', parse_mode='html')
    bot.register_next_step_handler(message, set_password, service)

def set_password(message, service):
    login = message.text
    bot.send_message(message.chat.id, f'Введите пароль для <u>{service}</u>:', parse_mode='html')
    bot.register_next_step_handler(message, set_helper, service, login)

def set_helper(message, service, login):
    password = message.text
    bot.send_message(message.chat.id, set_data(message.chat.id, service, login, password))

@bot.message_handler(commands=['del'])
def del_message(message):
    bot.send_message(message.chat.id, "Введите сервис:")
    bot.register_next_step_handler(message, del_help)

def dele_help(message):
    service = message.text
    bot.send_message(message.chat.id, del_data(message.chat.id, service))

@bot.message_handler(commands=['get'])
def get_message(message):
    bot.send_message(message.chat.id, "Введите сервис:")
    bot.register_next_step_handler(message, get_help)

def get_help(message):
    service = message.text
    bot.send_message(message.chat.id, get_data(message.chat.id, service))

bot.polling(none_stop=True)
from .. import *


def get_profile_files(name):
    loader = Instaloader()
    try:
        loader.download_profile(name)
    finally:
        result = dict()
        file_list = list()
        for root, dirs, files in os.walk(name):
            for file in files:
                if str(file).endswith('.jpg'):
                    file_list.append(file)
        result['file_list'] = file_list
        result['dir'] = name
        return result


def get_zip(files_info, chat_id):
    newzip = zipfile.ZipFile(path.join(files_info["dir"], f'{chat_id}.zip'), 'w')
    for file in files_info['file_list']:
        newzip.write(path.join(files_info['dir'], file))
    newzip.close()
    return newzip.filename


class Bot:

    def __init__(self, token):
        logging.basicConfig(level=logging.INFO, filename="../log.log", filemode="w")
        self.token = token
        self.bot = telebot.TeleBot(self.token)
        self.file_and_chat = {}

        @self.bot.message_handler(commands=['start'], content_types=['text'])
        def get_user_comand(message):
            out_message = f'<b>Привет! Я могу выгрузить весь медиаконтент из профиля Инстаграм.</b>'
            markup_inline = telebot.types.InlineKeyboardMarkup()
            item_profile = telebot.types.InlineKeyboardButton(text='Получить контент профиля', callback_data='profile')
            item_tag = telebot.types.InlineKeyboardButton(text='Получить контент по тегу', callback_data='tag')

            markup_inline.add(item_profile, item_tag)
            self.bot.send_message(message.chat.id, out_message, parse_mode='html', reply_markup=markup_inline)

        @self.bot.callback_query_handler(func=lambda call: True)
        def answer(call):
            if call.data == 'profile':
                out_message = f'<b>Введите имя профиля</b>'
            elif call.data == 'tag':
                out_message = f'<b>Функция находится в разработке и пока не доступна(((</b>'
            elif call.data == 'zip':
                zip_name = get_zip(self.file_and_chat[call.message.chat.id], call.message.chat.id)
                self.bot.send_document(call.message.chat.id,
                                       telebot.types.InputFile(open(zip_name, 'rb')))
            elif call.data == 'photo':
                file_list = self.file_and_chat[call.message.chat.id]['file_list']
                dir_name = self.file_and_chat[call.message.chat.id]['dir']
                for photo in file_list:
                    self.bot.send_photo(call.message.chat.id,
                                        telebot.types.InputFile(open(path.join(dir_name, photo), 'rb')))
                return 0

            self.bot.send_message(call.message.chat.id, out_message, parse_mode='html')

        @self.bot.message_handler(content_types=['text'])
        def get_user_comand(message):
            name = message.text
            self.file_and_chat[message.chat.id] = get_profile_files(name)
            out_message = f'<b>Выберите способ загрузки.</b>'

            markup_inline = telebot.types.InlineKeyboardMarkup()
            zip_method = telebot.types.InlineKeyboardButton(text='Архивом', callback_data='zip')
            photo_method = telebot.types.InlineKeyboardButton(text='Фото сюда', callback_data='photo')

            markup_inline.add(zip_method, photo_method)
            self.bot.send_message(message.chat.id, out_message, parse_mode='html', reply_markup=markup_inline)

        self.bot.polling(none_stop=True)


mybot = Bot(TOKEN)

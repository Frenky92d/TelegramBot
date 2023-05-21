from VoiceBot import *


TOKEN = 'token'


class TelBotVoice:

    def __init__(self, token):
        logging.basicConfig(level=logging.INFO, filename="../log.log", filemode="w")
        self.token = token
        self.bot = telebot.TeleBot(self.token)
        self.file_and_chat = {}

        @self.bot.message_handler(content_types=['audio'])
        def get_audio_file(message):
            out_message = f'<b>Что добавить в описание?</b>'
            file_info = self.bot.get_file(message.audio.file_id)
            self.file_and_chat[message.chat.id] = self.bot.download_file(file_info.file_path)
            if not message.caption:
                self.bot.send_message(message.chat.id, out_message, parse_mode='html')
            else:
                self.bot.send_voice(message.chat.id,
                                    voice=self.file_and_chat[message.chat.id],
                                    caption=message.caption)
            logging.info(f'{datetime.now()}\t'
                         f'chat ID: {message.chat.id}\t'
                         f'method: get_audio_file\t'
                         f'text:{message.text if message.text else message.caption}')

        @self.bot.message_handler(content_types=['text'])
        def get_text_file(message):
            if self.file_and_chat.get(message.chat.id):
                self.bot.send_voice(message.chat.id,
                                    voice=self.file_and_chat[message.chat.id],
                                    caption=message.text)
                logging.info(f'{datetime.now()}\t'
                             f'chat ID: {message.chat.id}\t'
                             f'method: get_text_file\t'
                             f'text:{message.text}')
            else:
                out_message = f'<b>Не отправлен аудио файл или пустое описание!</b>'
                self.bot.send_message(message.chat.id, out_message, parse_mode='html')
                logging.info(f'{datetime.now()}\t'
                             f'chat ID: {message.chat.id}\t'
                             f'method: get_text_file\t'
                             f'Error:{"Send text before audio"}')

        self.bot.polling(none_stop=True)


mybot = TelBotVoice(TOKEN)

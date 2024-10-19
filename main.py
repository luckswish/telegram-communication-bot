import os
import requests
import logging
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_log.log"),
        logging.StreamHandler()
    ]
)

# Входные данные
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_CHAT_ID'))

# Словари для хранения состояний пользователей
user_message_map = {}
forward_to_admin = {}  # Отслеживает, пересылать ли сообщения админу для каждого пользователя

def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=data)
    return response.json()

def get_updates(offset=None):
    url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
    params = {'offset': offset}
    response = requests.get(url, params=params)
    return response.json()

def log_user_message(chat_id, text):
    # Логирование сообщения, отправленного пользователем боту (только если не пересылается админу)
    if not forward_to_admin.get(chat_id, False):
        logging.info(f"Пользователь {chat_id} отправил боту сообщение: {text}")

def log_user_to_admin(chat_id, text):
    # Логирование пересылки сообщения админу
    logging.info(f"Пользователь {chat_id} отправил администратору сообщение: {text}")

def log_admin_reply(user_chat_id, text):
    # Логирование ответа администратора пользователю
    logging.info(f"Администратор отправил пользователю {user_chat_id} сообщение: {text}")

def main():
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates['result']:
            message = update.get('message')
            if message:
                chat_id = message['chat']['id']
                username = message['chat']['username']

                # Проверяем, что сообщение содержит текст
                if 'text' in message:
                    text = message['text']
                    if text == '/start':
                        send_message(chat_id, f"Привет, {username}! Введите /admin, чтобы начать пересылку ваших сообщений админу, или /back, чтобы прекратить пересылку.")
                        forward_to_admin[chat_id] = False  # По умолчанию пересылка отключена
                        log_user_message(chat_id, text)
                    elif text == '/admin':
                        forward_to_admin[chat_id] = True
                        send_message(chat_id, "Теперь ваши сообщения будут пересылаться админу.")
                        log_user_message(chat_id, text)
                    elif text == '/back':
                        forward_to_admin[chat_id] = False
                        send_message(chat_id, "Ваши сообщения больше не пересылаются админу.")
                        log_user_message(chat_id, text)
                    else:
                        # Логируем сообщение пользователя боту, только если оно не пересылается админу
                        log_user_message(chat_id, text)

                        # Если сообщение от администратора (ответ пользователю)
                        if chat_id == ADMIN_ID and message.get('reply_to_message'):
                            original_message_text = message['reply_to_message']['text']
                            user_chat_id = user_message_map.get(original_message_text)

                            if user_chat_id:
                                # Отправляем ответ пользователю
                                send_message(user_chat_id, f"Ответ от администратора: {text}")
                                # Логируем отправку сообщения от администратора
                                log_admin_reply(user_chat_id, text)
                            else:
                                send_message(ADMIN_ID, "Ошибка: Не могу найти пользователя для ответа.")
                        # Если сообщение от пользователя и включена пересылка админу
                        elif chat_id != ADMIN_ID and forward_to_admin.get(chat_id, False):
                            modified_message = f'Сообщение от пользователя {username}: {text}'
                            # Отправляем сообщение администратору
                            send_message(ADMIN_ID, modified_message)
                            # Сохраняем соответствие между текстом сообщения и chat_id пользователя
                            user_message_map[modified_message] = chat_id
                            # Логируем пересылку сообщения админу
                            log_user_to_admin(chat_id, text)

                # Обновляем offset для получения следующих сообщений
                offset = update['update_id'] + 1

if __name__ == '__main__':
    main()

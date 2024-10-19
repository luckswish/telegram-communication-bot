# Telegram Communication Bot

## Описание
Этот бот предназначен для общения между пользователями и администратором. Пользователь может отправить сообщение боту, и оно будет переслано администратору. Ответы администратора будут отправлены пользователю. Бот поддерживает команды `/start`, `/admin` и `/back` для управления тем, пересылаются ли сообщения администратору.

## Функциональность
- **/start**: Бот приветствует пользователя и сообщает, что его сообщения могут быть пересланы администратору при активации.
- **/admin**: Активирует режим пересылки сообщений администратору.
- **/back**: Деактивирует режим пересылки сообщений, и пользователь может отправлять сообщения боту без пересылки администратору.
- Администратор может отвечать на сообщения пользователей, и бот отправит ответ пользователю.

## Требования
- Python 3.7+
- Библиотеки Python:
  - `requests`
  - `python-dotenv`
  - `logging`

## Настройка переменных окружения.
Создайте файл .env в корне проекта и добавьте следующие переменные:

- BOT_TOKEN=your_bot_token
- ADMIN_CHAT_ID=your_admin_chat_id
- ADMIN_USERNAME=your_admin_username

- BOT_TOKEN: токен вашего Telegram-бота.
- ADMIN_CHAT_ID: ID администратора (можно получить с помощью бота UserInfoBot).
- ADMIN_USERNAME: username администратора Telegram.

## Логирование
Бот ведет логирование с помощью библиотеки logging. Логи содержат три типа сообщений:

- Пользователь отправил сообщение боту.
- Пользователь отправил сообщение администратору.
- Администратор отправил сообщение пользователю.

Пример логов:
- 2024-10-19 23:00:09,523 - INFO - Пользователь 3124231 отправил боту сообщение: Привет
- 2024-10-19 23:00:09,777 - INFO - Пользователь 3124231 отправил администратору сообщение: Привет
- 2024-10-19 23:00:19,715 - INFO - Администратор отправил пользователю 3124231 сообщение: Привет, чем могу помочь?

#!/usr/bin/python3
# -*- coding: utf-8 -*-
import telebot
from telebot.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
    
from database import DataBase as DB
import config
    
    
bot = telebot.TeleBot(config.TOKEN)

# Главное меню
menu = ReplyKeyboardMarkup(resize_keyboard = True)
info = KeyboardButton("🔐Профиль")
money = KeyboardButton('💳Баланс💸')
rab = KeyboardButton('⚒️Зарабатывать🛠️')
ref = KeyboardButton('📊Реферальная система')
rules = KeyboardButton('📖Правила')
menu.add(rules).add(rab, info).add(money, ref)

# Баланс
b = InlineKeyboardMarkup(row_width = 1)
out = InlineKeyboardButton("💰Вывести деньги", callback_data = 'out')
b.add(out)

# Назад
back = InlineKeyboardMarkup(row_width = 1)
exit = InlineKeyboardButton("Назад", callback_data = 'exit')
back.add(exit)

# Реферальная система
referal = InlineKeyboardMarkup(row_width = 1)
refe = InlineKeyboardButton("💰Вывести деньги", callback_data = 'out')
referal.add(refe)

# Кнопки администратора
verifi = InlineKeyboardMarkup(row_width = 1)
ver = InlineKeyboardButton("Одобрить", callback_data = 'y')
unver = InlineKeyboardButton("Отклонить", callback_data = 'n')
verifi.add(ver, unver)

compleet = InlineKeyboardMarkup(row_width = 1)
com = InlineKeyboardButton("Готово", callback_data = 'com')
compleet.add(com)

# Кнопки модератора
moderator = InlineKeyboardMarkup(row_width = 1)
yes = InlineKeyboardButton("Подтвердить", callback_data = 'yes')
no = InlineKeyboardButton("Отклонить", callback_data = 'no')
moderator.add(yes, no)

@bot.message_handler(commands = ['start', 'help'])
def start(message):
	try:
		db = DB()
		db.AddUser(message.chat.id)
		reff = extract_unique_code(message.text)
		for r in db.getAll():
			print(r, reff)
			if reff == r and message.chat.id != reff:
				db.setRef(reff, db.getRef(r) + 1)
				bot.send_message(r, f'📊По вашей ссылке присоеденился реферал! У вас {db.getRef(r)} рефералов.')
		bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! \n Рад приветсвовать тебя. Я бот, который поможет тебе  зарабатывать выполняя простые задания.', reply_markup  = menu)
	except Exception as e:
		pass
	
	
def extract_unique_code(text):
	try:
	    # Extracts the unique_code from the sent /start command.
		return text.split()[1] if len(text.split()) > 1 else None
	except Exception as e:
		pass
	

# Обработчик клавиатуры
@bot.callback_query_handler(func=lambda c:True)
def keyboard(c):
	try:
		db = DB()
		config.outb = 1
		if c.data == 'exit':
			bot.delete_message(c.message.chat.id, c.message.id)
			bot.delete_message(c.message.chat.id, c.message.id-1)
			bot.register_next_step_handler(c.message, messages)
		if c.data == 'out':
			config.outb=0
			if db.getRef(c.message.chat.id) >= 3:
				bot.send_message(c.message.chat.id, f'💵Минимальная сумма вывода 100 руб. \n Пришлите сумму вывода💰, номер карты💳 и банк куда вывести деньги. \n  Ваш баланс: {db.getBalance(c.message.chat.id)}.', reply_markup = back)
				bot.register_next_step_handler(c.message, cash)
			else:
				bot.send_message(c.message.chat.id, 'Чтобы вывести деньги вам необходимо пригласить миинимум трех человеек в бота. Внимание они должны зайти по вашей реферальной ссылке. Чтобы получить вашу реферальную ссылку нажмите на кнопку Реферальная система.', reply_markup=menu)
			
		if c.data == 'y':
			bot.delete_message(c.message.chat.id, c.message.message_id)
			id = c.message.caption.rsplit('= ', 2)[1]
			sum = c.message.caption.rsplit('id = ', 2)[0]
			db.money(id, -int(sum))
			bot.send_message(id, f'💸Деньги зачислены на счет, ваш баланс: {db.getBalance(id)}')
		if c.data == 'n':
			bot.delete_message(c.message.chat.id, c.message.message_id)
			id = c.message.caption.rsplit('= ', 2)[1]
			bot.send_message(id, 'Заявка на пополнение счета отклонена.')
		if c.data == 'com':
			try:
				id = int(c.message.text.rsplit('= ', 2)[1])
				db.money(id, int(config.text))
				bot.delete_message(c.message.chat.id, c.message.message_id)
				bot.send_message(id, f'💰Деньги списаны со счета и переведены на указаную карту, ваш баланс: {db.getBalance(id)}')
			except:
				id = int(c.message.text.rsplit('= ', 2)[1])
				db.money(id, float(config.text))
				bot.delete_message(c.message.chat.id, c.message.message_id)
				bot.send_message(id, f'💰Деньги списаны со счета и переведены на указаную карту, ваш баланс: {db.getBalance(id)}')
	
		if c.data == 'next':
			db.setNum(message.from_user.id, 1)
			moderTask(c.message)
			
		if c.data == 'yes':
			text = c.message.caption
			id = int(text.rsplit('id = ', 2)[1])
			t = text.rsplit('id = ', 2)[0]
			t = t[ 9 : -2]
			cost = {
				t == 'подписки':0.4,
				t == 'лайки': 0.2,
				t  == 'просмотры': '0,4',
				t == 'комментарии': 1,
				t == 'отзывы': 5
				}[True]
			bot.delete_message(message_id=c.message.id, chat_id=c.message.chat.id)
			db.money(id, -cost)
		if c.data == 'no':
			text = c.message.caption
			id = int(text.rsplit('id = ', 2)[1])
			t = text.rsplit('id = ', 2)[0]
			t = t[ 9 : -2]
			cost = {
				t == 'подписки':0.5,
				t == 'лайки': 0.5,
				t  == 'просмотры': 0.4,
				t == 'комментарии': 1,
				t == 'отзывы': 5
				}[True]
			db.money(id, cost)
			
	except Exception as e:
		print(e, 156)


@bot.message_handler(content_types=['text'])
def messages(message):
	try:
		config.uid = message.message_id
		db = DB()
		if message.chat.id == config.admin:
			config.text = message.text
		config.id = message.chat.id
		if message.text == '🔐Профиль':
			bot.send_message(message.chat.id, f'📋Имя: {message.from_user.first_name} \n 💳Баланс: {db.getBalance(message.chat.id)} \n 📊Рефералы: {db.getRef(message.chat.id)} \n 📑Количество выплненых заданий: {db.getNum(message.chat.id)}')
		
		if message.text == '💳Баланс💸':
			balance = db.getBalance(message.chat.id)
			bot.send_message(message.chat.id, f'💰Ваш баланс: {balance} pyб.', reply_markup = b)
			db.setAns(message.chat.id, 0)
			
		if message.text == '📊Реферальная система':
			bot.send_message(message.chat.id, 'Вот ваша персональная ссылка для приглашения рефералов. Приглаcите не менее 3 человек чтобы можно было выводить деньги. \n https://t.me/mnogodeneg_bot?start=' + str(message.from_user.id))
			
		if message.text == '📖Правила':
			bot.send_message(message.chat.id, f"""Информация:

  Ваш ID: {message.chat.id}
  Ссылка для приглашения : https://t.me/mnogodeneg_bot?start={message.from_user.id}

⛔️ Исполнителям запрещено:
• Иметь более одного аккаунта.
• Использовать ПО для автоматизации действий в боте.
• Отписываться от канала раннее 7ми дней с момента подписки(штраф 1 рубль).
• Пополнять баланс для заказа минимальной выплаты.
• Брать заказ на действие и не выполнять его.
• Сдавать скриншот или фото не соответствующее описанию к заданию или не свой скриншот.
• Иметь нечеловекоподобные логин или имя на аккаунте.
• За флуд в сапорт - БАН!

💵 Выплаты:
• Выплаты осуществляются в течение суток с момента заказа в рабочие дни.
• Выплаты производятся на кошельки Yandex и Qiwi

Admin: @Basadeneg""")
			
		if message.text == '⚒️Зарабатывать🛠️':
			moderTask(message)
	except Exception as e:
		pass

def chek(message):
	try:
		db = DB()
		photo = message.photo[0].file_id
		caption = message.caption
		db.setCash(message.chat.id, caption)
		bot.send_photo(config.admin, photo, caption + 'id = ' + str(message.chat.id), reply_markup=verifi)
	except Exception as e:
		pass
		

def cash(message):
	bot.register_next_step_handler(message, messages)
	try:
		db = DB()
		id = message.chat.id
		if db.getBalance(message.chat.id) > 99:
			bot.send_message(config.admin, 'Не забудте указать сумму списания перед тем как нажать кнопку!!! Вот данные от пользователя: ' + message.text + '\n' + 'Текущий баланс пользователя: ' + str(db.getBalance(message.chat.id)) + '\n id = ' + str(id), reply_markup=compleet)
			bot.send_message(id, 'Ваша заявка отправлена! Ожидайте.')	
		
	except Exception as e:
		print(e, 204)
			
			
def moderTask(message):
	try:
		db = DB()
		try:
			num = db.getNum(message.chat.id)
			task = db.getWork(num)
			comment = db.getComment(num)
			link = db.getLink(num)[num]
			t = task
			db.moneyTask(num, -1)
			#print(link)
			
			taskText = {
					task == 'подписки': f'📩 Задание: \n\n 1️⃣ Подписаться на канал. \n 2️⃣Прислать скриншот.\n3️⃣ Не отписываться от канала 7 дней. \n Цена за задание: 0.4 руб. \n Комментарий заказчика: {comment}.',
					task == 'лайки': f'📩 Задание: \n\n 1️⃣ Поставить лайк \n 2️⃣Прислать скриншот.\n Цена за задание: 0.2 руб. \n Комментарий заказчика: {comment}.',
					task == 'просмотры': f'📩 Задание: \n\n 1️⃣ Просмотр видео/поста. \n 2️⃣Прислать скриншот.\n Цена за задание: 0.4 руб. \n Комментарий заказчика: {comment}.',
					task == 'комментарии': f'📩 Задание: \n\n 1️⃣ Написать комментарий. \n 2️⃣Прислать скриншот.\n Цена за задание: 1.0 руб. \n Комментарий заказчика: {comment}.',
					}[True]
					
			cost = {
				t == 'подписки': 0.5,
				t == 'лайки': 0.5,
				t  == 'просмотры': 0.4,
				t == 'комментарии': 1
				}[True]
					
			db.setTask(message.chat.id, task)
			
			# Зарабатывать
			work = InlineKeyboardMarkup(row_width = 1)
			link = InlineKeyboardButton(f"Выполнить задание {cost} pyб.", url=link)
			next = InlineKeyboardButton("Пропустить задание", callback_data = 'next')
			work.add(link, next)
			
			db.setNum(message.from_user.id, 1)		
			bot.send_message(message.chat.id, taskText, reply_markup=work)
			bot.register_next_step_handler(message, moderka)
		except Exception as e:
			print(e, 'moderTask')
			bot.send_message(message.chat.id, 'Пока что заданий нет. Зайдите позже.')
	except Exception as e:
		pass
	
	
def moderka(message):
	try:
		db = DB()
		task = db.getTask(message.chat.id)
		print(task)
		photo = message.photo[0].file_id
		text = f'задание: {task}' + '\n id = ' + str(message.chat.id)
		bot.send_photo(config.moderator, photo, text, reply_markup=moderator)
		moderTask(message)
	except Exception as e:
		print(e)
		
	
bot.polling()
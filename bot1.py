#!/usr/bin/python3
# -*- coding: utf-8 -*-
import telebot
from telebot.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
    
from database import DataBase as DB
import config
    
    
bot = telebot.TeleBot(config.TOCEN)

# Главное меню
menu = ReplyKeyboardMarkup(resize_keyboard = True)
money = KeyboardButton('💳Баланс💸')
order = KeyboardButton('💹Сделать заказ💼')
menu.add(money, order)

# Баланс
b = InlineKeyboardMarkup(row_width = 1)
put = InlineKeyboardButton("💸Пополнить баланс", callback_data = 'put')
b.add(put)

# Назад
back = InlineKeyboardMarkup(row_width = 1)
exit = InlineKeyboardButton("Назад", callback_data = 'exit')
back.add(exit)

# Заказчикам
oder = InlineKeyboardMarkup(row_width = 1)
putb = InlineKeyboardButton("💸Пополнить баланс", callback_data = 'put')
like = InlineKeyboardButton("👍Лайки 1 руб", callback_data = 'like')
sub = InlineKeyboardButton("🌍Подписки 2 руб", callback_data = 'sub')
watch = InlineKeyboardButton("📺Просмотры 2 руб", callback_data = 'watch')
comment = InlineKeyboardButton("📃Комментарии 5 руб", callback_data = 'comment')
feedback = InlineKeyboardButton("📨Отзывы 5 руб", callback_data = 'feed')
oder.add(putb, like, sub, watch, comment, feedback)

# Кнопки администратора
verifi = InlineKeyboardMarkup(row_width = 1)
ver = InlineKeyboardButton("Одобрить", callback_data = 'y')
unver = InlineKeyboardButton("Отклонить", callback_data = 'n')
verifi.add(ver, unver)

compleet = InlineKeyboardMarkup(row_width = 1)
com = InlineKeyboardButton("Готово", callback_data = 'com')
compleet.add(com)


@bot.message_handler(commands = ['start', 'help'])
def start(message):
	try:
		db = DB()
		db.AddUser(message.chat.id)
		bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! \n Рад приветсвовать тебя. Я бот, который поможет тебе накрутить подписки, лайки, комментарии, отзывы и просмотры.', reply_markup  = menu)
	except Exception as e:
		pass
	

# Обработчик клавиатуры
@bot.callback_query_handler(func=lambda c:True)
def keyboard(c):
	try:
		db = DB()
		if c.data == 'exit':
			bot.delete_message(c.message.chat.id, c.message.id)
			bot.register_next_step_handler(c.message, messages)
		if c.data == 'put':
			oplata = InlineKeyboardMarkup(row_width=1)
			link = InlineKeyboardButton('Оплатить', url=f'https://qiwi.com/payment/form/99?amountFraction=0&currency=RUB&extra%5B%27account%27%5D=+79626025949&extra%5B%27comment%27%5D={c.message.chat.id}&blocked[0]=account&blocked[1]=comment')
			back = InlineKeyboardButton('Назад', callback_data='exit')
			oplata.add(link, back)
			bot.send_message(c.message.chat.id, 'Для того чтобы 💸пополнить 💳баланс нажмите на кнопку(вы перейдете на страницу оплаты), переведите нужную сумму, затем пришлите сюда скриншот чека c подписью в виде цифры какую сумму вы перевели.', reply_markup = oplata)
			bot.register_next_step_handler(c.message, chek)
			
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
		if c.data == 'like' or c.data == 'sub' or c.data == 'watch' or c.data == 'comment' or c.data == 'feed':
			task = {
				c.data == 'like': 'лайки',
				c.data == 'sub': "подписки",
				c.data == 'watch': "просмотры",
				c.data == 'comment': "комментарии"
				}[True]
			db.setTask(c.message.chat.id, task)
			bot.send_message(c.message.chat.id, 'Хорошо! Теперь пришлите ссылку на пост, видео или на страничку в соц сети/ютубе.')
			bot.register_next_step_handler(c.message, setLink)
			
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
			bot.send_message(message.chat.id, f'📋Имя: {message.from_user.first_name} \n 💳Баланс: {db.getBalance(message.chat.id)} \n Рефералы: {db.getRef(message.chat.id)} \n 📑Количество выплненых заданий: {db.getNum(message.chat.id)}')
		
		if message.text == '💳Баланс💸':
			balance = db.getBalance(message.chat.id)
			bot.send_message(message.chat.id, f'💰Ваш баланс: {balance} pyб. Вы можете пополнить или вывести деньги. ', reply_markup = b)
			db.setAns(message.chat.id, 0)
			
		if message.text == '💹Сделать заказ💼':
			db.setOder(message.chat.id)
			bot.send_message(message.chat.id, f'Что вы хотите накрутить? Цены указаны за один лайк/коммент и тд. Сначала пополните баланс до необходимой суммы. Ваш баланс: {db.getBalance(message.from_user.id)}', reply_markup=oder)

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
		bot.register_next_step_handler(message, messages)
		

def setLink(message):
	try:
		db = DB()
		url = message.text
		db.setUrl(message.chat.id, url)
		t = db.getTask(message.chat.id)
		cost = {
				t == 'подписки': 2,
				t == 'лайки': 1,
				t  == 'просмотры': 2,
				t == 'комментарии': 5,
				t == 'отзывы': 5
				}[True]
		bot.send_message(message.chat.id, f'Отлично! Остался один шаг. Один {t} стоит {cost} рубля. Пополните баланс до необходимой суммы и пришлите сколько вам необходимо {t}. С вашего счета спишется нужня сумма.')
		bot.register_next_step_handler(message, OrderBegin)
	except Exception as e:
		pass

		
def OrderBegin(message):
	try:
		db = DB()
		try:
			t = db.getTask(message.chat.id)
			cost = {
				t == 'подписки': 2,
				t == 'лайки': 1,
				t  == 'просмотры': 2,
				t == 'комментарии': 5,
				t == 'отзывы': 5
				}[True]
			sum = int(message.text) * cost
			b = db.getBalance(message.chat.id)
			if b >= sum:
				db.setMoney(message.chat.id, sum/2)
				db.money(message.chat.id, sum)
				bot.send_message(message.chat.id, 'Спасибо заказ. Он будет выполнен в течении нескольких дней. Оставте комментрий для исполнителей.')
				bot.register_next_step_handler(message, setCom)
			else:
				bot.send_message(message.chat.id, 'На вашем счете недостаточно средств для совершения данной покупки.')
		except Exception as e:
			print(e)
			bot.send_message(message.chat.id, 'Пожалуйста введите только число без других символов.')
			bot.register_next_step_handler(message, OrderBegin)
	except Exception as e:
		pass
			
			

def setCom(message):
	try:
		db = DB()
		db.setComment(message.chat.id, message.text)
	except:
		pass
		
	
bot.polling()
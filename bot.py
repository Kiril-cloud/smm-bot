import telebot
import datetime
from telebot.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
    
from database import DataBase as DB
import config
    
    
bot = telebot.TeleBot(config.TOKEN)

# Главное меню
menu = ReplyKeyboardMarkup(resize_keyboard = True)
info = KeyboardButton("Как пользоваться ботом?")
money = KeyboardButton('Баланс')
order = KeyboardButton('Заказчикам')
rab = KeyboardButton('Зарабатывать')
ref = KeyboardButton('Реферальная система')
moder = KeyboardButton('Тех. поддержка')
menu.add(info).add(money, ref).add(rab, order).add(moder)

# Баланс
cash = InlineKeyboardMarkup(row_width = 1)
outcash = InlineKeyboardButton("Вывести деньги", callback_data = 'cash')
cash.add(outcash)

b = InlineKeyboardMarkup(row_width = 1)
put = InlineKeyboardButton("Пополнить баланс", callback_data = 'put')
out = InlineKeyboardButton("Вывести деньги", callback_data = 'out')
b.add(put, out)

# Заказчикам
oder = InlineKeyboardMarkup(row_width = 1)
like = InlineKeyboardButton("Лайки", callback_data = 'like')
sub = InlineKeyboardButton("Подписки", callback_data = 'sub')
watch = InlineKeyboardButton("Просмотры", callback_data = 'watch')
comment = InlineKeyboardButton("Комментарии", callback_data = 'comment')
feedback = InlineKeyboardButton("Отзывы", callback_data = 'feed')
oder.add(like, sub, watch, comment, feedback)

# Реферальная система
referal = InlineKeyboardMarkup(row_width = 1)
refe = InlineKeyboardButton("Вывести деньги", callback_data = 'out')
referal.add(refe)

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
	db = DB()
	db.AddUser(message.chat.id)
	reff = extract_unique_code(message.text)
	for r in db.getAll():
		if reff == r and db.getRef(message.chat.id) == 0 and db.getRef(reff) == 0:
			db.setRef(message.chat.id)
			db.money(message.chat.id, -10)
			db.money(r, -10)
			bot.send_message(r, f'По вашей ссылке присоеденился реферал! Вам начислено 10 рублей. Ваш баланс: {db.getBalance(r)}')
			bot.send_message(message.chat.id, f'Вы присоеденились по реферальной ссылке! Вам начислено 10 рублей. Ваш баланс: {db.getBalance(r)}')
	bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! \n Рад приветсвовать тебя. Я бот, который поможет тебе накрутить подписки, лайки, комментарии, отзывы и просмотры. Здесь также можно зарабатывать выполняя простые задания.', reply_markup  = menu)
	
	
def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None
	

# Обработчик клавиатуры
@bot.callback_query_handler(func=lambda c:True)
def keyboard(c):
	db = DB()
	if c.data == 'put':
		bot.send_message(c.message.chat.id, 'Для того чтобы пополнить баланс переведите деньги на карту: \n 4242 4242 4242 4242 \n затем пришлите сюда скриншот чека c подписью в виде цифры какую сумму вы перевели.')
	if c.data == 'out':
		bot.send_message(c.message.chat.id, f'Пришлите сумму вывода, номер карты и банк куда вывести деньги. Ваш баланс: {db.getBalance(c.message.chat.id)}. Затем нажмите на кнопку.', reply_markup=cash)
	if c.data == 'cash':
		id = c.message.chat.id
		if db.getBalance(c.message.chat.id) > 0:
			bot.send_message(-1001296667801, 'Не забудте указать сумму списания перед тем как нажать кнопку!!! Вот данные от пользователя: ' + config.text + '\n' + 'Текущий баланс пользователя: ' + str(db.getBalance(c.message.chat.id)) + '\n id = ' + str(id), reply_markup=compleet)
			bot.send_message(id, 'Ваша заявка отправлена! Ожидайте.')
		else:
			bot.send_message(c.message.chat.id, "У вас недостаточно средств для вывода денег.")
	if c.data == 'y':
		bot.delete_message(c.message.chat.id, c.message.message_id)
		id = c.message.caption.rsplit('= ', 2)[1]
		db.updateBalance(id)
		bot.send_message(id, f'Деньги зачислены на счет, ваш баланс: {db.getBalance(id)}')
	if c.data == 'n':
		bot.delete_message(c.message.chat.id, c.message.message_id)
		id = c.message.caption.rsplit('= ', 2)[1]
		bot.send_message(id, 'Заявка на пополнение счета отклонена.')
	if c.data == 'com':
		id = int(c.message.text.rsplit('= ', 2)[1])
		db.money(id, int(config.text))
		bot.delete_message(c.message.chat.id, c.message.message_id)
		bot.send_message(id, f'Деньги списаны со счета и переведены на указаную карту, ваш баланс: {db.getBalance(id)}')
		

@bot.message_handler(content_types=['text'])
def messages(message):
	db = DB()
	config.text = message.text
	config.id = message.chat.id
	if message.text == 'Как пользоваться ботом?':
		bot.send_message(message.chat.id, 'Вот небольшая презентация об этом боте.')
	
	if message.text == 'Баланс':
		balance = db.getBalance(message.chat.id)
		bot.send_message(message.chat.id, f'Ваш баланс: {balance}. Вы можете пополнить или вывести деньги. ', reply_markup = b)
		db.setAns(message.chat.id, 0)
		
	if message.text == 'Реферальная система':
		bot.send_message(message.chat.id, 'Вот ваша персональная ссылка для приглашения рефералов. Приглаcите друга и получите 10руб на баланс, тому кто зайдет по вашей ссылке также будет зачислено 10руб. \n https://t.me/SMM_Square_Bot?start=' + str(message.from_user.id))
		

@bot.message_handler(content_types=['photo'])		
def chek(message):
	db = DB()
	photo = message.photo[0].file_id
	caption = message.caption
	ans = db.getAns(message.chat.id)
	if ans == 0:
		db.setCash(message.chat.id, caption)
		bot.send_photo(-1001296667801, photo, caption + 'id = ' + str(message.chat.id), reply_markup=verifi)
	
bot.polling()
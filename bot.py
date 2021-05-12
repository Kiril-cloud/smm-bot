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
order = KeyboardButton('💹Заказчикам💼')
rab = KeyboardButton('⚒️Зарабатывать🛠️')
ref = KeyboardButton('Реферальная система')
moder = KeyboardButton('Тех. поддержка')
menu.add(info).add(money, ref).add(rab, order).add(moder)

# Баланс
b = InlineKeyboardMarkup(row_width = 1)
put = InlineKeyboardButton("💸Пополнить баланс", callback_data = 'put')
out = InlineKeyboardButton("💰Вывести деньги", callback_data = 'out')
b.add(put, out)

# Заказчикам
oder = InlineKeyboardMarkup(row_width = 1)
putb = InlineKeyboardButton("💸Пополнить баланс", callback_data = 'put')
like = InlineKeyboardButton("👍Лайки 1 руб", callback_data = 'like')
sub = InlineKeyboardButton("🌍Подписки 2 руб", callback_data = 'sub')
watch = InlineKeyboardButton("📺Просмотры 2 руб", callback_data = 'watch')
comment = InlineKeyboardButton("📃Комментарии 5 руб", callback_data = 'comment')
feedback = InlineKeyboardButton("📨Отзывы 5 руб", callback_data = 'feed')
oder.add(putb, like, sub, watch, comment, feedback)

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
	db = DB()
	db.AddUser(message.chat.id)
	reff = extract_unique_code(message.text)
	for r in db.getAll():
		if reff == r and message.chat.id != reff:
			db.setRef(r, db.getRef(r) + 1)
			bot.send_message(r, f'📊По вашей ссылке присоеденился реферал! У вас {db.getBalance(r)} рефералов.')
	bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! \n Рад приветсвовать тебя. Я бот, который поможет тебе накрутить подписки, лайки, комментарии, отзывы и просмотры. Здесь также можно зарабатывать выполняя простые задания.', reply_markup  = menu)
	
	
def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None
	

# Обработчик клавиатуры
@bot.callback_query_handler(func=lambda c:True)
def keyboard(c):
	db = DB()
	if c.data == 'put':
		bot.send_message(c.message.chat.id, 'Для того чтобы 💸пополнить 💳баланс переведите деньги на карту: \n 4242 4242 4242 4242 \n затем пришлите сюда скриншот чека c подписью в виде цифры какую сумму вы перевели.')
		bot.register_next_step_handler(c.message, chek)
	if c.data == 'out':
		if db.getRef(c.message.chat.id) >= 3:
			bot.send_message(c.message.chat.id, f'Пришлите сумму вывода💰, номер карты💳 и банк куда вывести деньги. Ваш баланс: {db.getBalance(c.message.chat.id)}. Затем нажмите на кнопку.')
			bot.register_next_step_handler(c.message, cash)
		else:
			bot.send_message(c.message.chat.id, 'Чтобы вывести деньги вам необходимо пригласить миинимум трех человеек в бота. Внимание они должны зайти по вашей реферальной ссылке. Чтобы получить вашу реферальную ссылку нажмите на кнопку Реферальная система.', reply_markup=menu)
		
	if c.data == 'y':
		bot.delete_message(c.message.chat.id, c.message.message_id)
		id = c.message.caption.rsplit('= ', 2)[1]
		db.updateBalance(id)
		bot.send_message(id, f'💸Деньги зачислены на счет, ваш баланс: {db.getBalance(id)}')
	if c.data == 'n':
		bot.delete_message(c.message.chat.id, c.message.message_id)
		id = c.message.caption.rsplit('= ', 2)[1]
		bot.send_message(id, 'Заявка на пополнение счета отклонена.')
	if c.data == 'com':
		id = int(c.message.text.rsplit('= ', 2)[1])
		db.money(id, int(config.text))
		bot.delete_message(c.message.chat.id, c.message.message_id)
		bot.send_message(id, f'💰Деньги списаны со счета и переведены на указаную карту, ваш баланс: {db.getBalance(id)}')
		
	if c.data == 'like' or c.data == 'sub' or c.data == 'watch' or c.data == 'comment' or c.data == 'feed':
		task = {
			c.data == 'like': 'лайки',
			c.data == 'sub': "подписки",
			c.data == 'watch': "просмотры",
			c.data == 'comment': "комментарии",
			c.data == 'feed': "отзывы"
			}[True]
		db.setTask(c.message.chat.id, task)
		bot.send_message(c.message.chat.id, 'Хорошо! Теперь пришлите ссылку на пост, видео или на страничку в соц сети/ютубе.')
		bot.register_next_step_handler(c.message, setLink)

	if c.data == 'next':
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
		db.money(id, -cost)
	if c.data == 'no':
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
		db.money(id, cost)


@bot.message_handler(content_types=['text'])
def messages(message):
	config.uid = message.message_id
	db = DB()
	if message.chat.id == config.admin:
		config.text = message.text
	config.id = message.chat.id
	if message.text == 'Профиль':
		bot.send_message(message.chat.id, f'📋Имя: {message.from_user.first_name} \n 💳Баланс: {db.getBalance(message.chat.id)} \n Рефералы: {db.getRef(message.chat.id)} \n 📑Количество выплненых заданий: {db.getNum(message.chat.id)}')
	
	if message.text == 'Баланс':
		balance = db.getBalance(message.chat.id)
		bot.send_message(message.chat.id, f'💰Ваш баланс: {balance} pyб. Вы можете пополнить или вывести деньги. ', reply_markup = b)
		db.setAns(message.chat.id, 0)
		
	if message.text == 'Реферальная система':
		bot.send_message(message.chat.id, 'Вот ваша персональная ссылка для приглашения рефералов. Приглаcите не менее 3 человек чтобы можно было выводить деньги. \n https://t.me/Rusmm_bot?start=' + str(message.from_user.id))
		
	if message.text == 'Заказчикам':
		db.setOder(message.chat.id)
		bot.send_message(message.chat.id, 'Хотите сделать заказ? Что именно вы хотите накрутить? Цены указаны за 1 шт. Сначала пополните баланс до необходимово вам.', reply_markup=oder)
		
	if message.text == 'Зарабатывать':
		moderTask(message)
		

def chek(message):
	db = DB()
	photo = message.photo[0].file_id
	caption = message.caption
	ans = db.getAns(message.chat.id)
	if ans == 0:
		db.setCash(message.chat.id, caption)
		bot.send_photo(config.admin, photo, caption + 'id = ' + str(message.chat.id), reply_markup=verifi)
		

def setLink(message):
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

		
def OrderBegin(message):
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
		
	
def cash(message):
		db = DB()
		id = message.chat.id
		if db.getBalance(message.chat.id) > 99:
			bot.send_message(config.admin, 'Не забудте указать сумму списания перед тем как нажать кнопку!!! Вот данные от пользователя: ' + message.text + '\n' + 'Текущий баланс пользователя: ' + str(db.getBalance(message.chat.id)) + '\n id = ' + str(id), reply_markup=compleet)
			bot.send_message(id, 'Ваша заявка отправлена! Ожидайте.')
		else:
			bot.send_message(message.chat.id, "У вас недостаточно средств для вывода денег. Минимальная сумма вывода: 100р")
			
			
def moderTask(message):
	db = DB()
	try:
		num = db.getNum(message.chat.id)
		task = db.getWork(num)
		comment = db.getComment(num)
		link = db.getLink(num)[num]
		t = task
		db.moneyTask(num, 1)
		#print(link)
		
		taskText = {
				task == 'подписки': f'Задача: \n подписаться и не отписываться. \n Комментарий заказчика: {comment}. \n После выполнения задания пришлите скриншот и мы перейдем к следующему.',
				task == 'лайки': f'Задача: \n Поставить лайк. \n Комментарий заказчика: {comment}. \n После выполнения задания пришлите скриншот и мы перейдем к следующему.',
				task == 'просмотры': f'Задача: \n просмотреть видео/пост. \n Комментарий заказчика: {comment}. \n После выполнения задания пришлите скриншот и мы перейдем к следующему.',
				task == 'комментарии': f'Задача: \n написать комментарий. \n Комментарий заказчика: {comment}. \n После выполнения задания пришлите скриншот и мы перейдем к следующему.',
				task == 'отзывы': f'Задача: \n оставить отзыв. \n Комментарий заказчика: {comment}. \n После выполнения задания пришлите скриншот и мы перейдем к следующему.'
				}[True]
				
		cost = {
			t == 'подписки': 0.4,
			t == 'лайки': 0.2,
			t  == 'просмотры': 0.4,
			t == 'комментарии': 1,
			t == 'отзывы': 5
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
	
	
def moderka(message):
		db = DB()
		task = db.getTask(message.chat.id)
		photo = message.photo[0].file_id
		text = f'задание: {task}' + '\n id = ' + str(message.chat.id)
		bot.send_photo(config.moderator, photo, text, reply_markup=moderator)
		

def setCom(message):
		db = DB()
		db.setComment(message.chat.id, message.text)
		
	
bot.polling()
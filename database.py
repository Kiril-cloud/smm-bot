#pylint:disable=W0703
#pylint:disable=W0622
#pylint:disable=W1309
import sqlite3

class DataBase():
	text = ''
	def __init__(self):
		self.db = sqlite3.connect("users.db")
		self.sql = self.db.cursor()
		try:
			self.sql.execute("""CREATE TABLE users
                                  (id, refid, ans, money, cash, tasks)
                               """)
		except Exception as e:
			print(e, 13)
            
		try:
			self.sql.execute("""CREATE TABLE oder
                                  (id, url, task, money)
                               """)
		except Exception as e:
			print(e, 20)

	def AddUser(self, userID):
		self.sql.execute(f""" SELECT id FROM users WHERE id = {userID} """)
		if self.sql.fetchone() is None:
			# self.sql.execute("SELECT id FROM users")
			self.sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (userID, 0, 0, 0, 0, 0))
		self.db.commit()
        
	def getBalance(self, id):
		self.sql.execute(f""" SELECT money FROM users WHERE id == {id} """)
		b = self.sql.fetchone()
		b = str(b)
		b = b.replace('(', '')
		b = b.replace(',', '')
		b = b.replace(')', '')
		b = int(b)
		return b
		
	def setCash(self, idAns, cash):
		try:
			self.sql.execute(f'SELECT cash FROM users WHERE id = {idAns} ')
			self.sql.execute(f' UPDATE users SET cash = {cash} WHERE id = {idAns} ')
		except Exception as e:
			print(e, 45)
		self.db.commit()
		
	def setAns(self, id, ans):
		try:
			self.sql.execute(f'SELECT ans FROM users WHERE id = {id}')
			self.sql.execute(f'UPDATE users SET ans = {ans} WHERE id = {id}')
		except Exception as e:
			print(e, 53)
			
	def getAns(self, id):
		self.sql.execute(f""" SELECT ans FROM users WHERE id = {id} """)
		b = self.sql.fetchone()
		b = str(b)
		b = b.replace('(', '')
		b = b.replace(',', '')
		b = b.replace(')', '')
		b = int(b)
		return b
		
	def updateBalance(self, id):
		self.sql.execute(f""" SELECT cash FROM users WHERE id = {id} """)
		b = self.sql.fetchone()
		b = str(b)
		b = b.replace('(', '')
		b = b.replace(',', '')
		b = b.replace(')', '')
		b = int(b)
		self.sql.execute(f'SELECT money FROM users WHERE id = {id} ')
		c = self.sql.fetchone()
		c = str(c)
		c = c.replace('(', '')
		c = c.replace(',', '')
		c = c.replace(')', '')
		c = int(c)
		b+=c
		self.sql.execute(f' UPDATE users SET money = {b} WHERE id = {id} ')
		self.db.commit()
		
	def money(self, id, sum):
		self.sql.execute(f""" SELECT money FROM users WHERE id = {id} """)
		b = self.sql.fetchone()
		b = str(b)
		b = b.replace('(', '')
		b = b.replace(',', '')
		b = b.replace(')', '')
		b = int(b)
		b-=sum
		self.sql.execute(f' UPDATE users SET money = {b} WHERE id = {id} ')
		self.db.commit()
		
	def getAll(self):
		try:
			self.sql.execute(f'SELECT id FROM users')
			AllID = self.sql.fetchall()
			ids = []
			for i in AllID:
				idd = str(i)
				a = idd.replace('(', '')
				b = a.replace(',', '')
				c = b.replace(')', '')
				ids.append(c)
				return ids
		except Exception as e:
			print(e, 111)
			return [0]
			
	def setRef(self, ref):
		try:
			self.sql.execute(f'SELECT ref FROM users WHERE id = {id}')
			self.sql.execute(f'UPDATE users SET refid = {ref} WHERE id = {id}')
		except Exception as e:
			print(e, 119)
			
	def getRef(self, id):
		self.sql.execute(f""" SELECT refid FROM users WHERE id = {id} """)
		b = self.sql.fetchone()
		b = str(b)
		b = b.replace('(', '')
		b = b.replace(',', '')
		b = b.replace(')', '')
		b = int(b)
		return b
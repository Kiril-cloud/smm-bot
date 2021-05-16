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
                                  (id, url, task, money, comment)
                               """)
		except Exception as e:
			print(e, 20)

	def AddUser(self, userID):
		try:
			self.sql.execute(f""" SELECT id FROM users WHERE id = {userID} """)
			if self.sql.fetchone() is None:
				# self.sql.execute("SELECT id FROM users")
				self.sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (userID, 0, 0, 0, 0, 0))
			self.db.commit()
		except Exception as e:
			pass
        
	def getBalance(self, id):
		try:
			self.sql.execute(f""" SELECT money FROM users WHERE id == {id} """)
			b = self.sql.fetchone()
			b = str(b)
			b = b.replace('(', '')
			b = b.replace(',', '')
			b = b.replace(')', '')
			try:
				b = int(b)
			except:
				b = float(b)
			return b
		except Exception as e:
			pass
		
	def setCash(self, idAns, cash):
		try:
			self.sql.execute(f'SELECT cash FROM users WHERE id = {idAns} ')
			self.sql.execute(f' UPDATE users SET cash = {cash} WHERE id = {idAns} ')
		except Exception as e:
			print(e, 45)
		self.db.commit()
			
	def getAns(self, id):
		try:
			self.sql.execute(f""" SELECT ans FROM users WHERE id = {id} """)
			b = self.sql.fetchone()
			b = str(b)
			b = b.replace('(', '')
			b = b.replace(',', '')
			b = b.replace(')', '')
			b = int(b)
			return b
		except Exception as e:
			pass
		
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
		try:
			self.sql.execute(f""" SELECT money FROM users WHERE id = {id} """)
			b = self.sql.fetchone()
			b = str(b)
			b = b.replace('(', '')
			b = b.replace(',', '')
			b = b.replace(')', '')
			try:
				b = float(b)
				b-=sum
			except:
				b = int(b)
				b-=sum
			self.sql.execute(f' UPDATE users SET money = {b} WHERE id = {id} ')
			self.db.commit()
		except Exception as e:
			pass
		
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
			
	def setRef(self, id, ref):
		try:
			self.sql.execute(f'SELECT refid FROM users WHERE id = {id}')
			self.sql.execute(f'UPDATE users SET refid = {ref} WHERE id = {id}')
			self.db.commit()
		except Exception as e:
			print(e, 117)
			
	def getRef(self, id):
		try:
			self.sql.execute(f""" SELECT refid FROM users WHERE id = {id} """)
			b = self.sql.fetchone()
			b = str(b)
			b = b.replace('(', '')
			b = b.replace(',', '')
			b = b.replace(')', '')
			b = int(b)
			return b
		except Exception as e:
			pass
		
	def setTask(self, id, task):
		try:
			self.sql.execute(f"""UPDATE oder SET task = '{task}' WHERE id = {id}""")
			self.db.commit()
		except Exception as e:
			print(e, 134)
	
	def setUrl(self, id, link):
		try:
			self.sql.execute(f""" UPDATE oder SET url = '{link}' WHERE id = {id} """)
			self.db.commit()
		except Exception as e:
			print(e, 141)
			
	def setOder(self, id):
		try:
			self.sql.execute(f""" SELECT id FROM oder WHERE id = {id} """)
			if self.sql.fetchone() is None:
				self.sql.execute('INSERT INTO oder VALUES(?, ?, ?, ?, ?)', (id, '0', 0, 0, '0'))
				self.db.commit()
		except Exception as e:
			print(e, 150)
			
	def getTask(self, id):
		try:
			self.sql.execute(f""" SELECT task FROM oder WHERE id = {id} """)
			b = self.sql.fetchone()
			b = str(b[0])
		
			return b
		except Exception as e:
			print(e, 'getTask')
		
	def setMoney(self, id, s):
		try:
			self.sql.execute(f'UPDATE oder SET money = {s} WHERE id = {id}')
			self.db.commit()
		except Exception as e:
			print(e, 134)
			
	def getWork(self, num):
			self.sql.execute(""" SELECT task FROM oder""")
			b = self.sql.fetchall()
			i=0
			f = True
			for el in b:
				el = str(el)
				el = el.replace('(', '')
				el = el.replace(',', '')
				el = el.replace('\'', '')
				el = el.replace(')', '')
				self.sql.execute(""" SELECT money FROM oder WHERE rowid = '{i}' """)
				i+=1
				if i-1>=num and self.sql.fetchone() != 0 and f == True:
					f = False
					return el
		
	def getNum(self, id):
		try:
			self.sql.execute(f""" SELECT tasks FROM users WHERE id = {id} """)
			b = self.sql.fetchone()
			b = str(b)
			b = b.replace('(', '')
			b = b.replace(',', '')
			b = b.replace(')', '')
			return int(b)
		except Exception as e:
			pass
		
	def setNum(self, id, num):
		try:
			self.sql.execute(f""" SELECT tasks FROM users WHERE id = {id} """)
			b = self.sql.fetchone()
			print(b)
			b = str(b)
			b = b.replace('(', '')
			b = b.replace(',', '')
			b = b.replace(')', '')
			b = int(b)
			b+=num
			
			self.sql.execute(f' UPDATE users SET tasks = {b} WHERE id = {id} ')
			self.db.commit()
		except Exception as e:
			print(e, 206)
			
	def getLink(self, num):
		try:
			self.sql.execute(""" SELECT url FROM oder""")
			b = self.sql.fetchall()
			i=0
			url = []
			for el in b:
				el = str(el)
				el = el.replace('(', '')
				el = el.replace(',', '')
				el = el.replace('\'', '')
				el = el.replace(')', '')
				self.sql.execute(""" SELECT money FROM oder WHERE rowid = '{i}' """)
				print(el)
				url.append(el)
			return url
		except Exception as e:
			pass
				
	def getComment(self, num):
		try:
			self.sql.execute(f""" SELECT comment FROM oder WHERE rowid = {num} """)
			b = self.sql.fetchone()
			b = str(b)
			b = b.replace('(', '')
			b = b.replace(',', '')
			b = b.replace(')', '')
			return b
		except Exception as e:
			pass
		
	def setComment(self, id, text):
		try:
			self.sql.execute(f""" UPDATE oder SET comment = '{text}' WHERE id = {id} """)
			self.db.commit()
		except Exception as e:
			print(e, 243)
			
	def setAns(self, id, task):
		try:
			self.sql.execute(f"""UPDATE users SET ans = '{task}' WHERE id = {id}""")
			self.db.commit()
		except Exception as e:
			print(e, 245)
			
	def getAns(self, id):
		try:
			self.sql.execute(f""" SELECT ans FROM users WHERE id = {id} """)
			b = self.sql.fetchone()
			b = str(b)
			b = b.replace('(', '')
			b = b.replace(',', '')
			b = b.replace(')', '')
			return b
		except Exception as e:
			pass
		
	def moneyTask(self, rowid, sum):
		try:
			self.sql.execute(f""" SELECT money FROM oder WHERE rowid = {rowid} """)
			b = self.sql.fetchone()
			b = str(b)
			b = b.replace('(', '')
			b = b.replace(',', '')
			b = b.replace(')', '')
			try:
				b = float(b)
				b-=sum
			except:
				b = int(b)
				b-=sum
			self.sql.execute(f' UPDATE users SET money = {b} WHERE id = {id} ')
			self.db.commit()
		except Exception as e:
			pass
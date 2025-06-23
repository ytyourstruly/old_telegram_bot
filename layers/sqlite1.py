import os
from typing import Dict, List, Tuple
import sqlite3 as sq
path = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(path, 'database.db')
base = sq.connect(db)
cursor = base.cursor()

def _init_sqlite1():
	with open("database.sql", "r", encoding="utf8") as a:
		sql = a.read()
	cursor.executescript(sql)
	base.commit()

def check_db():
	query = "select name from sqlite_master where type='table' and name='grade'"
	cursor.execute(query)
	table_exists = cursor.fetchall()
	if table_exists:
		return
	else:
		_init_sqlite1()

check_db()

class db:
	"""class db that initializes the base and cursor instances"""
	def __init__(self):
		self.base = base
		self.cursor = cursor
	def insert(self, table: str, column_values: Dict):
		"""method that inserts the tuple of values through dictionary, where keys are used for columns and placeholders """
		columns = ", ".join(column_values.keys())
		values = [tuple(column_values.values())]
		values1 = ", ".join("?" * len(column_values.keys()))
		cursor.executemany(f"insert into {table} ({columns}) values ({values1})", values)
		base.commit()
	
	def fetchgrades(self, columns: List[str]) -> List[Dict]:
		"""method that fetches a query through splitting list of columns"""
		query = "select {} from grade"
		cursor.execute(query.format(','.join(columns.split(" "))))
		rows = cursor.fetchall()
		result = []
		for row in rows:
			dict_row = {}
			for i, s in enumerate(columns.split()):
				dict_row[s] = row[i]
			result.append(dict_row)
		return result

	def fetchsubject(self, columns: List[str]) -> List[Dict]:
		"""method that fetches a query through splitting list of columns"""
		query = "select {} from subject"
		cursor.execute(query.format(','.join(columns.split(" "))))
		rows = cursor.fetchall()
		result = []
		for row in rows:
			dict_row = {}
			for i, c in enumerate(columns.split()):
				dict_row[c] = row[i]
			result.append(dict_row)
		return result

	def editsubject(self, id, aliases, name) -> None:
		"""method executes a query through using primary (subjects) and foreign (grades) keys"""
		cursor.execute(f"update subject set name='{name}', aliases='{aliases}' where id = {id}")
		cursor.execute(f"update grade set subject_name = '{name}' where subject_id = {id}")
		base.commit()


	
	def delete_subject(self, id, subject_name: str) -> None:
		"""method executes a query through using primary (subjects) and foreign (grades) keys"""
		cursor.execute(f"delete from subject where name='{subject_name}'")
		cursor.execute(f"delete from grade where subject_id = {id}")
		base.commit()


	def delete_grade(self, id) -> None:
		"""method executes a query through using primary keys"""
		cursor.execute(f"delete from grade where id = {id}")
		base.commit()

		
	def delete_grade_all(self) -> None:
		cursor.execute(f"delete from grade")
		base.commit()


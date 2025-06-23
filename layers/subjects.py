from typing import Dict, List

import exceptions

import re

import sqlite1 as db_1
db = db_1.db()

class Subject(Subjects):
	def __init__(self, subjects: List[str], id: int, name: str, aliases: List[str]):
		super().__init__(subjects)
		self.id = id
		self.name = name
		self.aliases = aliases
	
	def set_subject(self, raw_message:str):
		message = Message._parse_message(raw_message)
		# db.insert("subject", {"name": subject.name,"aliases": subject.aliases}) 
		# return Subject(id=None, name=message.name, aliases=message.aliases)
		return self.name, self.aliases
	
	def set_subject_FSM(self, raw_message: str) -> None:
		parsed_message = self._parse_message(raw_message)
		name = parsed_message.name
		aliases = parsed_message.aliases
		db.insert("subject", {"name": name,"aliases": aliases}) 

	def edit_subject_FSM(self, name_old:str, name_new: str, aliases: List[str])-> None:
		"""method that accepts three variables and finds the old subject editing through db instance"""
		subject = self.get_subject(name_old)
		db.editsubject(subject.id, aliases, name_new)

	def get_subject(self, subjects):
		"""method that finds the subject by looping through the subject fields"""
		found = None
		for subject in subjects:
			if subject.name == subject_name:
				found = subject
			else:
				for alias in subject.aliases:
					if subject_name == alias:
						found = subject
		if not found:
			raise exceptions.NotCorrectMessage("Предмет не найден!")
		return found

	def delete(self, id: int, subject_name: str) -> None:
		db.delete_subject(id, subject_name)

	# def _parse_message(self,raw_message: str) -> List[Message]:
		# """method that parses the message"""
		# regexp_result = re.match(r"([a-zA-Z]+|[ЁёА-я]+) (\w+[\s,\w]+)", raw_message)
		# if not regexp_result or not regexp_result.group(0) or not regexp_result.group(1) or not regexp_result.group(2):
		# 	raise exceptions.NotCorrectMessage("Неправильно ввела предмет!")
		# name = regexp_result.group(1).replace(" ", "")
		# aliases = regexp_result.group(2).replace(" ","")
		# for subject in self.subjects:
		# 	if subject.name == name:
		# 		raise exceptions.NotCorrectMessage("Такой предмет уже есть!")
		# return Message(name=name, aliases=aliases)



class Message:
	def __init__(self, name, aliases):
		self.name = name
		self.aliases = aliases
	def _parse_message(self,raw_message: str):
		regexp_result = re.match(r"([a-zA-Z]+|[ЁёА-я]+) (\w+[\s,\w]+)", raw_message)
		if not regexp_result or not regexp_result.group(0) or not regexp_result.group(1) or not regexp_result.group(2):
			raise exceptions.NotCorrectMessage("Неправильно ввела предмет!")
		name = regexp_result.group(1).replace(" ", "")
		aliases = regexp_result.group(2).replace(" ","")
		# for subject in self.subjects:
		# 	if subject.name == name:
		# 		raise exceptions.NotCorrectMessage("Такой предмет уже есть!")
		return Message(name=name, aliases=aliases)



class Subjects:
	"""Class subject that returns the loaded subjects"""
	def __init__(self):
		self.subjects = self.load_subjects()
	
	def load_subjects(self) -> List[Subject]:
		"""method that returns the list of dictionaries through appending aliases to each subject"""
		subjects = db.fetchsubject("id name aliases")
		result = []
		for i, s in enumerate(subjects):
			aliases = list(map(str.strip, s["aliases"].split(",")))
			result.append(Subject(id=s['id'], name=s['name'], aliases=aliases))
		return result


	def get_all_subjects(self) -> List[Dict]:
		"""method that returns list of dictionaries for subjects"""
		return self.subjects
from datetime import datetime, timedelta
import re
from typing import Dict, List, NamedTuple, Optional
from subjects import Subjects
import sqlite1 as db_1


db = db_1.db()



class Message(NamedTuple):
	amount: int
	subject_text: str
	amount_achieved: int


class Grade(NamedTuple):
	id: Optional(int)
	amount: int
	amount_achieved: int
	subject_name: str


def add_grade(raw_message: str) -> List[Dict]:
now = datetime.now()
subject = Subjects(parsed_message.subject_text)
parsed_message = parse_message(raw_message)
db.insert("grade", {"amount": parsed_message.amount,"amount_achieved": parsed_message.amount_achieved,
"subject_name": subject, "date": now.strftime("%Y-%m-%d"),"raw_text": raw_message}) 
result = [{"id": None, "amount": parsed_message.amount,"amount_achieved": parsed_message.amount_achieved,
"subject_name": subject, "date": now.strftime("%Y-%m-%d")}]
return result


def add_grade_FSM(amount: int, amount_achieved: int, subject_name: str) -> None:
now = datetime.now()
subject = Subjects().get_subject(subject_name)
db.insert("grade", {"amount": amount, "amount_achieved": amount_achieved,
"subject_name": subject.name, "subject_id": subject.id, "date": now.strftime("%Y-%m-%d"),"raw_text": None})


def boundaries(percentage: str) -> int:
number = 0
if float(percentage.strip('\r%'))<15.0:
	number = 0
elif (15.0<=float(percentage.strip('\r%'))<=20.0):
	number = 1
elif (20.0<=float(percentage.strip('\r%'))<=35.0):
	number = 2
elif (35.0<=float(percentage.strip('\r%'))<=50.0):
	number = 3
elif (50.0<=float(percentage.strip('\r%'))<=70.0):
	number = 4
elif (70.0<=float(percentage.strip('\r%'))<=100.0):
	number = 5
return number


def get_today_grades() -> List[Dict]:
now = datetime.now()
grades_all = db.fetchgrades("amount amount_achieved date subject_name")
grades_today = [item for item in grades_all if item['date'] == now.strftime("%Y-%m-%d")]
return appendsum(grades_today)


def appendsum(grades: List) -> List[Dict]:
subjects = sorted(set(map(lambda x: x['subject_name'], grades)))
result = []
for subject in subjects:
	result.append({'subject_name':subject,'amount':sum(map(lambda x: x['amount'] if x['subject_name']==subject else 0,grades)), 
	'amount_achieved':sum(map(lambda x: x['amount_achieved'] if x['subject_name']==subject else 0,grades))})
	for row in result:
		amount = row['amount']
		amount_achieved = row['amount_achieved']
		percentage = str(round((amount_achieved/amount)*100))+'%'
		row['percentage'] = percentage
		row['number'] = boundaries(percentage)
	result = sorted(result, key=lambda x: float(x['percentage'].strip('\r%')))
return result



def get_yesterday_grades() -> List[Dict]:
now = datetime.now()
yesterday = now - timedelta(days=1) 
grades_all = db.fetchgrades("amount amount_achieved date subject_name")
grades_yesterday = [item for item in grades_all if item['date'] == yesterday.strftime("%Y-%m-%d")]
return appendsum(grades_yesterday)


def get_week_grades() -> List[Dict]:
day = datetime.today()
weekday = day.isoweekday()
start = day - timedelta(days=weekday)
dates_1 = [start + timedelta(days=d) for d in range(7)]
dates = [str(d.strftime('%Y-%m-%d')) for d in dates_1]
grades_all = db.fetchgrades("amount amount_achieved date subject_name")
grades_week = []
for date in dates:
	for item in grades_all:
		if item['date'] == date:
			grades_week.append(item)
return appendsum(grades_week)



def delete_grade(row_id: int) -> None:
db.delete_grade(row_id)


def last_grades() -> List[Dict]:
rows = db.fetchgrades("id amount amount_achieved date subject_name")
result = sorted(rows, key=lambda x: x['date'])
return result

def last_grades_subject() -> List[Dict]:
grades_all = db.fetchgrades("amount amount_achieved date subject_name")
return appendsum(grades_all)

def delete_all_grades() -> None:
db.delete_grade_all()


def parse_message(raw_message: str) -> Message:
regexp_result = re.match(r"(\d{1,2}).(\d{1,2})\s(\w+)", raw_message)
if not regexp_result or not regexp_result.group(0) \
		or not regexp_result.group(1) or not regexp_result.group(2) or not regexp_result.group(3):
	raise exceptions.NotCorrectMessage("Пожалуйста напиши в таком формате:""\n19.23 мат")
amount_achieved = regexp_result.group(1)
amount = regexp_result.group(2)
subject_text = regexp_result.group(3).strip().lower()
if int(amount)<int(amount_achieved):
	raise exceptions.NotCorrectMessage("Неправильно ввели цифры!")
else:
	return Message(amount=int(amount), amount_achieved=int(amount_achieved), subject_text=subject_text)




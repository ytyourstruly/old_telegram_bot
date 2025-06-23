from aiogram import Bot, types, Dispatcher, executor
from aiogram.utils.markdown import text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher	import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import exceptions
import grades as Grades
import subjects as Subjects
import os
import config
import re
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, Message

st = [ "Предметы", "Оценки", "Автор" ]
start_menu_buttons = [KeyboardButton(x) for x in st]
start_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_menu.row(start_menu_buttons[0], start_menu_buttons[1], start_menu_buttons[2])
g = ["Добавить оценку:addgradeinline", "Показать оценки:showgrade", "Показать оценки (время):showgradetime", "Удалить все оценки:deleteallgrades", "Назад:back_to_start_menu"]
grade_buttons = [InlineKeyboardButton(x.split(":")[0], callback_data=x.split(":")[1]) for x in g]
grade_markup = InlineKeyboardMarkup(row_width=2)
grade_markup.add(*grade_buttons)
z = ["Показать все оценки:showgradeall","Оценки с предметами:showgradeallsubject", "Назад:back_to_start_menu"]
y = ["Показать оценки на сегодня:showgradetoday","Показать оценки на вчера:showgradeyesterday", "Показать оценки на неделю:showgradeweek", "Назад:back_to_start_menu"]
grade_buttons_show = [InlineKeyboardButton(x.split(":")[0], callback_data=x.split(":")[1]) for x in z]
grade_buttons_show_time = [InlineKeyboardButton(x.split(":")[0], callback_data=x.split(":")[1]) for x in y]
grade_markup_show = InlineKeyboardMarkup(row_width=2)
grade_markup_show.add(*grade_buttons_show)
grade_markup_show_time = InlineKeyboardMarkup(row_width=2)
grade_markup_show_time.add(*grade_buttons_show_time)
s = ["Добавить предмет:addsubjectinline", "Показать предметы:showsubject", "Изменить предмет:editsubject", "Удалить предмет:deletesubject", "Назад:back_to_start_menu"]
subject_buttons = [InlineKeyboardButton(x.split(":")[0], callback_data=x.split(":")[1]) for x in s]
subject_markup = InlineKeyboardMarkup(row_width=2)
subject_markup.add(*subject_buttons)

i = ["Нет:no","Да:yes"]
confirmation_buttons = [InlineKeyboardButton(x.split(":")[0], callback_data=x.split(":")[1]) for x in i]
confirmation_markup = InlineKeyboardMarkup(row_width=1)
confirmation_markup.add(*confirmation_buttons)

bot = Bot(token=os.getenv('API_KEY'))
dp = Dispatcher(bot=bot, storage=MemoryStorage())

async def on_startup(_):
	print('Bot is online!')




@dp.message_handler(regexp="Автор")
@dp.message_handler(commands=['author'])
async def author(message: types.Message):
	await message.answer(text = "автор: Tursynbay Yeskendir\n\n"\
	"мой емейл: tursynbay.y@nisa.edu.kz",
	reply_markup=start_menu)

help_message = text(
	"\nПривет! Я твой бот. Что я могу сделать:",
	"Добавлять твои оценки",
	"Показывать твои предметы",
	"Давать статистику на твои оценки",
	sep="\n"
)

@dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
	await message.answer(help_message, reply_markup=start_menu)



@dp.message_handler(regexp="Оценки")
async def grades(message: types.Message):
	await message.answer('Что ты хочешь сделать?', reply_markup=grade_markup)

@dp.callback_query_handler(lambda callback_query: callback_query.data == "showgrade")
async def showgradeall(callback_query: types.CallbackQuery):
	await callback_query.message.answer("Выбери что хочешь", reply_markup=grade_markup_show)

@dp.callback_query_handler(lambda callback_query: callback_query.data == "showgradetime")
async def showgradealltime(callback_query: types.CallbackQuery):
	await callback_query.message.answer("Ну что ж, оценки?", reply_markup=grade_markup_show_time)

@dp.message_handler(regexp="Предметы")
async def subjects(message: types.Message):
	await message.answer('Что ты хочешь сделать?', reply_markup=subject_markup)

@dp.callback_query_handler(lambda callback_query: callback_query.data == "showgradeall")
async def showgradeall(callback_query: types.CallbackQuery):
	grade = Grades.last_grades()
	if grade:
		rows = [
			f"В {grade[g]['date']} для {grade[g]['subject_name']}: ты получила {grade[g]['amount_achieved']} из {grade[g]['amount']}\n"
			f"нажми на -> /del{grade[g]['id']}, чтобы удалить "
			for g in range(len(grade))]
		answer = "Все оценки:\n\n " + "\n\n  ".join(rows)
		await callback_query.message.answer(answer,reply_markup=start_menu)
	else:
		await callback_query.message.answer("Нет оценок", reply_markup=start_menu)

@dp.callback_query_handler(lambda callback_query: callback_query.data == "showgradeallsubject")
async def showgradeallsubject(callback_query: types.CallbackQuery):
	grade = Grades.last_grades_subject()
	if grade:
		rows = [f"Для предмета {grade[g]['subject_name']}, ты получила {grade[g]['amount_achieved']}" 
			      f" из {grade[g]['amount']}.\n"
			      f"Это в оценке: {grade[g]['number']}\n"
			      f"Это в процентах: {grade[g]['percentage']} " for g in range(len(grade))]
		answer = "Все оценки:\n\n " + "\n\n  ".join(rows)
		await callback_query.message.answer(answer,reply_markup=start_menu)
	else:
		await callback_query.message.answer("Нет оценок", reply_markup=start_menu)
		

@dp.callback_query_handler(lambda callback_query: callback_query.data == "showgradetoday")
async def showgradetoday(callback_query: types.CallbackQuery):
	grade = Grades.get_today_grades()
	if grade:
		rows = [
		f"Для предмета {grade[g]['subject_name']}, ты получила {grade[g]['amount_achieved']}" 
			      f" из {grade[g]['amount']}.\n"
			      f"Это в оценке: {grade[g]['number']}\n"
			      f"Это в процентах: {grade[g]['percentage']} " for g in range(len(grade))]
		answer = "Все оценки:\n\n " + "\n\n  ".join(rows)
		await callback_query.message.answer(answer,reply_markup=start_menu)
	else:
		await callback_query.message.answer("Нет оценок на сегодня", reply_markup=start_menu)


@dp.callback_query_handler(lambda callback_query: callback_query.data == "showgradeyesterday")
async def showgradeyesterday(callback_query: types.CallbackQuery):
	grade = Grades.get_yesterday_grades()
	if grade:
		rows = [
			f"Для предмета {grade[g]['subject_name']}, ты получила {grade[g]['amount_achieved']}" 
				      f" из {grade[g]['amount']}.\n"
				      f"Это в оценке: {grade[g]['number']}\n"
				      f"Это в процентах: {grade[g]['percentage']} " for g in range(len(grade))]
		answer = "Все оценки:\n\n " + "\n\n  ".join(rows)
		await callback_query.message.answer(answer,reply_markup=start_menu)
	else:
		await callback_query.message.answer("Нет оценок на вчера",reply_markup=start_menu)

@dp.callback_query_handler(lambda callback_query: callback_query.data == "showgradeweek")
async def showgradeweek(callback_query: types.CallbackQuery):
	grade = Grades.get_week_grades()
	if grade:
		rows = [
			f"Для предмета {grade[g]['subject_name']}, ты получила {grade[g]['amount_achieved']}" 
				      f" из {grade[g]['amount']}.\n"
				      f"Это в оценке: {grade[g]['number']}\n"
				      f"Это в процентах: {grade[g]['percentage']} " for g in range(len(grade))]
		answer = "Все оценки:\n\n " + "\n\n  ".join(rows)
		await callback_query.message.answer(answer,reply_markup=start_menu)
	else:
		await callback_query.message.answer("Нет оценок на эту неделю",reply_markup=start_menu)



class Addgrade(StatesGroup):
	nameofsubject = State()
	amount_achieved = State()
	amount = State()



@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel(message:types.Message, state: FSMContext):
	current_state = await state.get_state()
	if current_state is None:
		return
	await state.finish()
	await message.reply('Все хорошо, отменяю', reply_markup=start_menu)

@dp.callback_query_handler(lambda callback_query: callback_query.data =="addgradeinline", state=None)
async def add_grade_start(callback_query: types.CallbackQuery):
	await bot.send_message(callback_query.from_user.id,"Ты можешь еще написать в такой форме: 23.24 математика")
	await callback_query.message.answer("Введи предмет")
	await Addgrade.nameofsubject.set()
@dp.message_handler(state=Addgrade.nameofsubject)
async def add_grade_1(message:types.Message, state:FSMContext):
	try:
		subject = Subjects.Subjects().get_subject(message.text.lower())
		await state.update_data(subject = subject.name)
		await Addgrade.next()
		await message.reply("Напиши сколько получила")
	except exceptions.NotCorrectMessage as e:
		await message.answer(str(e), reply_markup=start_menu)
		await state.finish()

@dp.message_handler(state=Addgrade.amount_achieved)
async def add_grade_2(message:types.Message, state:FSMContext):
	if not message.text.isdigit():
		await message.reply("Что за цифры? Напиши еще раз")
		await state.set_state(Addgrade.amount_achieved)
	elif int(message.text)>100:
		await message.reply("Неправильно ввела цифры!\nНапиши заново сколько получила")
		await state.set_state(Addgrade.amount_achieved)
	else:
		await state.update_data(amount_achieved=int(message.text))
		await message.reply("Напиши из скольки")
		await Addgrade.next()


@dp.message_handler(state=Addgrade.amount)
async def add_grade_3(message:types.Message, state:FSMContext):
	state_now = await state.get_data()
	if not message.text.isdigit():
		await message.reply("Что за цифры? Напиши еще раз")
		await state.set_state(Addgrade.amount)
	elif int(state_now['amount_achieved'])>int(message.text):
		await message.reply("Неправильно ввела цифры!\nНапиши заново сколько получила")
		await state.set_state(Addgrade.amount)
	elif int(message.text)>100:
		await message.reply("Неправильно ввела цифры!\nНапиши заново сколько получила")
		await state.set_state(Addgrade.amount)
	else:
		await message.answer("Все правильно?", reply_markup=confirmation_markup)
		await state.update_data(amount=int(message.text))
		
@dp.callback_query_handler(lambda callback_query: callback_query.data == "yes", state=Addgrade.amount)
async def add_grade_finish(callback_query: types.CallbackQuery, state=FSMContext):
	state_now = await state.get_data()
	Grades.add_grade_FSM(state_now['amount'], state_now['amount_achieved'], state_now['subject'])
	await state.finish()
	answer = (f"Добавил оценки на {state_now['amount_achieved']} из {state_now['amount']} для предмета {state_now['subject']}.")
	await callback_query.message.answer(answer, reply_markup=start_menu)

@dp.callback_query_handler(lambda callback_query: callback_query.data == "no", state=Addgrade.amount)
async def add_grade_cancel(callback_query: types.CallbackQuery, state=FSMContext):
	await callback_query.message.answer("Хорошо, давай заново\nНапиши предмет")
	await state.set_state(Addgrade.nameofsubject)

@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_grade(message: types.Message):
	row_id = int(message.text[4:])
	Grades.delete_grade(row_id)
	await message.answer("Успешно удалил!", reply_markup=start_menu)


class Editsubject(StatesGroup):
	subject_old = State()
	subject_new = State()
	aliases = State()

@dp.callback_query_handler(lambda callback_query: callback_query.data =="editsubject", state= None)
async def edit_subject_start(callback_query: types.CallbackQuery):
	await Editsubject.subject_old.set()
	await callback_query.message.answer("Введи предмет")
@dp.message_handler(state=Editsubject.subject_old)
async def edit_subject_1(message:types.Message, state:FSMContext):
	try:
		subject = Subjects.Subjects().get_subject(message.text.lower())
		await state.update_data(subject_old = subject.name)
		await Editsubject.next()
		await message.reply("Напиши новый предмет")
	except exceptions.NotFoundError as e:
		await message.answer(str(e))
		await message.reply("Напиши еще раз предмет")
		await state.set_state(Editsubject.subject_old)
@dp.message_handler(state=Editsubject.subject_new)
async def edit_subject_2(message:types.Message, state:FSMContext):
	if not message.text.isdigit():
		await state.update_data(subject_new= message.text.lower())
		await Editsubject.next()
		await message.reply("Напиши элиасы")
	else: 	
		await message.reply("Что за предмет? Напиши еще раз")
		await state.set_state(Editsubject.subject_new)

@dp.message_handler(state=Editsubject.aliases)
async def edit_subject_3(message:types.Message, state:FSMContext):
	if not message.text.isdigit():
		await message.answer("Все правильно?", reply_markup=confirmation_markup)
		await state.update_data(aliases=message.text.lower())
	else:
		await message.reply("Что за элиасы? Напиши еще раз")
		await state.set_state(Editsubject.aliases)

@dp.callback_query_handler(lambda callback_query: callback_query.data == "yes", state=Editsubject.aliases)
async def edit_subject_4(callback_query:types.CallbackQuery, state:FSMContext):
	state_now = await state.get_data()
	Subjects.Subjects().edit_subject_FSM(state_now['subject_old'], state_now['subject_new'], state_now['aliases'])
	await state.finish()
	answer = (f"Изменил предмет из {state_now['subject_old']} на {state_now['subject_new']} с элиасами {state_now['aliases']}.")
	await callback_query.message.answer(answer, reply_markup=start_menu)

@dp.callback_query_handler(lambda callback_query: callback_query.data == "no", state=Editsubject.aliases)
async def edit_subject_cancel(callback_query: types.CallbackQuery, state=FSMContext):
	await callback_query.message.answer("Хорошо, давай заново\nНапиши старый предмет")
	await state.set_state(Editsubject.subject_old)

class Deletesubject(StatesGroup):
	subject_old = State()

@dp.callback_query_handler(lambda callback_query: callback_query.data =="deletesubject", state= None)
async def delete_subject_start(callback_query: types.CallbackQuery):
	await Deletesubject.subject_old.set()
	await callback_query.message.answer(("Введи предмет"))

@dp.message_handler(state=Deletesubject.subject_old)
async def delete_subject_1(message:types.Message, state:FSMContext):
	try:
		subject = Subjects.Subjects().get_subject(message.text.lower())
		await message.answer("Ты точно хочешь это сделать?", reply_markup=confirmation_markup)
		await state.update_data(subject_old=subject.name, subject_id=subject.id)
	except exceptions.NotCorrectMessage as e:
		await message.answer(str(e))
		await message.reply("Напиши еще раз предмет")
		await state.set_state(Deletesubject.subject_old)


@dp.callback_query_handler(lambda callback_query: callback_query.data == "yes", state=Deletesubject.subject_old)
async def delete_subject_2(callback_query:types.CallbackQuery, state:FSMContext):
	state_now = await state.get_data()
	Subjects.Subjects().delete(state_now['subject_id'], state_now['subject_old'])
	await callback_query.message.reply("Удалил", reply_markup=start_menu)
	await state.finish()


@dp.callback_query_handler(lambda callback_query: callback_query.data == "no", state=Deletesubject.subject_old)
async def delete_subject_cancel(callback_query: types.CallbackQuery, state=FSMContext):
	await callback_query.message.answer("Хорошо, отменяю", reply_markup=start_menu)
	await state.finish()


@dp.message_handler(lambda message: re.match(r'\d.+', message.text))
async def add_grade(message: types.Message):
	try:
		grade = Grades.add_grade(message.text)
		row = [f"Добавил оценки на {grade[g]['amount_achieved']} из {grade[g]['amount']} для {grade[g]['subject_name']}.\n"
		f"Дата: {grade[g]['date']}" for g in range(len(grade))]
		answer = "".join(row)
		await message.answer(answer, reply_markup=start_menu)
	except exceptions.NotCorrectMessage as e:
		await message.answer(str(e),reply_markup=start_menu)
		return

@dp.callback_query_handler(lambda callback_query: callback_query.data == "back_to_start_menu")
async def back_to_main_menu(callback_query: types.CallbackQuery):
	await callback_query.message.answer("Иду назад", reply_markup=start_menu)

class Addsubject(StatesGroup):
	subject_new = State()
	aliases = State()

@dp.callback_query_handler(lambda callback_query: callback_query.data =="addsubjectinline", state= None)
async def add_subject_inline_1(callback_query: types.CallbackQuery):
	await bot.send_message(callback_query.from_user.id,"Ты можешь еще написать в такой форме: математика мат, матеша")
	await Addsubject.subject_new.set()
	await callback_query.message.answer(("Введи предмет"))

@dp.message_handler(state=Addsubject.subject_new)
async def add_subject_inline_2(message:types.Message, state:FSMContext):
	try:	
		subject = Subjects.Subjects().get_subject(message.text.lower())
		await message.reply("Такой предмет уже есть!", reply_markup=start_menu)
		await state.finish()
	except:
		if not message.text.isdigit():
			await state.update_data(subject_new = message.text.lower())
			await Addsubject.next()
			await message.reply("Напиши элиасы")
		else:
			await message.reply("Что за предмет? Напиши еще раз")
			await state.set_state(Addsubject.subject_new)

@dp.message_handler(state=Addsubject.aliases)
async def add_subject_inline_3(message:types.Message, state:FSMContext):
	try:
		subject = Subjects.Subjects().get_subject(message.text.lower())
		await message.reply("Такой алиас уже есть! Напиши еще раз")
		await state.set_state(Addsubject.aliases)
	except:
		if not message.text.isdigit():
			await message.answer("Все правильно?", reply_markup=confirmation_markup)
			await state.update_data(aliases=message.text.lower())
		else:
			await message.reply("Что за алиасы? Напиши еще раз")
			await state.set_state(Addsubject.aliases)

@dp.callback_query_handler(lambda callback_query: callback_query.data == "yes", state=Addsubject.aliases)
async def add_subject_inline_4(callback_query:types.CallbackQuery, state:FSMContext):
	try:
		state_now = await state.get_data()
		Subjects.Subjects().add_subject_FSM(f"{state_now['subject_new']} {state_now['aliases']}")
		await state.finish()
		answer = (f"Добавил предмет {state_now['subject_new']} с элиасами {state_now['aliases']}.")
		await callback_query.message.answer(answer, reply_markup=start_menu)
	except exceptions.NotCorrectMessage as e:
		await callback_query.message.answer(str(e))
		await callback_query.message.answer("Напиши еще раз предмет")
		await state.set_state(Addsubject.subject_new)



@dp.callback_query_handler(lambda callback_query: callback_query.data == "no", state=Addsubject.aliases)
async def add_subject_cancel(callback_query: types.CallbackQuery, state=FSMContext):
	await callback_query.message.answer("Хорошо, давай заново\nНапиши новый предмет")
	await state.set_state(Addsubject.subject_new)



@dp.message_handler(lambda message: re.match(r'\w.+', message.text))
async def add_subject(message: types.Message):
	try:
		subject = Subjects.Subjects().add_subject(message.text)
	except exceptions.NotCorrectMessage as e:
		await message.answer(str(e))
		return
	answer = (
		f"Добавил предмет {subject.name} с элиасами {subject.aliases}")
	await message.answer(answer, reply_markup=start_menu)

@dp.callback_query_handler(lambda callback_query: callback_query.data == "showsubject")
async def showsubject(callback_query: types.CallbackQuery):
	subjects = Subjects.Subjects().get_all_subjects()
	if not subjects:
		await callback_query.message.answer("Нет предметов", reply_markup=start_menu)
	else:
		rows = [f"Предмет: {s.name}, элиасы: {s.aliases}\n"
			f"перейди в меню, чтобы удалить или изменить" for s in subjects]
		answer = "Все предметы:\n\n " + "\n\n ".join(rows)
		await callback_query.message.answer(answer, reply_markup=start_menu)

@dp.callback_query_handler(lambda callback_query: callback_query.data == "deleteallgrades")
async def delete_all(callback_query: types.CallbackQuery):
	await callback_query.message.answer("Точно?", reply_markup=confirmation_markup)
	
@dp.callback_query_handler(lambda callback_query: callback_query.data == "yes")
async def delete_all_1(callback_query: types.CallbackQuery):
	await callback_query.message.reply("Хорошо", reply_markup=start_menu)
	Grades.delete_all_grades()


@dp.callback_query_handler(lambda callback_query: callback_query.data == "no")
async def delete_all_2(callback_query: types.CallbackQuery):
	await callback_query.message.reply("Понял", reply_markup=start_menu)



if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

from pathlib import Path
from datetime import date
from random import randint, randrange as rr, choice
from pprint import pprint
from typing import Literal

path_files = Path.cwd() / 'names'
names_dict = {'names':[],'patronymics':[],'lastnames':[]}
days = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:21, 11:30, 12:31}

def load_date() -> None:

	"""Функция, которая читает из файлов данные(женские и мужские имена, отчества и фамилии) и 
	упорядочивает их в names_dict"""

	with open (path_files/'женские_имена.txt', 'r', encoding = 'utf - 8') as female_names, \
	open (path_files/'мужские_имена_отчества.txt', 'r', encoding = 'utf - 8') as male_names_patronymic, \
	open (path_files/'фамилии.txt' , 'r', encoding = 'utf - 8') as last_names:

		names_dict['names'].append([line.strip() for line in female_names.readlines()])
		names_dict['names'].append([line.strip().split()[0] for line in male_names_patronymic])
		male_names_patronymic.seek(0)
		names_dict['patronymics'].append([line.strip().split()[2][:-1] for line in male_names_patronymic])
		male_names_patronymic.seek(0)
		names_dict['patronymics'].append([line.strip().split()[1][1:] for line in male_names_patronymic])
		names_dict['lastnames'].append([line.strip().split()[1] if len(line.split()) == 2 else line.strip().split()[0] for line in last_names.readlines()])
		last_names.seek(0)
		names_dict['lastnames'].append([line.strip().split()[0] for line in last_names])
		
def rand_date(from_year:int = -1, years: int = -1) -> tuple[int, int, int]:
	if from_year == -1:
		from_year = date.today().year
	if years == -1:
		years = date.today().year - from_year
	rand_year = rr(from_year, from_year + years)
	rand_month = rr(1, 13)
	leap_febr = rand_month == 2 and leap_year(rand_year)
	max_day = days[rand_month] + 1 if leap_febr else days[rand_month]
	rand_day = rr(1, max_day + 1)
	return date(rand_year, rand_month, rand_day)


def leap_year(year: int) -> bool:

	"""Функция, проверяющая, является год високосным или нет"""

	return year % 4 == 0 and year % 100 != 0 or year % 400 == 0

def generate_birthdate(start: int = 1900, end: int = 2000) -> date:

	"""Функция, генерирующая и возвращающая случайную дату рождения (диапазон одно столетие), 
	учитывает количество дней в каждом месяце с учётом високосного года"""

	year = randint(start, end)
	if leap_year(year):
		days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	else:
		days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	month = randint(1, 12)
	day = randint(1, days[month - 1])
	return (date(year, month, day))

def generate_number() -> str:

	"""Функция, генерирующая и возвращающая случайный номер телефона, форматом: '+79xxxxxxxxx'"""

	return '+79'+ ''.join([str(randint(0, 9)) for _ in range(9)])
  

def generate_name():

	"""Функция, генерирующая и возвращающая случайные имя, отчество и фамилию, которые согласованы по полу из словаря: names_dict """
	gender = choice(['мужской', 'женский'])
	if gender == 'мужской':
		name = choice(names_dict['names'][1])
		patronymic = choice(names_dict['patronymics'][1])
		lastname = choice(names_dict['lastnames'][1])
	else:
		name = choice(names_dict['names'][0])
		patronymic = choice(names_dict['patronymics'][0])
		lastname = choice(names_dict['lastnames'][0])
	return name, patronymic, lastname, gender

def generate_person() -> dict['имя': str,'отчество': str,'фамилия': str,'пол': Literal['мужской', 'женский'],'дата_рождения': date,'мобильный': str]:

	"""Функция возвращает словарь с анкетными данными"""

	person = {
        'имя': '',
        'отчество': '',
        'фамилия': '',
        'пол': '',
        'дата рождения': '',
        'мобильный': ''
    }
	load_date()
	name, patronymic, lastname, gender  = generate_name()

	person['имя'] = name
	person['отчество'] = patronymic
	person['фамилия'] = lastname
	person['пол'] = gender
	person['дата рождения'] = generate_birthdate()
	person['мобильный'] = generate_number()

	return person

test = generate_person()
pprint(test)

#{'дата рождения': datetime.date(1992, 5, 25),
#'имя': 'Ираида',
# 'мобильный': '+79407594698',
#'отчество': 'Максимильяновна',
# 'пол': 'женский',
#'фамилия': 'Шарова'}

#{'дата рождения': datetime.date(1963, 12, 2),
# 'имя': 'Назар',
# 'мобильный': '+79596844537',
# 'отчество': 'Арефиевич,',
# 'пол': 'мужской',
# 'фамилия': 'Долин,'}
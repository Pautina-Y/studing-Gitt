import psycopg2
from json import loads as json_loads
from pprint import pprint
from pathlib import Path
from sys import path
# текущий проект
import generate
import queries


config_path = Path(r'C:\SQL\hospital\config.json')
config = json_loads(config_path.read_text())

connection = psycopg2.connect(**config)
connection.autocommit = True

with connection.cursor() as cursor:
    cursor.executemany(queries.ins_departments, generate.departments)
    cursor.executemany(queries.ins_sponsors, generate.sponsors)
    cursor.executemany(queries.ins_specializations, generate.specializations)
    cursor.executemany(queries.ins_wards, generate.wards)
    cursor.executemany(queries.ins_donations, generate.donations)
    cursor.executemany(queries.ins_doctors, generate.doctors)
    cursor.executemany(queries.ins_doctors_specs, generate.doctors_specs)
    cursor.executemany(queries.ins_vacations, generate.vacations)



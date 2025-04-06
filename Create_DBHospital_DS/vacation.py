import datetime

def rand_date(from_year:int = -1, years: int = -1) -> tuple[int, int, int]:
	if from_year == -1:
		from_year = datetime.date.today().year
	if years == -1:
		years = datetime.date.today().year - from_year
	rand_year = rr(from_year, from_year + years)
	rand_month = rr(1, 13)
	leap_febr = rand_month == 2 and leap_year(rand_year)
	max_day = days[rand_month] + 1 if leap_febr else days[rand_month]
	rand_day = rr(1, max_day + 1)
	return date(rand_year, rand_month, rand_day)
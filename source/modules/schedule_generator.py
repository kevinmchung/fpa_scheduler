import datetime
import random
import math

class Provider:
	def __init__(self, name, abbrev, num_work_days, vacation_dates, office_ranges, vacation_formatting):
		self.name = name
		self.abbrev = abbrev

		self.num_work_days = num_work_days
		self.num_work_idx = 0

		self.vacation_dates = vacation_dates
		if vacation_formatting:
			self.format_vacation_dates()

		self.office_ranges = office_ranges
		self.working_today = False
		self.cur_week = 0
		self.cur_month_counts = [{val:0 for val in [*office_ranges.keys(), "7am", "Call"]} for i in range(4)]
		self.mon_fri_off = 0

	def format_vacation_dates(self):
		if len(self.vacation_dates) == 0:
			self.vacation_dates = []
			return
		self.vacation_dates = self.vacation_dates.split(",")
		i = 0
		while i < len(self.vacation_dates):
			date_range = self.vacation_dates[i].split("-")
			j = 0
			while j < len(date_range):
				m, d, y = list(map(int, date_range[j].split("/")))
				if y < 2000:
					y += 2000
				date_range[j] = datetime.date(y, m, d)
				j += 1
			self.vacation_dates[i] = date_range
			i += 1

	def check_vacation_date(self, date):
		res = False
		for vac in self.vacation_dates:
			if len(vac) > 1:
				if vac[0] <= date <= vac[1]:
					res = True
			else:
				if vac[0] == date:
					res = True
		return res

	def get_week_counts(self):
		return self.cur_month_counts[self.cur_week]

	def get_valid_offices(self, cur_date, month_based, weekend_offices):
		counts = self.get_week_counts()
		out = []
		if cur_date.weekday() < 5:
			office_pool = self.office_ranges.keys()
		else:
			office_pool = weekend_offices
		if not self.check_vacation_date(cur_date) and sum(counts.values()) < self.num_work_days[self.num_work_idx]:
			for office in office_pool:
				if office in month_based:
					if sum(self.cur_month_counts[i][office] for i in range(4)) < self.office_ranges[office][1] and \
							self.cur_month_counts[self.cur_week][office] < 1:
						out.append(office)
				else:
					if counts[office] < self.office_ranges[office][1]:
						out.append(office)
		return out

	def assign_office(self, office, today):
		self.cur_month_counts[self.cur_week][office] += 1
		today[office].append(self)
		self.working_today = True

	def reset_today_assignment(self, office, today):
		self.cur_month_counts[self.cur_week][office] -= 1
		today[office].remove(self)
		self.working_today = False

	def next_day(self):
		self.working_today = False

	def next_week(self):
		self.next_day()
		self.cur_week += 1
		self.num_work_idx = (self.num_work_idx + 1) % len(self.num_work_days)
		if self.cur_week >= 4:
			self.cur_week = 0
			self.cur_month_counts = [{office:0 for office in self.office_ranges} for i in range(4)]

	def __str__(self):
		return self.abbrev

	def __hash__(self):
		return hash(self.abbrev)


def generate_week(providers, offices, weekend_offices, month_based, week_sched, cur_date, end_date):
	# if reset_scheduling.is_set():
	# 	return None

	if cur_date == end_date:
		return week_sched

	# WEEKDAY VS. WEEKEND
	if cur_date.weekday() < 5:
		office_pool = offices.keys()
	else:
		office_pool = weekend_offices

	# NEXT DAY LOGIC
	if all(len(week_sched[cur_date.weekday()][office]) >= offices[office][0] for office in office_pool): # current day is finished
		for provider in providers:
			provider.next_day()
		new_date = cur_date + datetime.timedelta(days=1)
		random.shuffle(providers)
		return generate_week(providers, offices, weekend_offices, month_based, week_sched, new_date, end_date)

	# CREATE POOLS OF AVAILABLE PROVIDERS FOR EACH OFFICEE
	valid_offices_dict = {provider:provider.get_valid_offices(cur_date, month_based, weekend_offices) for provider in providers}
	available = {office:[] for office in office_pool}

	for provider in providers:
		if not provider.working_today:
			for office in valid_offices_dict[provider]:
				available[office].append(provider)

	# SORT PROVIDERS BASED ON NEEDED WORK DAYS AND MON/FRI OFF
	def sort_func(p):
		ret = sum(p.get_week_counts().values()) - p.num_work_days[p.num_work_idx]
		if cur_date.weekday() == 0 or cur_date.weekday() == 4:
			if p.mon_fri_off != 0:
				ret *= p.mon_fri_off
		return ret

	for office in available:
		available[office] = sorted(available[office], key=sort_func)

	# print("------")

	spots_needed = lambda office: offices[office][0] - len(week_sched[cur_date.weekday()][office])

	# print(cur_date)
	# for office in office_pool:
	# 	print(office + " - " + str(len(week_sched[cur_date.weekday()][office])) + "/" + str(
	# 		spots_needed(office)) + " - " + str(len(available[office])))
	# print("----")

	# CHECK FOR IMPOSSIBLE OUTCOMES
	if any(len(available[office]) < spots_needed(office) for office in office_pool):
		return None

	sort_key = lambda office: len(available[office]) - spots_needed(office) if spots_needed(office) != 0 else math.inf
	office_pool = sorted([office for office in office_pool if spots_needed(office) > 0], key=sort_key)

	# GENERATING CODE
	for office in office_pool:
		for provider in available[office]:
			if len(week_sched[cur_date.weekday()][office]) < offices[office][0]:
				provider.assign_office(office, week_sched[cur_date.weekday()])
				schedule = generate_week(providers, offices, weekend_offices, month_based, week_sched,
										 cur_date, end_date)
				if schedule is not None:
					return schedule
				provider.reset_today_assignment(office, week_sched[cur_date.weekday()])

	return None

def fill_week(providers, offices, weekend_offices, month_based, week_sched, start_date, end_date):

	# PRIORITIZE MONDAYS AND FRIDAYS
	days = [0, 4, 1, 2, 3]
	for day in days:
		if start_date + datetime.timedelta(days=day) <= end_date:
			cur_date = start_date + datetime.timedelta(days=day)

			for office in offices:

				available = []
				for provider in providers:
					if all(provider not in week_sched[day][office] for office in week_sched[day]):
						if office in provider.get_valid_offices(cur_date, month_based, weekend_offices):
							available.append(provider)

				available = sorted(available, key=lambda p: sum(p.get_week_counts().values()) - p.num_work_days[p.num_work_idx])

				i = 0
				while i < len(available) and len(week_sched[day][office]) < offices[office][1]:
					provider = available[i]
					provider.assign_office(office, week_sched[day])
					i += 1

	return week_sched


def convert_models(models):
	provider_models = models['providers']
	location_models = models['locations']
	location_max_models = models['plms']
	vacation_models = models['vacations']

	new_providers = []
	for provider_model in provider_models:

		vacations = []
		for vacation_model in provider_model.providervacation_set.all():
			vacations.append((vacation_model.start_date, vacation_model.end_date))

		location_maxes = {}

		for provider_location_max in provider_model.providerlocationmax_set.all():
			location_maxes[provider_location_max.location.abbrev] = (0, provider_location_max.provider_at_location_max_days)

		new_providers.append(Provider(
				'{}, {}'.format(provider_model.name_last, provider_model.name_first),
				provider_model.abbrev,
				[provider_model.days_per_week],
				vacations,
				location_maxes,
				vacation_formatting=False))

	weekend_locations = {}
	locations = {}
	for location_model in location_models:
		locations[location_model.abbrev] = (location_model.provider_min, location_model.provider_max)
		if location_model.weekend:
			weekend_locations[location_model.abbrev] = location_model.num_providers_weekend

	return new_providers, locations, weekend_locations

def generate_schedule(providers, offices, weekend_offices, month_based, start_date, end_date):
	schedule = []

	for i in range(math.ceil((end_date - start_date).days / 7)):

		cur_date = start_date + datetime.timedelta(weeks=1) * i
		week_sched = None

		while week_sched is None:
			empty_sched = [{office: [] for office in (offices if i < 5 else weekend_offices)} for i in range(7)]
			random.shuffle(providers)  # shuffle providers for randomness
			# scheduling_finished.clear()
			# reset_scheduling.clear()

			scheduling_info = [providers,
							   offices,
							   weekend_offices,
							   month_based,
							   empty_sched,
							   cur_date,
							   min(end_date, cur_date + datetime.timedelta(weeks=1))]

			# timer_thread = Thread(target=timer)
			# timer_thread.daemon = True
			# timer_thread.start()

			week_sched = generate_week(*scheduling_info)
			# scheduling_finished.set()

			if week_sched is None:
				print("Impossible configuration. Resetting...")

		week_sched = fill_week(providers, offices, weekend_offices, month_based,
							   week_sched, cur_date, min(end_date, cur_date + datetime.timedelta(weeks=1)))

		for provider in providers:
			if not any(provider in week_sched[0][office] for office in week_sched[0]):
				provider.mon_fri_off += 1
			if not any(provider in week_sched[4][office] for office in week_sched[4]):
				provider.mon_fri_off += 1

		schedule.append(week_sched)

		for provider in providers:
			provider.next_week()

	return schedule
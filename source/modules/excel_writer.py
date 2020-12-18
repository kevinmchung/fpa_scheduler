import xlsxwriter
import datetime
import os

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
days = ["MON", "TUES", "WED", "THURS", "FRI", "SAT", "SUN"]

column_width = 6.3
column_starts = {}
off_columns = {"VAC": 2, "OFF": 3}

save_dir = "./scheduler/static/files/"

def make_spreadsheet(providers, offices, schedule, start_date, end_date):
	files = os.listdir(save_dir)
	full_path = [os.path.join(save_dir, file) for file in files]
	if len(files) >= 20:
		oldest_file = min(full_path, key=os.path.getctime)
		os.remove(oldest_file)

	filename = "{}_{}_schedule.xlsx".format(start_date.strftime("%m-%d"), end_date.strftime("%m-%d"))
	wb = xlsxwriter.Workbook(os.path.join(save_dir, filename))
	sheet = wb.add_worksheet("Schedule")

	header_format = wb.add_format({"font_name": "Arial", "font_size": 7, "font_color": "white",
								   "bg_color": "black", "align": "center", "valign": "bottom", "bold":True})
	sheet.write(0, 0, "", header_format)

	# Fill in headers
	sheet.write(0, 1, "DAY", header_format)

	col = 2
	for office in offices:
		column_starts[office] = col
		for i in range(offices[office][1]):
			sheet.write(0, col, office, header_format)
			col += 1

	for off_type in off_columns:
		column_starts[off_type] = col
		for i in range(off_columns[off_type]):
			sheet.write(0, col, off_type, header_format)
			col += 1


	# Fill in days
	cur_date = start_date
	row = 1

	empty_format = wb.add_format({"border": 1})
	date_format = wb.add_format({"bg_color": "#c0c0c0", "align": "right", "valign": "vcenter", "border": 1})
	day_name_format = wb.add_format({"font_name": "Arial", "font_size": 10, "align": "center", "valign": "vcenter", "border": 1})
	provider_format = wb.add_format({"font_name": "Arial", "font_size": 10, "font_color": "#000d7b",
									 "align": "center", "valign": "vcenter", "border": 1})

	weekend_name_format = wb.add_format({"font_name": "Arial", "font_size": 10, "bg_color": "#c0c0c0",
										 "align": "center", "valign": "vcenter", "border": 1})
	weekend_empty_format = wb.add_format({"border": 1, "bg_color": "#c0c0c0"})
	weekend_provider_format = wb.add_format({"font_name": "Arial", "font_size": 10, "font_color": "#000d7b", "bg_color": "#c0c0c0",
									 "align": "center", "valign": "vcenter", "border": 1})

	for week in schedule:
		for day in week:
			sheet.write(row, 0, "{}-{}".format(cur_date.day, months[cur_date.month - 1]), date_format)
			if cur_date.weekday() < 5:
				sheet.write(row, 1, days[cur_date.weekday()], day_name_format)
			else:
				sheet.write(row, 1, days[cur_date.weekday()], weekend_name_format)

			off_providers = providers.copy()

			for office in offices:
				i = 0
				if office in day:
					for provider in day[office]:
						if provider in off_providers:
							off_providers.remove(provider)
						if cur_date.weekday() < 5:
							sheet.write(row, column_starts[office] + i, provider.abbrev, provider_format)
						else:
							sheet.write(row, column_starts[office] + i, provider.abbrev, weekend_provider_format)
						sheet.set_column(column_starts[office] + i, column_starts[office] + i, column_width)
						i += 1
				while i < offices[office][1]:
					if cur_date.weekday() < 5:
						sheet.write(row, column_starts[office] + i, "", empty_format)
					else:
						sheet.write(row, column_starts[office] + i, "", weekend_empty_format)
					i += 1

			vacation_providers = []
			i = 0
			while i < len(off_providers):
				off_provider = off_providers[i]
				if off_provider.check_vacation_date(cur_date):
					vacation_providers.append(off_provider)
					off_providers.remove(off_provider)
				else:
					i += 1

			# for provider in off_providers:
			# 	print(provider, end=" ")
			# print()

			if cur_date.weekday() < 5:
				vacations_per_cell = [len(vacation_providers) // off_columns["VAC"] +
									  (i < len(vacation_providers) % off_columns["VAC"]) for i in range(off_columns["VAC"])]
				idx = 0
				col = column_starts["VAC"]
				for i in range(off_columns["VAC"]):
					sheet.write(row, col, "/".join(map(str, vacation_providers[idx:idx + vacations_per_cell[i]])), provider_format)
					sheet.set_column(col, col, column_width)
					idx += vacations_per_cell[i]
					col += 1

				off_per_cell = [len(off_providers) // off_columns["OFF"] +
								(i < len(off_providers) % off_columns["OFF"]) for i in range(off_columns["OFF"])]
				idx = 0
				col = column_starts["OFF"]
				for i in range(off_columns["OFF"]):
					sheet.write(row, col, "/".join(map(str, off_providers[idx:idx + off_per_cell[i]])), provider_format)
					sheet.set_column(col, col, column_width)
					idx += off_per_cell[i]
					col += 1
			else:
				for i in range(off_columns["VAC"]):
					sheet.write(row, column_starts["VAC"] + i, "", weekend_empty_format)

				for i in range(off_columns["OFF"]):
					sheet.write(row, column_starts["OFF"] + i, "", weekend_empty_format)


			sheet.set_row(row, 19.5)
			row += 1
			cur_date += datetime.timedelta(days=1)

	# FORMATTING
	sheet.set_row(0, 14)

	sheet.set_column(0, 0, 9)
	sheet.set_column(1, 1, 7.3)

	wb.close()

	return filename
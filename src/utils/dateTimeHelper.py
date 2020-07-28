from datetime import datetime


def get_date_string_from_date_time_string(date_time_string):
	return date_time_string[0: date_time_string.index('T')]


def get_date_from_date_time_string(date_time_string):
	return datetime.strptime(get_date_string_from_date_time_string(date_time_string), '%Y-%m-%d')


def get_date_from_date_string(date_string):
	return datetime.strptime(date_string, '%Y-%m-%d')



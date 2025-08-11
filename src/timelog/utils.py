#!/usr/bin/python

import os
from datetime import datetime
import pandas as pd

from tabulate import tabulate




		
def tprint(df, width=80, use_tabulate=False):
	#table = tabulate(df.fillna(''), tablefmt='fancy_grid', headers='keys')
	if use_tabulate:
		#df.loc['Total'] = df['Time'].sum()
		#table = tabulate(df.fillna(''), tablefmt='fancy_grid', headers='keys')
		#table = tabulate(df, tablefmt='fancy_grid', headers='keys')
		table = tabulate(df, tablefmt='fancy_grid')
		#df.to_markdown(headers='keys', tablefmt='psql')
		print(table)
	else:
		df = df.set_index(['Date', 'Category'],inplace=False)
		print('-'*80)
		print(df)
		#print(df.to_string())
		print('-'*80+'\n')

def filter_dates(df, start_date, stop_date):
	if start_date is not None:
		df = df[df['Date'] >= start_date]
	if stop_date is not None:
		df = df[df['Date'] <= stop_date]
	return df

def wrapper(string_value, max_width=30):
	"""Not in use, pandas does not execute line-breaks in std.out"""
	words = string_value.split(' ')
	num_sections = len(string_value)//max_width
	if '\n' in string_value:
		return string_value
	elif (len(string_value) < max_width) or (max_width < 10):
		return string_value
	elif len(words) > num_sections:
		section_length = len(words)//num_sections
		section_strings = [' '.join(words[section_length*(i-1):section_length*i]) for i in range(1,num_sections+1)]
		wrapped_string = '\n'.join(section_strings)
		return wrapped_string

def build_table():
	args_dict = {}
	while True:
		s = input('Enter a key value pair separated by a \':\' to register a value in a column (key):\n')
		if s != '':
			key, values = s.split(':')
			if ',' in values: values = values.split(',')
			else: values = [values]		
			args_dict[key] = values
		else:
			break
	df = pd.DataFrame(args_dict)
	return df


def get_table(path, name, start_date, stop_date):
	if not os.path.isfile(path+name):
		print(f'No table exists in the specified root directory:\n{path}\n')
		p = input(f'Would you like to create a new table called \'{name}\' in this directory? (y/[n])\n')
		if p.lower() in ['y', 'ye', 'yes']:
			table = build_table()
			tprint(table)
			#table.to_csv(path+name, index=False)
			table.to_csv(path+name)

	else:
		table = pd.read_csv(path+name)
		table = filter_dates(table, start_date, stop_date)
		#table = table[table.Date[self.start_date:self.stop_date]]
		table.set_index(['Date', 'Category'],inplace=False)
		#tprint(table)
		return table




if __name__ == '__main__':
	pass
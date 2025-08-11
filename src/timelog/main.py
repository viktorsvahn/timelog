#!/usr/bin/python

import os
from datetime import datetime
import pandas as pd

from tabulate import tabulate

from timelog.parser import argument_parser
args = argument_parser()

from timelog.utils import tprint, filter_dates, build_table, get_table

		
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




class Config:
	def __init__(self):
		script_path = os.getcwd()
		#spath = script_path.split('/')
		#print(spath)

		self.config_path = os.getcwd()+'/'
		print(self.config_path)
		#self.config_path = '../../'
		self.config_fname = 'timelog.conf'
		#print(self.config_path+self.config_fname)
		self.config = self.parse_config(self.config_path+self.config_fname)


	def read_config(self, file):
		config = {}
		#print(f'Using the following config file:\n{file}')
		with open(file, 'r') as f:
			for line in f:
				variable, value = line.split(':'); value = value.strip()
				config[variable] = value
		#print(config)
		return config

	def save_config(self, file, args):
		with open(file, 'w') as f:
			for key, value in args.items():
				print(key,value)
				if value.isnumeric():
					f.write(f'{key}:  {value}')
				else:
					f.write(f'{key}:  \'{value}\'')
		f.close()

	def parse_config(self, file):
		if os.path.isfile(file):
			#print('hoppla')
			#print(file)
			config = self.read_config(file)
			#print(config)
			for key, val in config.items():
				key = key.replace(' ', '_')
				if val.isnumeric():
					if '.' in val:
						exec(f'self.{key} = {float(val)}')
					else:
						exec(f'self.{key} = {int(val)}')
				else:
					exec(f'self.{key} = \'{val}\'')
			#print(self.root)
			return config
		else:
			print('Could not locate a config file.')
			self.root = input('Please specify a root-directory for the time table:\n')
			self.vacation_days = input('Please specify the number of vacation days per year:\n')
			self.table_name = input('Please specify the name of the time table file:\n')
			config = {
				'root':self.root,
				'vacation_days':self.vacation_days,
				'table name':self.table_name,
			}
			self.save_config(file, config)
		return self.root



class Schema(Config):
	def __init__(self, start_date, stop_date, fname=None, *args):
		super().__init__(*args)
		self.start_date = start_date
		self.stop_date = stop_date
		if 'table name' in self.config:
			self.fname = self.config['table name']
		else:
			self.fname = fname

		self.table = get_table(self.root, self.fname, self.start_date, self.stop_date)
		self.date = datetime.today().strftime('%Y-%m-%d')

	
	def filter(self, category):
		table = self.table[self.table.Category == category]
		if len(table) == 0:
			categories = set(self.table.Category)
			print(f'The specified category \'{category}\' is not part of the table.')
			print('\nPlease choose one of the following:')
			for c in categories:
				print(f'  {c}')
			quit()
		else:
			tprint(table)


	def add_entry(self, time_spent, category, note, date=None):
		"""Use the following order:
			time_spent, category, note, date=None
		"""
		#table = self.table.set_index(['Date', 'Category'],inplace=False)
		#print(table, table.index)
		#print(self.table)
		if date is None: date = self.date
		
		self.table.loc[-1] = [date, category, time_spent, note]
		#self.table[(self.table['Date'] == date) & (self.table['Category'] == category)] = [time_spent, note]
		#self.table.loc[date] = [time_spent, category, note]
		#self.table[[date, category]] = [time_spent, note]
		#self.table.loc[(date,category),:] = [time_spent, note]
		#table.loc[(date,category),:] = [time_spent, note]
		#table.loc[(date,category),:] = [time_spent, note]

		#tprint(self.table)
		self.table.to_csv(self.root+self.fname, index=False)

	def remove_entry(self, date, category):
		selection = self.table[(self.table.Date == date) & (self.table.Category == category)]	
		if len(selection) > 1:
			print(selection)
			print('\nThere exists multiple entries with the same date and category.\n')
			s = int(input('Select the index of the entry you wish to delete: '))
			while True:
				if s in selection.index:
					break
				else:
					print('Invalid index, closing.')
					quit()
		else:
			s = selection.index[0]

		print(f'\nAttempting to delete the following entry:\n')
		print(selection.loc[s])
		t = input('\nAre you sure? (y/N): ')
		if t.lower() in ['y', 'ye', 'yes']:
			self.table.drop(s, inplace=True)
			tprint(self.table)
			self.table.to_csv(self.root+self.fname, index=False)
		else:
			print('Closing')
			quit()


	def results(self, start_date, stop_date, column='Category'):
		if start_date is None:
			#start_date = self.table.index.min()[0]
			start_date = min(self.table.Date)
		if stop_date is None:
			#stop_date  = self.table.index.max()#[0]
			stop_date = max(self.table.Date)

		start = datetime.strptime(start_date, "%Y-%m-%d").date()
		stop = datetime.strptime(stop_date, "%Y-%m-%d").date()
		
		for col, grp in self.table.groupby(column):
			print(f'\nResults from time spent on \'{col}\' between {start_date} and {stop_date}:')
			column_total = grp['Time'].to_numpy().sum()
			time_span = (stop-start).days + 1
			working_hrs_per_day = ((5*52-self.vacation_days)*8)/365
			working_hrs = time_span*working_hrs_per_day # This should account for weekends
			rate = column_total/working_hrs*100
			
			# aggregate results
			results = {
				'Total time':round(column_total),
				'Avg. working hrs*':round(working_hrs),
				'Rate':round(rate,2),
			}
			res_df = pd.DataFrame.from_dict(results, columns=['Result'], orient='index')
			res_df['Unit'] = ['hrs', 'hrs', '%']
			tprint(res_df, use_tabulate=True)
		print('\n*Average working hours takes into account the number of weekends and')
		print(' vacation days per year so it is an average per day per year.')
		print(' The longer the time span the more reliable this estimate becomes.')



	
def main():
	if args.start: start_date = args.start
	else: start_date = None
	if args.stop: stop_date = args.stop
	else: stop_date = None
	schema = Schema(start_date, stop_date)


	if args.add:
		if len(args.add) == 4:
			time_spent, category, note, date = args.add
		elif len(args.add) == 3:
			time_spent, category, note = args.add
			date = None
		else:
			print('Not enough parameters given.')
			print('\nPlease include the following arguments:')
			print('  time spent (hours)\n  category\n  short description\n  date (optional)')
			quit()
		
		schema.add_entry(
			float(time_spent),
			category,
			note,
			date,
		)

	elif args.show:
		date_selection = schema.table[schema.table.Date == args.show]
		print(date_selection.to_string())

	elif args.delete:
		if len(args.delete) == 2:
			date, category = args.delete
			schema.remove_entry(date, category)
		else:
			print('Incorrect number of parameters specified.')
			print('\nPlease include the following arguments:')
			print('  category\n  date')
			quit()
	
	elif args.category:
		schema.filter(args.category)

	elif args.results:
		if stop_date is None:
			stop_date = schema.date
		schema.results(start_date, stop_date, 'Category')

	else:
		tprint(schema.table)



if __name__ == '__main__':
	main()
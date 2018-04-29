#!/usr/bin/env python3
import os
import datetime
import math

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import stats
import pandas as pd

def csv_to_df(file_path, col_names, col_types, col_converters):
	df = pd.read_csv(file_path,
		delimiter=',',
		header='infer', # read col names from file itself
		names=None, # since 'infer' is used above
		usecols=col_names,
		dtype=col_types,
		converters=col_converters,
		true_values=['TRUE'],
		false_values=['FALSE'],
		skipinitialspace=True,
		nrows=NUM_ROWS
	)
	# create more columns
	# df['year'] = [
	# 	date.year for date in df['stop_date']
	# ]
	return df

def init_dataframes():
	""" Takes in file path and creates dataframe with only the info we want. """
	# import data
	# col names we need, (subset of col_names_full)
	col_names = [
		'Pts',
		'PtsAfter',
		'isAce',
	]
	# the data type of each column
	col_types = {
		'isAce': bool,
	}
	# the data cleaners for select columns
	# NONE_VALUES = ['', 'NON-', 'UNK']
	def convert_score(score):
		if score == 'GM':
			return [0, 0]
		split_scores = score.split('-')
		if len(split_scores) != 2:
			return None
		lscore, rscore = split_scores
		score_to_int = {
			'0': 0,
			'15': 1,
			'30': 2,
			'40': 3,
			'AD': 4,
			# '1': 1,
			# '2': 2,
			# '3': 3,
			# '4': 4,
		}
		if lscore not in score_to_int or rscore not in score_to_int:
			return None
		return [score_to_int[lscore], score_to_int[rscore]]
	col_converters = {
		'Pts': convert_score,
		'PtsAfter': convert_score,
	}
	df = csv_to_df(FILE_PATH, col_names, col_types, col_converters)
	# df = pd.concat([df_VT, df_MT])
	return df

def score_to_str(score):
	point_to_str = {
		0: '0',
		1: '15',
		2: '30',
		3: '40',
		4: 'AD',
	}
	return '{}-{}'.format(point_to_str[score[0]], point_to_str[score[1]])

def is_won_point(score, scoreAfter):
	""" from the *server*'s perspective """
	if score[0] in (3, 4) and scoreAfter == [0, 0]:
		return True
	elif score[0] < scoreAfter[0]:
		return True
	else:
		return False

def score_to_win_percent(df):
	""" 's' is short for 'score' in this function """
	# score --> [num_wins_next_pt, num_losses_next_pt]
	s_to_win_lose = dict()
	for s, sA in zip(df['Pts'], df['PtsAfter']):
		if s is None or sA is None:
			continue
		s_str = score_to_str(s)
		is_won = is_won_point(s, sA)
		if s_str not in s_to_win_lose:
			s_to_win_lose[s_str] = [0, 0]
		if is_won:
			s_to_win_lose[s_str][0] += 1
		else:
			s_to_win_lose[s_str][1] += 1
	s_to_win_percent = {
		s:(win/(win+lose)) for s,[win,lose] in s_to_win_lose.items()
	}
	return s_to_win_percent

def score_to_ace_percent(df):
	""" 's' is short for 'score' in this function """
	# score --> [num_aces, num_non_aces]
	s_to_ace_noace = dict()
	for s, is_ace in zip(df['Pts'], df['isAce']):
		if s is None or is_ace is None:
			continue
		s_str = score_to_str(s)
		if s_str not in s_to_ace_noace:
			s_to_ace_noace[s_str] = [0, 0]
		if is_ace:
			s_to_ace_noace[s_str][0] += 1
		else:
			s_to_ace_noace[s_str][1] += 1
	s_to_ace_percent = {
		s:(ace/(ace+noace)) for s,[ace,noace] in s_to_ace_noace.items()
	}
	return s_to_ace_percent

def show_bar_graph(dic, yname):
	categories = dic.keys()
	y_pos = np.arange(len(categories))
	values = [dic[x] for x in categories]

	plt.bar(y_pos, values, align='center', alpha=0.5)
	plt.xticks(y_pos, categories)
	plt.ylabel('{} probability'.format(yname))
	plt.title('Score to {} probability'.format(yname))

	plt.show()

if __name__ == '__main__':
	# MT = Montana, VT = Vermont
	FILE_PATH = 'tennis_MatchChartingProject/charting-m-points.csv'
	NUM_ROWS = 202
	df = init_dataframes()
	print([
		# area_largest_MT_county(df_MT),
	])
	dic = score_to_ace_percent(df)
	show_bar_graph(dic, 'ace')




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

# HELPERS
def player_to_initials(pl):
	# pl is a player such as "Sam_Querrey"
	first, last = pl.split('_')
	return first[0] + last[0]

# DATAFRAME
def csv_to_df(file_path, col_names, col_types, col_converters):
	df = pd.read_csv(file_path,
		encoding='utf_8',
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
	def id_to_info(id_):
		date, gender, location, _, player1, player2 = id_.split('-')
		return [date, gender, location, _, player1, player2]
	df['player1'] = [
		id_to_info(id_)[4] for id_ in df['match_id']
	]
	df['player2'] = [
		id_to_info(id_)[5] for id_ in df['match_id']
	]
	return df

def init_dataframes():
	""" Takes in file path and creates dataframe with only the info we want. """
	# import data
	# col names we need, (subset of col_names_full)
	col_names = [
		'match_id',
		'Svr', # server player number (1 or 2)
		'Ret', # returner player number
		'Serving', # server's initials
		'Pts',
		'isAce',
		'isDouble',
		'isSvrWinner',
		'GmW',
		'SetW',
	]
	# the data type of each column
	col_types = {
		'match_id': str,
		'Serving': str,
		'isAce': bool,
		'isSvrWinner': bool,
	}
	# the data cleaners for select columns
	# NONE_VALUES = ['', 'NON-', 'UNK']
	def convert_player_num(s):
		if s == '1':
			return 1
		elif s == '2':
			return 2
		else:
			return 0
	def convert_double(s):
		if s == 'TRUE':
			return True
		elif s == 'FALSE':
			return False
		else:
			return False
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
		'isDouble': convert_double,
		'Svr': convert_player_num,
		'Ret': convert_player_num,
		'GmW': convert_player_num,
		'SetW': convert_player_num,
	}
	df = csv_to_df(FILE_PATH, col_names, col_types, col_converters)
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

def momentum_count(df):
	""" when a player wins a set, count if they win the next game """
	# [momentum_games, total_games]
	momentum_count = [0, 0]
	prev_set_w = None
	for game_w, set_w, ret in zip(df['GmW'], df['SetW'], df['Ret']):
		if prev_set_w is None:
			# find out who wins the set
			if set_w == 0:
				continue
			else:
				prev_set_w = set_w
		else:
			# find out who wins the game following the set,
			# but ONLY if they are returning
			# if ret != prev_set_w:
				# prev_set_w = None
				# continue
			if game_w == 0:
				continue
			else:
				# if game_w == prev_set_w:
				if game_w == ret:
					momentum_count[0] += 1
				else:
					pass
				momentum_count[1] += 1
				prev_set_w = None
	return momentum_count

def score_to_bool_count(df, other_name, is_yes_converter=lambda s, other_datum: other_datum):
	""" 's' is short for 'score' in this function """
	# score --> [num_yes, num_no]
	s_to_yes_no = dict()
	for s, other_datum in zip(df['Pts'], df[other_name]):
		if s is None or other_datum is None:
			continue
		is_yes = is_yes_converter(s, other_datum)
		s_str = score_to_str(s)
		if s_str not in s_to_yes_no:
			s_to_yes_no[s_str] = [0, 0]
		if is_yes:
			s_to_yes_no[s_str][0] += 1
		else:
			s_to_yes_no[s_str][1] += 1
	return s_to_yes_no

def score_to_bool_probability(df, other_name, is_yes_converter=lambda s, other_datum: other_datum):
	s_to_yes_no = score_to_bool_count(df, other_name, is_yes_converter)
	s_to_yes_probability = {
		s:(yes/(yes+no)) for s,[yes,no] in s_to_yes_no.items()
	}
	return s_to_yes_probability

def player_serving_filter(df, player):
	df_player = df[
		(df['player1'] == player) | (df['player2'] == player)
	]
	df_player_serving = df_player[
		df_player['Serving'] == player_to_initials(player)
	]
	return df_player_serving

def chi_square(df, obj):
	""" let's first try the chi_square for score-to-win situation, all rows """
	# we find the TOTAL point wins and point losses.  This allows us to calculate the EXPECTED point wins and losses in the 'score' situation
	if isinstance(obj, dict):
		score_to_yes_no_count = obj
	elif isinstance(obj, str):
		score_to_yes_no_count = score_to_bool_count(df, obj)
	else:
		raise ValueError('obj can be a score_to_yes_no_count dictionary or a column label of what to count.')

	total_yes = sum(yes_no[0] for yes_no in score_to_yes_no_count.values())
	total_no = sum(yes_no[1] for yes_no in score_to_yes_no_count.values())
	total_count = total_yes + total_no
	expected_yes_percent = total_yes / total_count
	expected_no_percent = total_no / total_count

	# observed
	observed_yes = score_to_yes_no_count[SCORE_OF_INTEREST][0]
	observed_no = score_to_yes_no_count[SCORE_OF_INTEREST][1]
	observed_count = observed_yes + observed_no

	# expected
	expected_yes = observed_count * expected_yes_percent
	expected_no = observed_count * expected_no_percent

	# run the chi square
	chisq, p = sp.stats.chisquare(
		[
			observed_yes,
			observed_no,
		],
		f_exp=[
			expected_yes,
			expected_no,
		]
	)
	return chisq, p

def plot_bar_graph(dic, yname):
	# categories = sorted(dic.keys())
	categories = ['0-40', '15-40', '0-30', '40-AD', '30-40', '15-30', '0-15', '40-40', '30-30', '15-15', '0-0', '15-0', '30-15', '40-30', 'AD-40', '30-0', '40-15', '40-0']
	y_pos = np.arange(len(categories))
	values = [dic[x] for x in categories]

	bar_list = plt.bar(y_pos, values, align='center', alpha=0.5)
	(bar.set_color('r') for bar in bar_list)
	plt.xticks(y_pos, categories)
	plt.ylabel(PLOT_V_AXIS_TITLE)
	plt.title(PLOT_TITLE)


if __name__ == '__main__':
	FILE_PATH = 'charting-m-points.csv'
	NUM_ROWS = None
	SCORE_OF_INTEREST = '40-0'
	PLAYER = 'Sam_Querrey' # use "_"
	PLOT_TITLE = "Sam Querrey's score to ace/double-fault probability"
	PLOT_V_AXIS_TITLE = "probability of ace/double-fault"

	df = init_dataframes()
	df_server = player_serving_filter(df, PLAYER)
	chisq, p = chi_square(df_server, 'isAce')
	print([
		chisq,
		p,
		# momentum_count(df),
	])

	dic = score_to_bool_probability(df_server, 'isAce')
	plot_bar_graph(dic, PLOT_TITLE)
	dic = score_to_bool_probability(df_server, 'isDouble')
	plot_bar_graph(dic, '')
	plt.show()



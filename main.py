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
		'isSvrWinner',
	]
	# the data type of each column
	col_types = {
		'isAce': bool,
		'isSvrWinner': bool,
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

def score_to_win_probability(df):
	return score_to_bool_probability(df, 'isSvrWinner')

def score_to_ace_probability(df):
	return score_to_bool_probability(df, 'isAce')

def chi_square(df, score_to_yes_no_count):
	""" let's first try the chi_square for score-to-win situation, all rows """
	# we find the TOTAL point wins and point losses.  This allows us to calculate the EXPECTED point wins and losses in the 'score' situation
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

def win_chi_square(df):
	dic = score_to_bool_count(df, 'isSvrWinner')
	return chi_square(df, dic)

def ace_chi_square(df):
	dic = score_to_bool_count(df, 'isAce')
	return chi_square(df, dic)

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
	FILE_PATH = 'tennis_MatchChartingProject/charting-m-points.csv'
	NUM_ROWS = 202
	SCORE_OF_INTEREST = '15-40'

	df = init_dataframes()
	chisq, p = ace_chi_square(df)
	dic = score_to_ace_probability(df)
	print([
		chisq,
		p,
	])
	show_bar_graph(dic, 'ace')




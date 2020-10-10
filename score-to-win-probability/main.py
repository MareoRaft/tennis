#!/usr/bin/env python3
import os
import time
import datetime
import math
import collections

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import stats

from data_ingestion import init_dataframes

# HELPERS
def player_to_initials(pl):
	# pl is a player such as "Sam_Querrey"
	first, last = pl.split('_')
	return first[0] + last[0]

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

def is_server_game_winner(df, i, games_to_skip=0):
	""" given a dataframe and a row index, see if the server won the NEXT...NEXT game (games_to_skip times) """
	server = df['Svr'][i]
	while True:
		# go to end of game
		while i in range(0, len(df)) and df['GmW'][i] == 0:
			i += 1
		# check for end of data
		if i not in range(0, len(df)):
			return None
		# skip game
		if games_to_skip > 0:
			i += 1
			games_to_skip -= 1
		else:
			break
	# check for end of data
	if i not in range(0, len(df)):
		return None
	# see if server won
	game_winner = df['GmW'][i]
	return server == game_winner

def deuce_count(df):
	num_won, num_total = (0, 0)
	df_pts = df['Pts']
	def is_deuce(i):
		return i in range(0, len(df_pts)) and df_pts[i] is not None and df_pts[i][0] == df_pts[i][1] == 3
	def is_four_deuces(i):
		return all(is_deuce(index) for index in range(i, i+4*2, 2))
	for i in range(0, len(df)):
		did_server_win = is_server_game_winner(df, i)
		did_server_win_after = is_server_game_winner(df, i, games_to_skip=2)
		if is_four_deuces(i) and did_server_win is not None and did_server_win_after is not None:
			if not did_server_win:
				# situation where server lost 4+ deuce game
				num_total += 1
				if did_server_win_after:
					num_won += 1
	return num_won, num_total

def server_count(df):
	""" count how many times the server wins the game """
	num_won, num_total = (0, 0)
	for i in range(0, len(df)):
		if df['GmW'][i] == 0:
			continue
		else:
			num_total += 1
			if is_server_game_winner(df, i):
				num_won += 1
	return num_won, num_total

def score_to_bool_count(df, other_name, is_yes_converter=lambda s, other_datum: other_datum):
	""" 's' is short for 'score' in this function """
	# score --> [num_yes, num_no]
	s_to_yes_no = collections.defaultdict(lambda: [0, 0])
	for s, other_datum in zip(df['Pts'], df[other_name]):
		if s is None or other_datum is None:
			continue
		is_yes = is_yes_converter(s, other_datum)
		s_str = score_to_str(s)
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
	NUM_ROWS = 800
	SCORE_OF_INTEREST = '0-30'
	PLAYER = 'Roger_Federer' # use "_"
	PLOT_TITLE = "Roger Federer's score to ace/double-fault probability"
	PLOT_V_AXIS_TITLE = "probability of ace/double-fault"

	df = init_dataframes(FILE_PATH, NUM_ROWS)
	df_server = player_serving_filter(df, PLAYER)
	start_time = time.time()
	print('data loaded.  crunching numbers...')
	num_won, num_total = deuce_count(df)
	chisq, p = chi_square(df_server, 'isAce')
	print([
		chisq,
		p,
		num_won,
		num_total,
		num_won / num_total,
		# momentum_count(df),
	])

	dic = score_to_bool_probability(df_server, 'isAce')
	plot_bar_graph(dic, PLOT_TITLE)
	dic = score_to_bool_probability(df_server, 'isDouble')
	plot_bar_graph(dic, '')
	plt.show()

	print('Finished crunching numbers.', end='')
	end_time = time.time()
	elapsed_time = end_time - start_time
	print(' Elapsed time = {}'.format(elapsed_time))


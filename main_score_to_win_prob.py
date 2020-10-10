#!/usr/bin/env python3
import time

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np

from data_ingestion.ingest_points import init_dataframes
import analysis.score_to_win_prob as a


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
	FILE_PATH = './tennis_MatchChartingProject/charting-m-points.csv'
	NUM_ROWS = 800
	SCORE_OF_INTEREST = '0-30'
	PLAYER = 'Roger_Federer' # use "_"
	PLOT_TITLE = "Roger Federer's score to ace/double-fault probability"
	PLOT_V_AXIS_TITLE = "probability of ace/double-fault"

	df = init_dataframes(FILE_PATH, NUM_ROWS)
	df_server = a.player_serving_filter(df, PLAYER)
	start_time = time.time()
	print('data loaded.  crunching numbers...')
	num_won, num_total = a.deuce_count(df)
	chisq, p = a.chi_square(df_server, 'isAce', SCORE_OF_INTEREST)
	print([
		chisq,
		p,
		num_won,
		num_total,
		num_won / num_total,
		# momentum_count(df),
	])

	dic = a.score_to_bool_probability(df_server, 'isAce')
	plot_bar_graph(dic, PLOT_TITLE)
	dic = a.score_to_bool_probability(df_server, 'isDouble')
	plot_bar_graph(dic, '')
	plt.show()

	print('Finished crunching numbers.', end='')
	end_time = time.time()
	elapsed_time = end_time - start_time
	print(' Elapsed time = {}'.format(elapsed_time))


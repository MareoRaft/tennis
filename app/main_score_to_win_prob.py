#!/usr/bin/env python3
import time


from data_ingestion.ingest_points import init_dataframe
from output.score_to_win_prob import plot_bar_graph, plot_bar_graphs
import analysis.score_to_win_prob as a



if __name__ == '__main__':
	FILE_PATH = './data/charting-m-points.csv'
	NUM_ROWS = 800
	SCORE_OF_INTEREST = '0-30'
	PLAYER = 'Roger_Federer' # use "_"

	df = init_dataframe(FILE_PATH, NUM_ROWS)
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

	plot_bar_graphs([
		a.score_to_bool_probability(df_server, 'isAce'),
  	a.score_to_bool_probability(df_server, 'isDouble'),
  ])

	print('Finished crunching numbers.', end='')
	end_time = time.time()
	elapsed_time = end_time - start_time
	print(' Elapsed time = {}'.format(elapsed_time))


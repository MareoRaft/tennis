#!/usr/bin/env python3
import time

import numpy as np

from data_ingestion.ingest_points import init_dataframes
import analysis.player_rank as a


if __name__ == '__main__':
	FILE_PATH = './tennis_MatchChartingProject/charting-m-points.csv'
	NUM_ROWS = 2000

	# ingest
	df = init_dataframes(FILE_PATH, NUM_ROWS)
	start_time = time.time()
	print('data loaded.  crunching numbers...')

	# make graph
	graph = a.init_weighted_graph(df)
	pagerank_list = a.pagerank(df)

	# output
	print('graph size:', graph.size())
	print('top pagerank:', pagerank_list[:4])
	# print('Finished crunching numbers.', end='')
	# end_time = time.time()
	# elapsed_time = end_time - start_time
	# print(' Elapsed time = {}'.format(elapsed_time))


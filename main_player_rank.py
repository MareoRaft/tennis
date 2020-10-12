#!/usr/bin/env python3
import time

import numpy as np
import networkx as nx

from data_ingestion.ingest_points import init_dataframes
import analysis.player_rank as a


if __name__ == '__main__':
	FILE_PATH = './tennis_MatchChartingProject/charting-m-points.csv'
	NUM_ROWS = None # charting-m-points has 297532 lines # A value of None will get them all

	# ingest
	df = init_dataframes(FILE_PATH, NUM_ROWS)
	start_time = time.time()
	print('data loaded.  crunching numbers...')

	# analyze
	graph = a.init_weighted_graph(df)
	# pagerank_list = a.pagerank(graph)
	arborescense = nx.maximum_spanning_arborescence(graph)

	# outgest (convert to output data structure for frontend)
	# uf_tree =

	# output
	print('graph size:', graph.size())
	print('arbor:', arborescense)
	print('Finished crunching numbers.', end='')
	end_time = time.time()
	elapsed_time = end_time - start_time
	print(' Elapsed time = {}'.format(elapsed_time))


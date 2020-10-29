#!/usr/bin/env python3
import time

import numpy as np
import networkx as nx

from data_ingestion.ingest_points import init_dataframe
from analysis import pagerank as a


def main(gender, limit, verbose=False):
	FILE_NAME = f'charting-{gender}-points.csv'
	# charting-m-points has 297532 lines # A value of None will get them all
	NUM_ROWS = None

	# ingest
	df = init_dataframe(FILE_NAME, NUM_ROWS)
	if verbose:
		start_time = time.time()
		print('data loaded.  crunching numbers...')

	# analyze
	graph = a.init_weighted_graph(df, gender)
	pagerank_list = a.pagerank(graph, limit)

	# outgest (convert to output data structure for frontend)
	frontend_pagerank_list = [{'category': player, 'value': score} for player,score in pagerank_list]

	# output
	if verbose:
		end_time = time.time()
		elapsed_time = end_time - start_time
		print(' Elapsed time = {}'.format(elapsed_time))
	return frontend_pagerank_list

if __name__ == '__main__':
	gender = 'm'
	pr = main(gender, 5, verbose=True)
	print('gender:', gender, 'pagerank:\n', pr, '\n')
	print('Finished crunching numbers.', end='')


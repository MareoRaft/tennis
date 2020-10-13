#!/usr/bin/env python3
import time

import numpy as np
import networkx as nx

from data_ingestion.ingest_points import init_dataframe
from analysis import pagerank as a


def main(verbose=False):
	FILE_PATH = './data/charting-m-points.csv'
	NUM_ROWS = None # charting-m-points has 297532 lines # A value of None will get them all

	# ingest
	df = init_dataframe(FILE_PATH, NUM_ROWS)
	if verbose:
		start_time = time.time()
		print('data loaded.  crunching numbers...')

	# analyze
	graph = a.init_weighted_graph(df)
	pagerank_list = a.pagerank(graph)

	# outgest (convert to output data structure for frontend)
	frontend_pagerank_list = [{'category': player, 'value1': score} for player,score in pagerank_list]

	# output
	if verbose:
		end_time = time.time()
		elapsed_time = end_time - start_time
		print(' Elapsed time = {}'.format(elapsed_time))
	return frontend_pagerank_list

if __name__ == '__main__':
	pr = main(verbose=True)
	print('pagerank:', pr)
	print('Finished crunching numbers.', end='')


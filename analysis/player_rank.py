import collections

import scipy as sp
from scipy import stats
import networkx as nx
import numpy as np

def row_to_loser_winner_pair(row):
  if row['PtWinner'] == 1:
    return (row['player1'], row['player2'])
  elif row['PtWinner'] == 2:
    return (row['player2'], row['player1'])
  else:
    raise ValueError(f"unexpected point winner value {row['PtWinner']}")

def init_weighted_graph(df):
  # for each row in df (which represents a match), create an edge from losing player to winning player
  df_ = df[['player1', 'player2', 'PtWinner']]
  loser_winner_pairs = [row_to_loser_winner_pair(row) for _,row in df_.iterrows()]
  lower_winner_pair_to_weight = collections.Counter(loser_winner_pairs)
  graph = nx.DiGraph()
  for pp,weight in lower_winner_pair_to_weight.items():
    graph.add_edge(pp[0], pp[1], weight=weight)
  return graph

def pagerank(df):
  # nx uses alpha=0.85 as the default damping parameter
  # nx pagerank does not work on multi graphs.  We must feed it a weighted graph.
  # by default, if edges have a 'weight' key, they will be used as weights in the PageRank algo.
  graph = init_weighted_graph(df)
  pagerank_dict = nx.pagerank(graph)
  top_pagerank_list = sorted(pagerank_dict.items(), key=lambda item: item[1], reverse=True)[:10]
  return top_pagerank_list

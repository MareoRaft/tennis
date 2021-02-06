import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()


def plot_bar_graph(dic):
  PLOT_TITLE = "score to ace/double-fault probability"
  PLOT_V_AXIS_TITLE = "probability of ace/double-fault"
  # categories = sorted(dic.keys())
  categories = ['0-40', '15-40', '0-30', '40-AD', '30-40', '15-30', '0-15', '40-40', '30-30', '15-15', '0-0', '15-0', '30-15', '40-30', 'AD-40', '30-0', '40-15', '40-0']
  y_pos = np.arange(len(categories))
  values = [dic[x] for x in categories]

  bar_list = plt.bar(y_pos, values, align='center', alpha=0.5)
  (bar.set_color('r') for bar in bar_list)
  plt.xticks(y_pos, categories)
  plt.ylabel(PLOT_V_AXIS_TITLE)
  plt.title(PLOT_TITLE)

def plot_bar_graphs(dicts):
  for dict_ in dicts:
    plot_bar_graph(dict_)
  plt.show()

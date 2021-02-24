import pandas as pd

# constant term added to denominator of all time-decay percentages to penalize players who haven't played in a long time
PENALTY = 2.9

NORMALIZATION_TO_COL_SYMBOL = {
  'count': '#',
  'percent': '%',
  'time-decay': '%w',
}


def get_stat_df(df, group_by_col, agg_col, new_stat_col):
  # aggregate
  agg = {}
  agg[agg_col] = 'sum'
  df_stat = df.groupby([group_by_col], as_index=False).agg(agg)
  # rename columns
  columns = {}
  columns[group_by_col] = 'player'
  columns[agg_col] = new_stat_col
  df_stat.rename(columns=columns, inplace=True)
  return df_stat


def player_to_stats_df(df):
  ''' Given the point dataframe, output a [(player,num_stat),...] ranking. '''

  # calculate various stats
  df_service_wins = get_stat_df(df, group_by_col='playerPtWinner', agg_col='isSvrWinner', new_stat_col='svcPtWin#')
  df_points_won = get_stat_df(df, group_by_col='playerPtWinner', agg_col='isPt', new_stat_col='ptWin#')
  df_points_lost = get_stat_df(df, group_by_col='playerPtLoser', agg_col='isPt', new_stat_col='ptLoss#')
  df_aces = get_stat_df(df, group_by_col='playerPtWinner', agg_col='isAce', new_stat_col='ace#')
  df_double_faults = get_stat_df(df, group_by_col='playerPtLoser', agg_col='isDouble', new_stat_col='dblFault#')

  # create player stat dataframe
  df_player = pd.merge(df_points_won, df_points_lost, on='player')
  # v weighted
  # df_player['pt#w'] = df_player['ptWin#w'] + df_player['ptLoss#w']
  # df_player['ptWin%w'] = df_player['ptWin#w'] / (df_player['pt#w'] + PENALTY)
  # ^ weighted
  df_player['pt#'] = df_player['ptWin#'] + df_player['ptLoss#']
  df_player['ptWin%'] = df_player['ptWin#'] / df_player['pt#']
  df_player['svcPtWin#'] = df_service_wins['svcPtWin#']
  df_player['svcPtWin%'] = df_player['svcPtWin#'] / df_player['pt#']
  df_player['ace#'] = df_aces['ace#']
  df_player['ace%'] = df_player['ace#'] / df_player['pt#']
  df_player['dblFault#'] = df_double_faults['dblFault#']
  df_player['dblFault%'] = df_player['dblFault#'] / df_player['pt#']

  # restrict it to players where we have a reasonable amount of data
  df_player_enough_data = df_player[df_player['pt#'] >= 400]
  # print('df_player_enough_data:', df_player_enough_data[['player', 'ptWin%', 'ptWin%w']])
  return df_player_enough_data


def player_to_stat(df, stat, normalization, reverse, limit, verbose=False):
  ''' `df` is the player_to_stats dataframe. '''
  if verbose:
    print('normalization:', normalization)
  normalization_col_symbol = NORMALIZATION_TO_COL_SYMBOL[normalization]
  stat_col = f'{stat}{normalization_col_symbol}'
  if verbose:
    print('stat_col:', stat_col)
  df_player_to_stat = df[['player', stat_col]]
  # take the 'top 10' or so
  top_player_to_stat = df_player_to_stat.nsmallest(limit, stat_col) if reverse else df_player_to_stat.nlargest(limit, stat_col)
  # convert to a list
  list_player_to_stat = [(row['player'],row[stat_col]) for index,row in top_player_to_stat.iterrows()]
  return list_player_to_stat


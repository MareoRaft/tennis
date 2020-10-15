import pandas as pd

NORMALIZATION_TO_COL_SYMBOL = {
  'count': '#',
  'percent': '%',
}


def player_to_stats_df(df):
  ''' Given the point dataframe, output a [(player,num_stat),...] ranking. '''

  # calculate various stats
  df_service_wins = df.groupby(['playerPtWinner'], as_index=False).agg({'isSvrWinner': 'sum'})
  df_service_wins.rename(columns={'playerPtWinner':'player', 'isSvrWinner':'svcPtWin#'}, inplace=True)

  df_points_won = df.groupby(['playerPtWinner'], as_index=False).agg({'isPt': 'sum'})
  df_points_won.rename(columns={'playerPtWinner':'player', 'isPt':'ptWin#'}, inplace=True)

  df_points_lost = df.groupby(['playerPtLoser'], as_index=False).agg({'isPt': 'sum'})
  df_points_lost.rename(columns={'playerPtLoser':'player', 'isPt':'ptLoss#'}, inplace=True)

  df_ace = df.groupby(['playerPtWinner'], as_index=False).agg({'isAce': 'sum'})
  df_ace.rename(columns={'playerPtWinner':'player', 'isAce':'ace#'}, inplace=True)

  df_double_faults = df.groupby(['playerPtLoser'], as_index=False).agg({'isDouble': 'sum'})
  df_double_faults.rename(columns={'playerPtLoser':'player', 'isDouble':'dblFault#'}, inplace=True)

  # create player stat dataframe
  df_player = pd.merge(df_points_won, df_points_lost, on='player')
  df_player['pt#'] = df_player['ptWin#'] + df_player['ptLoss#']
  df_player['ptWin%'] = df_player['ptWin#'] / df_player['pt#']
  df_player['svcPtWin#'] = df_service_wins['svcPtWin#']
  df_player['svcPtWin%'] = df_player['svcPtWin#'] / df_player['pt#']
  df_player['ace#'] = df_ace['ace#']
  df_player['ace%'] = df_player['ace#'] / df_player['pt#']
  df_player['dblFault#'] = df_double_faults['dblFault#']
  df_player['dblFault%'] = df_player['dblFault#'] / df_player['pt#']

  # restrict it to players where we have a reasonable amount of data
  df_player_enough_data = df_player[df_player['pt#'] >= 400]

  return df_player_enough_data


def player_to_stat(df, stat, normalization, limit):
  ''' `df` is the player_to_stats dataframe. '''
  normalization_col_symbol = NORMALIZATION_TO_COL_SYMBOL[normalization]
  stat_col = f'{stat}{normalization_col_symbol}'
  df_player_to_stat = df[['player', stat_col]]
  # take the 'top 10' or so
  top_player_to_stat = df_player_to_stat.nlargest(limit, stat_col)
  # convert to a list
  list_player_to_stat = [(row['player'],row[stat_col]) for index,row in top_player_to_stat.iterrows()]
  return list_player_to_stat


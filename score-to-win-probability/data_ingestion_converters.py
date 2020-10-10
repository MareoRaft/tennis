# Convert data from CSV file to the value we want.

def player_num(s):
  if s == '1':
    return 1
  elif s == '2':
    return 2
  else:
    return 0

def double_fault(s):
  if s == 'TRUE':
    return True
  elif s == 'FALSE':
    return False
  else:
    return False

def score(score):
  if score == 'GM':
    return [0, 0]
  split_scores = score.split('-')
  if len(split_scores) != 2:
    return None
  lscore, rscore = split_scores
  score_to_int = {
    '0': 0,
    '15': 1,
    '30': 2,
    '40': 3,
    'AD': 4,
  }
  if lscore not in score_to_int or rscore not in score_to_int:
    return None
  return [score_to_int[lscore], score_to_int[rscore]]

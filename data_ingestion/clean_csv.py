import os

def get_output_file_path(file_path):
  ''' For example, given an input of 'data.csv', return 'data.clean.csv'. '''
  root, ext = os.path.splitext(file_path)
  out_file_path = f'{root}.clean{ext}'
  return out_file_path

def remove_non_utf_8_chars(file_path):
  file_str = open(file_path, 'r', encoding='utf8', errors='ignore').read()
  out_file_path = get_output_file_path(file_path)
  # remove the file if it's there to prevent a pandas.read_csv glitch
  try:
    os.remove(out_file_path)
  except FileNotFoundError:
    pass
  with open(out_file_path, 'a', encoding='utf8') as f:
    f.write(file_str)


if __name__ == '__main__':
  print('starting')
  remove_non_utf_8_chars('../tennis_MatchChartingProject/charting-m-points.csv')
  remove_non_utf_8_chars('../tennis_MatchChartingProject/charting-m-points.csv')
  print('done')

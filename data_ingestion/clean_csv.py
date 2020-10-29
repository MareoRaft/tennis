import os

def read_file_omitting_utf_8_chars(file_path):
  file_str = open(file_path, 'r', encoding='utf8', errors='ignore').read()
  return file_str


if __name__ == '__main__':
  print('starting')
  read_file_omitting_utf_8_chars('../data/charting-m-points.csv')
  read_file_omitting_utf_8_chars('../data/charting-w-points.csv')
  print('done')

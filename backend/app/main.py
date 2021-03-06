# builtin imports
import os

# 3rd party imports
import flask
from flask import Flask, request, redirect, send_from_directory, jsonify
from flask_cors import CORS

# local imports
import main_pagerank
import main_generic_query


# Create the app
app = Flask(__name__)
# CORS(app, origins=[
#   '/', # <-- maybe origin missing?
#   'http://localhost:80',
#   'http://localhost:5001',
#   'http://localhost:5001/',
#   'http://localhost:5000',
#   'http://162.243.168.182:80',
#   'http://162.243.168.182:5001',
#   'http://73.194.96.176:80',
#   'http://73.194.96.176:5001',
# ])
CORS(app, resources={
  r"*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"},
  r"/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"},
  r"/data*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"},
  r"/data/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"},
})


# Define the routes
@app.route('/data')
def index():
  # get url params
  gender = flask.request.args.get('gender', default='m')
  stat = flask.request.args.get('stat', default='pagerank')
  normalization = flask.request.args.get('normalization', default='percent')
  print('normalization:', normalization)
  reverse = bool('true' == flask.request.args.get('reverse', default='false'))
  limit = int(flask.request.args.get('limit', default=10))
  app.logger.info(f'got limit: {limit}')
  # compute everything
  if stat == 'pagerank':
    frontend_data = main_pagerank.main(gender, limit)
  else:
    frontend_data = main_generic_query.main(gender, stat, normalization, reverse, limit, verbose=True)
  return jsonify(frontend_data)



# Main execution loop
# gunicorn doesn't run this.  it grabs the app var and runs/hosts it itself
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80, debug=True)

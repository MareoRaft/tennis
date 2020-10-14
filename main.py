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
CORS(app, origins=[
  'http://localhost:5001',
  'http://learnnation.org',
])


# Define the routes
@app.route('/')
def index():
  # get url params
  stat = flask.request.args.get('stat', default='pagerank')
  normalization = flask.request.args.get('normalization', default='%')
  limit = int(flask.request.args.get('limit', default=10))
  app.logger.info(f'got limit: {limit}')
  # compute everything
  if stat == 'pagerank':
    frontend_data = main_pagerank.main(limit)
  else:
    frontend_data = main_generic_query.main(stat, normalization, limit)
  return jsonify(frontend_data)



# Main execution loop
# gunicorn doesn't run this.  it grabs the app var and runs/hosts it itself
if __name__ == '__main__':
  # port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=5000, debug=True)

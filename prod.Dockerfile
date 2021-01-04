# base image
# We use alpine because it's slimmer and we pin down the specific commit for future-proofing
FROM tiangolo/uwsgi-nginx-flask:python3.8-2020-12-19

# install deps
RUN pip3 install ediblepickle==1.1.3
# RUN pip3 install flask==1.1.2 # pre-installed on tiangolo/uwsgi-nginx-flask
RUN pip3 install flask-cors==3.0.9
RUN pip3 install numpy==1.19.2
RUN pip3 install scipy==1.5.2
RUN pip3 install pandas==1.1.2
RUN pip3 install networkx==2.5

# pull in files for deployment
COPY ./app /app

# Note that there is no CMD to run because the CMD set in the base image is what we already wanted.  As long as the Flask app is called `app`, the python file is named `main.py`, the parent directory is named `app`, and that same directory gets copied into `/app`, then the base image is designed to make our app work out-of-the-box.

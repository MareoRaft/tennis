# base image
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

# modify nginx config to allow CORS
# echo -e "server {\n    listen 80;\n    location / {\n        try_files \$uri @app;\n    }\n    location @app {\n           include uwsgi_params;\n        uwsgi_pass unix:///tmp/uwsgi.sock;\n    }\n    location /static {\n        alias /app/static;\n    }\n}\n" > /etc/nginx/conf.d/nginx.conf
# COPY dummy.txt /app/.
# COPY nginx.conf /etc/nginx/conf.d/.
# COPY dummy.txt /app/nginx.conf
# echo -e "server {\n    listen 80;\n    location / {\n        add_header Access-Control-Allow-Origin *;\n        try_files \$uri @app;\n    }\n    location @app {\n        add_header Access-Control-Allow-Origin *;\n        include uwsgi_params;\n        uwsgi_pass unix:///tmp/uwsgi.sock;\n    }\n    location /static {\n        alias /app/static;\n    }\n}\n" > /etc/nginx/conf.d/nginx.conf

# Note that there is no CMD to run because the CMD set in the base image is what we already wanted.  As long as the Flask app is called `app`, the python file is named `main.py`, the parent directory is named `app`, and that same directory gets copied into `/app`, then the base image is designed to make our app work out-of-the-box.
# CMD ["sleep", "999999"]

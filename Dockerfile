# base image
FROM jupyter/scipy-notebook

# install deps
RUN pip3 install ujson
RUN pip3 install pytest
RUN pip3 install ediblepickle==1.1.3
RUN pip3 install flask
RUN pip3 install flask-cors==3.0.9

# pull in files for deployment
COPY . /home/jovyan/work

# change CWD to the project dir
WORKDIR work

# program to run
CMD ["python3", "main.py"]

# base image
FROM python:3.8.6-buster

# change CWD to the project dir
WORKDIR /home/matt/work

# install deps
RUN pip3 install ediblepickle==1.1.3
RUN pip3 install flask==1.1.2
RUN pip3 install flask-cors==3.0.9
RUN pip3 install numpy==1.19.2
RUN pip3 install scipy==1.5.2
RUN pip3 install pandas==1.1.2
RUN pip3 install networkx==2.5

# pull in files for deployment
COPY . .

# program to run
CMD ["python3", "main.py"]

# base image
FROM jupyter/scipy-notebook

# install deps
RUN pip3 install ujson
RUN pip3 install pytest
RUN pip3 install ediblepickle

# program to run
CMD ["sleep", "99999"]

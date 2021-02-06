NOT IN USE

# latest node LTS (last updated 2020-10-16)
FROM node:12.19.0

# set working directory
WORKDIR /home/node/app

# add `myapp/node_modules/.bin` to PATH
ENV PATH /home/node/app/node_modules/.bin:$PATH

# install deps
COPY package.json .
COPY package-lock.json .
RUN npm install
# RUN npm install react-scripts@3.4.1 -g if it's a dev dep

# add app
# Do not COPY, use docker volumes instead

# start app
CMD ["npm", "run", "dev"]

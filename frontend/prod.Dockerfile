# BUILD ENVIRONMENT
FROM node:12.19.0 as build
WORKDIR /home/node/app
## install deps
ENV PATH /home/node/app/node_modules/.bin:$PATH
COPY package.json .
COPY package-lock.json .
RUN npm ci
RUN npm install react-scripts@3.4.3 -g
## build app
COPY . .
COPY ./src/prod.env.js ./src/env.js
RUN npm run build


# PRODUCTION ENVIRONMENT
FROM nginx:stable-alpine
## copy app over
COPY --from=build /home/node/app/build /usr/share/nginx/html
## serve with nginx
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

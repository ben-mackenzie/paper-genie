# base image
FROM node:11.12.0

# set working directory
RUN mkdir /app
WORKDIR /app

COPY package.json /app/
COPY package-lock.json /app/

RUN npm install
RUN npm install -g serve

COPY . /app

EXPOSE 5000

RUN npm run build

CMD ["serve", "-s", "build"]

FROM node:latest

WORKDIR /app
COPY package*.json ./

ENV CHOKIDAR_USEPOLLING=true

RUN npm install

COPY . .

EXPOSE 8080


CMD ["npm", "run", "serve"]
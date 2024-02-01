# frontend/Dockerfile
FROM node:latest

WORKDIR /app

COPY package*.json ./
RUN ls -ahl /app
RUN npm install && npm cache clean --force
RUN ls -ahl /app
COPY . .

CMD ["npm", "start"]
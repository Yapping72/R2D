# frontend/Dockerfile
FROM node:latest

WORKDIR /app

COPY package*.json ./
RUN npm install && npm cache clean --force
COPY . .
EXPOSE 5173 
# CMD ["npm", "run", "dev"]
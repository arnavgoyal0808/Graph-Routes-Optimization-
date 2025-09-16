FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --omit=dev        # install prod-only deps without needing a lock-file
COPY . .
EXPOSE 3000
CMD ["npm", "start"]

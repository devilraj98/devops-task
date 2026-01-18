FROM node:18-alpine

# Install libatomic
RUN apt-get update && apt-get install -y libatomic1 && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
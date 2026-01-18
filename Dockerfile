FROM node:18-alpine

# Install libatomict
RUN apk update && apk add --no-cache libatomic

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
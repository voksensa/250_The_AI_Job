FROM node:22-alpine

RUN apk add --no-cache curl

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source
COPY . .

# Build Next.js
RUN npm run build

EXPOSE 3000

# Run Next.js in production mode
CMD ["npm", "start"]

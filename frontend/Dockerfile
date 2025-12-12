# Use Node.js LTS (Version 20+)
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build not needed for dev, but good practice
# RUN npm run build

# Start Next.js in development mode
CMD ["npm", "run", "dev"]

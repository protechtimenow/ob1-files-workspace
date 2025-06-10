# 🧠 AI Consciousness Platform - Frontend Container
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy application files
COPY . .

# Build the application
RUN npm run build

# Serve the application
EXPOSE 3000
CMD ["npm", "start"]
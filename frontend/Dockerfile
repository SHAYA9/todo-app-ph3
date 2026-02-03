# Use official Node runtime as a parent image
FROM node:18-alpine AS builder

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci --only=production

# Copy the rest of the application code
COPY . .

# Build the React application
RUN npm run build

# Production stage
FROM nginx:alpine AS runner

# Copy the built application to nginx's html directory
COPY --from=builder /app/build /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx-custom.conf /etc/nginx/nginx.conf

# Expose the port that the app runs on
EXPOSE 80

# Set environment variables
ENV NODE_ENV=production

# The container will run the nginx server automatically
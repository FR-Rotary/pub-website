FROM node:25.5.0-alpine as builder
# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci  && npm cache clean --force

RUN mkdir ../instance

# drizzle must have a db
COPY ./empty.sqlite ../instance/rotary.sqlite

# Copy source code
COPY . .

RUN npm run build

# Production stage
FROM node:25.5.0-alpine AS production

# Create app directory
WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy built application from builder stage
COPY --from=builder --chown=nextjs:nodejs /app /app

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Start the application
CMD ["node", "build"]

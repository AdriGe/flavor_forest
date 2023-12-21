# Use a Node.js base image
FROM node:lts

# Set the working directory inside the container
WORKDIR /app

# Install project dependencies
# Note: Assumes package.json and package-lock.json are in .dockerignore
COPY package*.json ./
RUN npm install

# Expose port 8080 to access the server
EXPOSE 5173

# Start the app using the Vue CLI
CMD ["npm", "run", "serve"]

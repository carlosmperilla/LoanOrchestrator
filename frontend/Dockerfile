# Use the latest version of Node.js LTS
FROM node:lts

# Set the working directory to /app
WORKDIR /nuxt

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the files to the container
COPY . .

# Expose port 3000 for the server to listen on
EXPOSE 3000

# Start the server in development mode by default
CMD ["npm", "run", "dev"]

# Use a slim Node.js image as the base
FROM node:14-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./
COPY webpack.config.js ./

# Install project dependencies
RUN npm install

# Copy the rest of the project files to the container
COPY public /app/public
COPY src /app/src

# Build the React app
RUN npm run build

# Expose the port on which the app will run
EXPOSE 3030

# Set the command to start the app
CMD ["npm", "start"]

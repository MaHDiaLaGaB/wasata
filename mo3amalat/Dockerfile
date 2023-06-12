# Use the official Node.js 14 image as the base image
FROM node:14

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the working directory
COPY package*.json ./

# Install the application dependencies
RUN npm install

# Copy the application source code to the working directory
COPY src src
COPY index.js index.js


# Expose the port on which your application will run
EXPOSE 3000

# Specify the command to run your application
CMD ["node", "index.js"]

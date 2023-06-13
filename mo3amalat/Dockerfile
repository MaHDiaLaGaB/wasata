# Use the official Node.js 14 image as the base image
FROM node:14

# Copy the package.json and package-lock.json files to the working directory
COPY package.json package.json
COPY tsconfig.json tsconfig.json
COPY .env .env

# Install the application dependencies
RUN npm install

# Copy the application source code to the working directory
COPY src src

# Build the TypeScript code
RUN npm run build

# Expose the port on which your application will run
EXPOSE 3000

# Specify the command to run your application
CMD ["node", "dist/app.js"]

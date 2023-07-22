// webpack.config.js

module.exports = {
  // ... other webpack configuration options

  devServer: {
    // ... other devServer options

    host: '0.0.0.0',
    disableHostCheck: true,

    setupMiddlewares: (devServer) => {
      // Custom middlewares setup
      // ...

      // Call the original devServer middlewares setup
      devServer.app.use(devServer.middleware);
    },
  },
};
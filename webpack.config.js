const path = require("path");
const CopyWebpackPlugin = require("copy-webpack-plugin");

module.exports = {
  mode: "production",
  entry: {
    worker: "./extension/worker.js",
    content: "./extension/content.js",
  },
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "[name].js",
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
    ],
  },
  plugins: [
    new CopyWebpackPlugin({
      patterns: [{ from: "extension/manifest.json", to: "." }],
    }),
  ],
};

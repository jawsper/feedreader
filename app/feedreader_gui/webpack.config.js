var path = require("path");
var BundleTracker = require("webpack-bundle-tracker");
var MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
  context: __dirname,
  entry: path.resolve(__dirname, "assets/js/index"),
  output: {
    path: path.resolve(__dirname, "static"),
    filename: "[name]-[chunkhash].js",
    clean: true,
  },
  optimization: {
    splitChunks: {
      name: "vendor",
      chunks: "all",
    },
  },

  plugins: [
    new BundleTracker({
      filename: path.resolve(__dirname, "webpack-stats.json"),
    }),
    new MiniCssExtractPlugin({
      filename: "[name]-[chunkhash].css",
    }),
  ],

  resolve: {
    alias: {
      svelte: path.resolve("node_modules", "svelte"),
    },
    extensions: [".mjs", ".js", ".svelte"],
    mainFields: ["svelte", "browser", "module", "main"],
  },

  module: {
    rules: [
      {
        test: /\.(sa|sc|c)ss$/,
        use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"],
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: "asset/resource",
        generator: {
          filename: "images/[hash][ext][query]",
        },
      },
      {
        test: /\.(html|svelte)$/,
        use: {
          loader: "svelte-loader",
          options: {
            compilerOptions: {
              hydratable: true,
            },
          },
        },
      },
      {
        // required to prevent errors from Svelte on Webpack 5+, omit on Webpack 4
        test: /node_modules\/svelte\/.*\.mjs$/,
        resolve: {
          fullySpecified: false,
        },
      },
    ],
  },
};

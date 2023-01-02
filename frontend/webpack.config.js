module.exports = {
  module: {
    rules: [
      {
        test: /\.s[ac]ss$/i,
        use: [
          // ...
          {
            loader: "sass-loader",
            options: {
              sourceMap: true,
              sassOptions: {
                quietDeps: ["node_modules/bootstrap/**/*.scss"],
              }
            }
          }
        ]
      }
    ]
  }
};
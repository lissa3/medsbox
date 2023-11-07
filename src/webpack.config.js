const path = require('path');

module.exports = {
    entry: './assets/scripts/index.js',
    output: {
        'path': path.resolve(__dirname, 'static'),
        'filename': 'app.bundle.js'
    },
    mode: 'production',
    module:{
        rules:[
         {
             test:/\.css$/i,
             use:["style-loader","css-loader"]
         },
        //  {test:/\.scss$/i,
        //  use:["style-loader","css-loader"]}

        ]
     },
     optimization: {
        splitChunks: {
          chunks: 'async',
          minSize: 20000,
          minRemainingSize: 0,
          minChunks: 1,
          maxAsyncRequests: 30,
          maxInitialRequests: 30,
          enforceSizeThreshold: 50000,
          cacheGroups: {
            defaultVendors: {
              test: /[\\/]node_modules[\\/]/,
              priority: -10,
              reuseExistingChunk: true,
            },
            default: {
              minChunks: 2,
              priority: -20,
              reuseExistingChunk: true,
            },
          },
        },
      },
}
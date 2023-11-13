const path = require('path');

module.exports = {
    entry: './src/assets/scripts/index.js',
    output: {
        'path': path.resolve(__dirname, 'src', 'static','wbron'),
        'filename': '[name].bundle.js'
    },
    module:{
        rules:[
         {
             test:/\.css$/i,
             use:["style-loader","css-loader"]
         },


        ]
     },
     optimization: {
        minimize: true
    }



    // optimization: {
    //     splitChunks: {
    //       maxSize: 250000,
    //       chunks: 'all'
    //     }
    //   }
}
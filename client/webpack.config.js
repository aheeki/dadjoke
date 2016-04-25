var webpack = require('webpack');
var path = require('path');
var commonsPlugin = new webpack.optimize.CommonsChunkPlugin('common.js');

module.exports = {
  entry: {
    entry: './src/index.js'
  },
  output: {
    path: '/bundle/',
    publicPath: '/bundle/',
    filename: '[name].js'    
  },
  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        include: [ path.resolve(__dirname, "src") ],
        exclude: /(node_modules|bower_components)/,
        loader: 'babel',
        query: {
          plugins: ['transform-runtime'],
          presets: ['es2015', 'stage-0', 'react']
        }
      },
      { test: /\.less$/, loader: 'style-loader!css-loader!less-loader' },
      { test: /\.css$/, loader: "style!css" },
      { test: /\.(png|jpg)$/, loader: 'url-loader?limit=8192'}
    ]
  },
  plugins: [
    commonsPlugin,
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': '"development"'
    })
  ],
  resolve: {
    extensions: ['', '.js', '.json', '.less']
  }
};
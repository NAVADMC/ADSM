var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var CommonsChunkPlugin = require('webpack/lib/optimize/CommonsChunkPlugin');

module.exports = {
    context: __dirname,

    devtool: 'source-map',

    entry: {
        react_entry_point: './ADSM/static/js/react_entry_point',
    },

    output: {
        path: path.resolve('./ADSM/static/bundles/'),
        filename: "[name].js",
        chunkFilename: "[name].chunk[id].js"
    },

    plugins: [
        new webpack.optimize.OccurenceOrderPlugin(),
        new webpack.DefinePlugin({
            'process.env': {
                'NODE_ENV': JSON.stringify('production')
            }
        }),
        new webpack.optimize.UglifyJsPlugin({
            compressor: {
                warnings: false
            }
        }),
        new BundleTracker({filename: './webpack-stats.json'}),
        new CommonsChunkPlugin("commons.js")
    ],

    module: {
        loaders: [
            { test: /\.jsx?$/, exclude: /node_modules/, loader: 'babel-loader', query: {presets:['es2015', 'react']}}, // to transform JSX into JS
            { test: /\.css$/, loader: "style-loader!css-loader" },
            { test: /\.json$/, loader: "json-loader" }
        ]
    },

    resolve: {
        modulesDirectories: ['node_modules', 'bower_components'],
        extensions: ['', '.js', '.jsx']
    }
};
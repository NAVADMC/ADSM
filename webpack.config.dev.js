var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var CommonsChunkPlugin = require('webpack/lib/optimize/CommonsChunkPlugin');

module.exports = {
    context: __dirname,

    devtool: 'cheap-module-eval-source-map',

    entry: {
        population_panel_status: './ADSM/static/js/population-panel-status',
        assign_spread_widget:  './ADSM/static/js/assign_spread_widget'
    },

    output: {
        path: path.resolve('./ADSM/static/bundles/'),
        filename: "[name].js",
        chunkFilename: "[name].chunk[id].js"
    },

    plugins: [
        new webpack.DefinePlugin({
            'process.env': {
                'NODE_ENV': JSON.stringify('development')
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
var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var CommonsChunkPlugin = require('webpack/lib/optimize/CommonsChunkPlugin');

module.exports = {
    context: __dirname,

    entry: {
        population_panel_status: './ADSM/static/js/population-panel-status'
    },

    output: {
        path: path.resolve('./ADSM/static/bundles/'),
        filename: "[name].js",
        chunkFilename: "[name].chunk[id].js"
    },

    plugins: [
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
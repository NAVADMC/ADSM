'use strict';

var $ = require('jquery');
var React = require('react');

var TestApp = React.createClass({
    getInitialState: function(){
        return {clicked:false};
    },
    onClick: function(){
        this.setState({clicked: !this.state.clicked});
    },
    render: function() {
        var content = this.state.clicked ? "Clicked" :"React test!";
        return (
            <div className="page">
                <h1 onClick={this.onClick}>{content}</h1>
            </div>
        );
    }
});

React.render(
    React.createElement(TestApp, null),
    document.getElementById('content')
);
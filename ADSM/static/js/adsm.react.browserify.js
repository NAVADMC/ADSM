'use strict';

var $ = require('jquery');
var React = require('react');
var ReactDOM = require('react-dom');

/** using jQuery to always pass the CSRF token Cookie
* */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});



var genericAjaxGet = function() {
    $.ajax({
        url: this.props.url,
        dataType: 'json',
        cache: false,
        success: function (data) {
            this.setState({data: data.results});  // This is dropping extra info from the API (count, next, previous...)
        }.bind(this),
        error: function (xhr, status, err) {
            console.error(this.props.url, status, err.toString());
        }.bind(this)
    });
};

var ModelInstance = React.createClass({
    getInitialState: function() {
        return {editing: false};
    },
    submitEditedModel: function(form){
        this.props.instance.name = form.name;
        this.props.instance.number = form.number;
        this.setState({editing: false}); //set back to display state unless there was an error

        this.props.onModelEdit(this.props.instance);

    },
    becomeEditable: function(event){
        this.setState({editing: true});
    },
    deleteModel: function(){
        this.props.onModelDelete(this.props.instance);
    },
    render: function() {
        if(this.state.editing){
            return (
                <ModelForm onModelCreation={this.submitEditedModel} {...this.props.instance}/>
            );
        }else{
            return (
                <div className="list-group-item">
                    <div className="small-title">
                        {this.props.instance.name}
                    </div>
                    <div>{this.props.instance.number}</div>
                    <a href="#" onClick={this.becomeEditable}><i className="glyphicon glyphicon-pencil icon"></i></a>
                    <button onClick={this.deleteModel}>Delete</button>
                </div>
            );
        }
    }
});

// tutorial2.js
var ModelList = React.createClass({
    render: function() {
        var self = this;
        var instanceNodes = this.props.data.map(function (instance) {
            return (
                <ModelInstance instance={instance} onModelEdit={self.props.onModelEdit} onModelDelete={self.props.onModelDelete}>
                </ModelInstance>
            );
        });
        return (
            <div className="model-list">
                {instanceNodes}
            </div>
        );
    }
});

var ModelForm = React.createClass({
    getDefaultProps: function(){
        return {name: '',
                number: ''}
    },
    handleCreation: function(event) {
        event.preventDefault();
        var name = this.refs.name.value.trim();
        var number = this.refs.number.value.trim();
        if (!number && !name) {
            return;
        }
        // send request to the server
        this.props.onModelCreation({name: name, number: number});

        this.refs.name.value = '';
        this.refs.number.value = '';
        return;
    },
    render: function() {
        return (
            <form className="model-form form-inline" onSubmit={this.handleCreation}>
                <div className="form-group">
                    <label htmlFor="name"> Name: </label>
                    <input type="text" ref="name" defaultValue={this.props.name} className="form-control"/>
                </div>
                <div className="form-group">
                    <label htmlFor="name"> Number: </label>
                    <input type="text" ref="number" defaultValue={this.props.number} className="form-control"/>
                </div>
                <input type="submit" value="Save" />
            </form>
        );
    }
});

var ModelBox = React.createClass({
    getInitialState: function() {
        return {data: []};
    },
    componentDidMount: genericAjaxGet,
    handleModelCreation: function(model) {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            type: 'POST',
            data: model,
            success: function(data) {
                //Concat Update State:
                var temp = this.state.data;
                var newState = temp.concat([data]);
                this.setState({data: newState});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    handleModelEdit: function(model) {
        $.ajax({
            url: model.url,
            dataType: 'json',
            type: 'PUT',
            data: model,
            success: function(data) {
                //TODO: find the old one and change it somehow
                //this.setState({data: data});
                //This is currently handled inside the Model instance using an optimistic update
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    handleModelDelete: function(model) {
        $.ajax({
            url: model.url,
            dataType: 'json',
            type: 'DELETE',
            data: {},
            success: function() {
                //Find the old entry and delete it:
                var temp = this.state.data;
                var newState = temp.filter(function(element){return element.url != model.url});
                this.setState({data: newState});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    render: function() {
        return (
            <div className="model-box">
                <h1>{this.props.title}</h1>
                <ModelList data={this.state.data} onModelEdit={this.handleModelEdit} onModelDelete={this.handleModelDelete}/>
                <ModelForm onModelCreation={this.handleModelCreation}/>
            </div>
        );
    }
});



var TestApp = React.createClass({
    render: function() {
        return (
            <div className="page">
                <h1>PRS Web Portal</h1>
                <ModelBox url="/api/TestModels/" title="People" />
            </div>
        );
    }
});

ReactDOM.render(
    React.createElement(TestApp, null),
    document.getElementById('content')
);

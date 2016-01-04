/**
 * Created by josiah on 1/4/2016.
 */
import React, { Component, PropTypes } from 'react';

export default class SpreadAssigner extends Component {

    render(){
        return(
            <p>{JSON.stringify(this.props.input)}</p>
        )
    }
}
/**
 * Created by josiah on 12/31/2015.
 */

import React, { Component, PropTypes } from 'react';
import { get_population_status } from '../actions/actions';
import {dispatch} from '../GlobalStore'
import {ActionTypes} from '../actions/ActionTypes'


export default class NewPTCombinationButton extends Component {

    onClick(event){
        event.preventDefault()
        dispatch({
            type: ActionTypes.ADD_COMBINATION_INPUT,
            spread_type: this.props.spread_type,
            spread_pk: this.props.spread_pk
        })
        open_population_panel(); //from adsm.js
    }

    render() {
        return(
            <li className="addNew">
                <a className="action_link" onClick={this.onClick.bind(this)} href="#"><i> + Add New Source</i></a>
            </li>
        )
    }
}

NewPTCombinationButton.propTypes = {
    spread_type: PropTypes.string.isRequired,
    spread_pk: PropTypes.string.isRequired
};

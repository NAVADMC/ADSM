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
            new_input: {
                source:'source here',//TODO: check for duplicated "source" selections
                destinations: ['d1', 'd2']
            }
        })
        //TODO: where do the options come from?  Maybe a dummy input used as a template?  Maybe
    }

    render() {
        return(
            <li className="addNew">
                <a className="action_link" onClick={this.onClick.bind(this)}><i> + Create New Combination</i></a>
            </li>
        )
    }
}

NewPTCombinationButton.propTypes = {
    spread_type: PropTypes.string.isRequired,
    spread_inputs: PropTypes.array.isRequired
};

import React from 'react';
import $ from 'jquery'
import { store } from '../GlobalStore'
import {ActionTypes} from './ActionTypes'


export function get_population_status() {
    return function(dispatch){
        dispatch({type: ActionTypes.GET_POPULATION_STATUS});

        var url = '/setup/PopulationPanelStatus.json/';

        var jsPromise = Promise.resolve($.ajax({
            url: url,
            dataType: 'json',
            type: 'GET'
        }));

        jsPromise.then(
            function(json) {  // success
                dispatch({type: ActionTypes.RECEIVE_POPULATION_STATUS, population: json})
            },
            function(error) {  // failure
                    console.error(url, error);
            }
        )
    }
}

/** Could possibly be combined with get_population_status
 */
export function refresh_spread_inputs_from_server(){
    return function(dispatch){
        var url = '/setup/SpreadInputs.json/';

        var jsPromise = Promise.resolve($.ajax({
            url: url,
            dataType: 'json',
            type: 'GET'
        }));

        jsPromise.then(
            function(json) {  // success
                dispatch({type: ActionTypes.RECEIVE_SPREAD_INPUTS, response: json})
            },
            function(error) {  // failure
                    console.error(url, error);
            }
        )
    }
}

export function select_value_changed(spread_type, pk, field_name, new_value){
    return function(dispatch){
        dispatch({type: ActionTypes.SELECT_VALUE_CHANGED,
        spread_type,
        pk,
        field_name,
        new_value})
    }

}
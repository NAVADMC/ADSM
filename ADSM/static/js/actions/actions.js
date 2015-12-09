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

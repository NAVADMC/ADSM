import React from 'react';
import $ from 'jquery'
import { store } from '../GlobalStore'
import {ActionTypes} from './ActionTypes'


/** Boiler plate for initializing from the server:
 * get_population_status, refresh_spread_inputs_from_server, refresh_spread_inputs_from_server, refresh_disease_spread
 */
function refresh_from_server(dispatch, url, actionType){
    Promise.resolve($.ajax({
        url: url,
        dataType: 'json',
        type: 'GET'
    })).then(
        function(json) {  // success
            dispatch({type: actionType, response: json})
        },
        function(error) {  // failure
                console.error(url, error);
        }
    )
}

export function get_population_status() {
    return function(dispatch){
        refresh_from_server(dispatch, '/setup/PopulationPanelStatus.json/', ActionTypes.RECEIVE_POPULATION_STATUS);
    }
}

export function refresh_spread_inputs_from_server(){
    return function(dispatch){
        refresh_from_server(dispatch, '/setup/SpreadInputs.json/', ActionTypes.RECEIVE_SPREAD_INPUTS);
    }
}

export function refresh_disease_spread(){
    return function(dispatch){
        refresh_from_server(dispatch, '/setup/DiseaseSpreadAssignments.json/', ActionTypes.RECEIVE_DISEASE_SPREAD);
    }
}

export function refresh_spread_options(){
    return function(dispatch){
        refresh_from_server(dispatch, '/setup/SpreadOptions.json/', ActionTypes.RECEIVE_SPREAD_OPTIONS);
    }
}




function exclude(container, exclusion){
    return container.filter(function(x) {
        return exclusion.indexOf(x) < 0
    })
}

export function select_value_changed(spread_type, pk, input_index, field_name, new_value, old_value){
    return function(dispatch){
        dispatch({type: ActionTypes.SELECT_VALUE_CHANGED,
            spread_type,
            pk,
            field_name,
            new_value,
            old_value
        })
        if(field_name == 'source'){
            if(new_value.source && new_value.destinations.length == 0){
                //intermediate case where the destination hasn't been filled in yet.
                //update the widget but don't tell the server
                dispatch({type: ActionTypes.SET_SOURCE_ON_NEW_SPREAD, spread_type, spread_pk: pk, input_index, new_input: new_value})
                //don't do any other modifications beyond this point because destinations is not yet set to valid
            }else{
                //deleting old values is STILL necessary, even when new_value.source is not null or 0
                var delete_old = Promise.resolve($.ajax({
                    url: '/setup/ModifySpreadAssignments/',
                    dataType: 'json',
                    type: 'POST',
                    data: {
                        action: 'DELETE', spread_type, pk,
                        source: old_value.source,
                        destinations: old_value.destinations
                    }
                }));
                //delete_old.then( // we really only need to update the state once, which is done on create_new
                //    function(json){/* success*/dispatch({type: ActionTypes.RECEIVE_SPREAD_INPUTS, response: json}) }
                //)
                var create_new = Promise.resolve($.ajax({
                    url: '/setup/ModifySpreadAssignments/',
                    dataType: 'json',
                    type: 'POST',
                    data: {action: 'POST', spread_type, pk,
                        source: new_value.source,
                        destinations: new_value.destinations}
                }));
                create_new.then(
                    function(json){/* success*/dispatch({type: ActionTypes.RECEIVE_SPREAD_INPUTS, response: json}) }
                )
            }
        }
        if(field_name == 'destinations'){
            var deletions = exclude(old_value.destinations, new_value.destinations)
            var additions = exclude(new_value.destinations, old_value.destinations)
            if(deletions.length > 0){
                Promise.resolve($.ajax({
                    url: '/setup/ModifySpreadAssignments/',
                    dataType: 'json',
                    type: 'POST',
                    data: {action: 'DELETE', spread_type, pk,
                        source: old_value.source,//presumably old and new 'source' values are the same here
                        destinations: deletions}
                }))
                    .then(
                    function(json){/* success*/
                        if(additions.length == 0){//make sure that the values get updated if there's no additions
                            dispatch({type: ActionTypes.RECEIVE_SPREAD_INPUTS, response: json})
                        }}
                )
            }
            if(additions.length > 0){
                Promise.resolve($.ajax({
                    url: '/setup/ModifySpreadAssignments/',
                    dataType: 'json',
                    type: 'POST',
                    data: {action: 'POST', spread_type, pk,
                        source: new_value.source,//presumably old and new 'source' values are the same here
                        destinations: additions}
                })).then(
                    function(json){/* success*/dispatch({type: ActionTypes.RECEIVE_SPREAD_INPUTS, response: json}) }
                )
            }
        }
    }
}


import { combineReducers } from 'redux'
import { ActionTypes } from '../actions/ActionTypes'
import $ from 'jquery'


export function population(population=[], action){
    switch(action.type ){
        case ActionTypes.RECEIVE_POPULATION_STATUS: {
            return action.population
        }

        default:
            return population
    }
}

export function disease_spread(disease_spread={}, action){
    switch(action.type ){
        case ActionTypes.RECEIVE_DISEASE_SPREAD: {
            return action.response  // clobbers the entire data structure
        }

        default:
            return disease_spread
    }
}

var STARTING_INPUTS = {
    DirectSpread: {},
    IndirectSpread: {},
    AirborneSpread: {}
}
export function spread_inputs(spread_inputs=STARTING_INPUTS, action){
    switch(action.type ){
        case ActionTypes.ADD_COMBINATION_INPUT: {
            var prev_inputs = spread_inputs[action.spread_type][action.spread_pk] || []
            var new_inputs = [
                ...prev_inputs,
                {//new_input:
                    source:'',//TODO: check for duplicated "source" selections
                    destinations: []
                }
            ];
            var modified_list = Object.assign({}, spread_inputs)
            modified_list[action.spread_type][action.spread_pk] = new_inputs
            return modified_list
        }
        case ActionTypes.RECEIVE_SPREAD_INPUTS: {
            return action.response  //clobbers data that disagrees with server
        }
        case ActionTypes.SET_SOURCE_ON_NEW_SPREAD: {
            var modified_list = Object.assign({}, spread_inputs)
            modified_list[action.spread_type][action.spread_pk][action.input_index] = action.new_input
            return modified_list
        }
        default:
            return spread_inputs
    }
}


export default combineReducers({
    population,
    disease_spread,
    spread_inputs
})
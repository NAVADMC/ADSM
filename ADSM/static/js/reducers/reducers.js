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

export function spread_inputs(spread_inputs=[], action){
    switch(action.type ){
        case ActionTypes.ADD_COMBINATION_INPUT: {
            var tmp = [
                ...spread_inputs,
                action.new_input
            ];
            return tmp
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
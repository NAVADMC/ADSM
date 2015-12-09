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


export default combineReducers({
    population
})
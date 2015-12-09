import { combineReducers } from 'redux'
import { ActionTypes } from '../actions/ActionTypes'
import $ from 'jquery'


export function base(initial={}, action){
    switch(action.type ){
        default:
            return initial
    }
}


export default combineReducers({
    base
})
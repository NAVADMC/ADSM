import React from 'react';
import $ from 'jquery'
import { store } from '../GlobalStore'
import {ActionTypes} from './ActionTypes'


export function none_action() {
    return {type:ActionTypes.NONE}
}

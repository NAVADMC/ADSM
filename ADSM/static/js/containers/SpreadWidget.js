/**
 * Created by josiah on 12/31/2015.
 */
import $ from 'jquery';
import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import { get_population_status } from '../actions/actions';
import {store} from '../GlobalStore'
import { DevTools, DebugPanel, LogMonitor } from 'redux-devtools/lib/react';
import DiffMonitor from 'redux-devtools-diff-monitor';



export default class SpreadWidget extends Component {

    render() {
        var debug_panel = ''
        if (process.env.NODE_ENV === 'development') {
            debug_panel = <DebugPanel top right bottom><DevTools store={store} monitor={DiffMonitor} visibleOnLoad={true} /></DebugPanel>
        }

        return (
            <div>
                <h1>React Wins!</h1>
                { debug_panel }
            </div>

        );

    }
}
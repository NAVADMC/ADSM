/**
 * Created by josiah on 12/31/2015.
 */
import $ from 'jquery';
import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import {store} from '../GlobalStore'
import { DevTools, DebugPanel, LogMonitor } from 'redux-devtools/lib/react';
import DiffMonitor from 'redux-devtools-diff-monitor';
import NewPTCombinationButton from './NewPTCombinationButton'



export class SpreadWidget extends Component {

    render() {
        var debug_panel = ''
        if (process.env.NODE_ENV === 'development') {
            debug_panel = <DebugPanel top right bottom><DevTools store={store} monitor={DiffMonitor} visibleOnLoad={true} /></DebugPanel>
        }
        var inputs = []
        this.props.spread_inputs.map(function(input, index){
            return <p key={index}>{Object.toString(input)}</p>
        });
        return (
            <div className="spread-widget-contents">
                <h1>React Wins!</h1>
                <p>{window.location.pathname}</p>
                {inputs}
                <NewPTCombinationButton spread_inputs={this.props.spread_inputs}/>
                { debug_panel }
            </div>

        );
    }
}


/*disease_spread is the main data structure that drives everything.
* It is a 2D array of cells that each contain {IndirectSpread:pk, DirectSpread: pk, AirborneSpread:pk}
* in them.  The Array is indexed by the Production Type name, rather than a numerical index, so we use Objects
* (python dictionaries) instead of Array[].  Rows are source production types and Columns are destination Production
* Types.  */
SpreadWidget.propTypes = {
    disease_spread: PropTypes.objectOf(
        //sheep: {pk: 3, desinations: {...}
        PropTypes.shape({
            pk: PropTypes.number.isRequired,
            destinations: PropTypes.objectOf(
                //cow: {"IndirectSpread": 2, "DirectSpread": 5, AirborneSpread: null }
                PropTypes.shape({
                    IndirectSpread: PropTypes.number,  //not required, may be null
                    DirectSpread: PropTypes.number,
                    AirborneSpread: PropTypes.number
                })
            ).isRequired
        })
    ).isRequired
};


function select(state) {
    return {
        disease_spread: state.disease_spread,
        spread_inputs: state.spread_inputs
    }
}

// Wrap the component to inject dispatch and state into it
export default connect(select)(SpreadWidget)

'use strict';

/**
 * Created by josiah on 12/31/2015.
 */
import $ from 'jquery';
import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import {refresh_spread_inputs_from_server} from '../actions/actions'
import {store} from '../GlobalStore'
import NewPTCombinationButton from './NewPTCombinationButton'
import SpreadAssigner from './SpreadAssigner'



export class SpreadWidget extends Component {

    componentDidMount(){
        this.props.dispatch(refresh_spread_inputs_from_server())
    }

    // render function is called twice when a Disease Spread is selected.
    render() {
        var url = $('#center-panel form').first().attr('action').split('/');
        var spread_type = url[2];
        var pk = url[3];
        var {spread_inputs, population} = this.props;
        var inputs = [];
        var contains_bool = false;
        var next_key = "";
        var incomplete_rebuild = true;
        // this conditional DOES NOT run on the first pass. Fills in the type combinations
        if (pk in spread_inputs[spread_type] && typeof population !== 'undefined') {

            for (let i = 0; i < population.length; i++){
                contains_bool = false;
                for(let j = 0; j < spread_inputs[spread_type][pk].length; j++){
                    if(population[i]["pk"] == spread_inputs[spread_type][pk][j]["source"]){
                        contains_bool = true;
                    }
                }
                if(!contains_bool){
                    spread_inputs[spread_type][pk].push({"source": population[i]["pk"], "destinations": new Array()});
                }
            }

            spread_inputs[spread_type][pk].sort((a,b) => ((a.source > b.source) ? 1 : ((b.source > a.source) ? -1 : 0)));

            inputs = spread_inputs[spread_type][pk].map(function (input_state, index) {
                return (<SpreadAssigner population={population}
                                        input_state={input_state}
                                        spread_type={spread_type}
                                        pk={pk}
                                        index={index}
                                        key={index}/>);s
            });

            rebuild:
            while (incomplete_rebuild){
                for (let i = 0; i < spread_inputs[spread_type][pk].length; i++){
                    if(spread_inputs[spread_type][pk][i]["destinations"].length == 0) {
                        spread_inputs[spread_type][pk].splice(i, 1);
                        continue rebuild;
                    }
                }
                break;
            }
        }


        // the return of the first pass, sets up the actual space for the type combinations to go
        return (
            <div className="spread-widget-contents">
                    <hr/>
                    <h1>Production Type Combinations</h1>
                    <p>Sources without destinations are not used and only serve as placeholders.</p>
                    {inputs}
            </div>
        );
    }
}

var list_of_source_destination_pks =
    PropTypes.arrayOf(
        PropTypes.shape(
            {source: PropTypes.any/*number or ''*/, destination: PropTypes.array})
    );

SpreadWidget.propTypes = {
    spread_inputs: PropTypes.shape({
        DirectSpread: PropTypes.objectOf(list_of_source_destination_pks).isRequired,
        IndirectSpread: PropTypes.objectOf(list_of_source_destination_pks).isRequired,
        AirborneSpread: PropTypes.objectOf(list_of_source_destination_pks).isRequired
}).isRequired
};


function select(state) {
    return {
        spread_inputs: state.spread_inputs,
        population: state.population
    }
}

// Wrap the component to inject dispatch and state into it
export default connect(select)(SpreadWidget)

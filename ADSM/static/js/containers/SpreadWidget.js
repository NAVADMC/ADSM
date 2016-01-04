/**
 * Created by josiah on 12/31/2015.
 */
import $ from 'jquery';
import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import {store} from '../GlobalStore'
import NewPTCombinationButton from './NewPTCombinationButton'
import SpreadAssigner from './SpreadAssigner'



export class SpreadWidget extends Component {

    render() {
        var row = '' // row of disease_spread.  filter out rows that never mention this particular DiseaseSpread
        var inputs = this.props.spread_inputs.map(function(input, index){
            return (<SpreadAssigner source_info={row} input={input} key={index} />);
        });
        var spread_type = $('#center-panel form').first().attr('action').split('/')[2]
        return (
            <div className="spread-widget-contents">
                <hr/>
                <h1>Production Type Combinations</h1>
                {inputs}
                <NewPTCombinationButton spread_inputs={this.props.spread_inputs} spread_type={spread_type}/>
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
        spread_inputs: state.spread_inputs,
        population: state.population
    }
}

// Wrap the component to inject dispatch and state into it
export default connect(select)(SpreadWidget)

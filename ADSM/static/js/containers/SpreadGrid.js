/**
 * Created by josiah on 1/20/2016.
 */

import $ from 'jquery';
import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import {refresh_disease_spread} from '../actions/actions'
import {store} from '../GlobalStore'



export class SpreadGrid extends Component {

    componentDidMount(){
        this.props.dispatch(refresh_disease_spread())
    }

    render() {
        return (
            <div className="spread-grid-contents">
                <h1>Visualization of Disease Spread</h1>
            </div>

        );
    }
}


/*disease_spread is the main data structure that drives everything.
* It is a 2D array of cells that each contain {IndirectSpread:pk, DirectSpread: pk, AirborneSpread:pk}
* in them.  The Array is indexed by the Production Type name, rather than a numerical index, so we use Objects
* (python dictionaries) instead of Array[].  Rows are source production types and Columns are destination Production
* Types.  */
SpreadGrid.propTypes = {
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
    ).isRequired,
};


function select(state) {
    return {
        disease_spread: state.disease_spread,
        population: state.population
    }
}

// Wrap the component to inject dispatch and state into it
export default connect(select)(SpreadGrid)

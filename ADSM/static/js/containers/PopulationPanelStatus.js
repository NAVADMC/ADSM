import $ from 'jquery';
import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import ProductionTypeRow from './ProductionTypeRow'
import { get_population_status } from '../actions/actions';
import {store} from '../GlobalStore'


export class PopulationPanelStatus extends Component {
    componentDidMount(){
        this.props.dispatch(get_population_status())
    }

    render() {
        var rows = [];
        if(typeof this.props.population !== 'undefined'){
            rows = this.props.population.map(pt => <ProductionTypeRow {... pt} key={pt.name}/>);
        }
        return (
            <div>
                <h2><a href="/setup/ProductionType/">Population Production Types</a></h2>

                <ul id="ProductionTypes">
                    {rows}
                </ul>
            </div>
        );
    }
}


PopulationPanelStatus.propTypes = {
    population: PropTypes.arrayOf(PropTypes.shape({
        name: PropTypes.string.isRequired,
        unit_count: PropTypes.number.isRequired,
        progression: PropTypes.bool.isRequired,
        spread: PropTypes.bool.isRequired,
        control: PropTypes.bool.isRequired,
        zone: PropTypes.bool.isRequired
    }))
};


function select(state) {
    return {
        population: state.population
    }
}


// Wrap the component to inject dispatch and state into it
export default connect(select)(PopulationPanelStatus)

'use strict';

import $ from 'jquery';
import ReactDOM from 'react-dom'
import React, { Component, PropTypes } from 'react';
import { connect, Provider } from 'react-redux';
import {store} from './GlobalStore'
import { get_population_status } from './actions/actions';


class ProductionTypeRow extends Component {
    render() {
        var { name, unit_count, progression, spread, control, zone } = this.props;
        return(
            <li>
                <a href="#">{ name }</a>
                <span>({ unit_count } units)</span>
                <span className={progression ? 'green-dot on' : 'green-dot'} />
                <span className={spread ? 'green-dot on' : 'green-dot'} />
                <span className={control ? 'green-dot on' : 'green-dot'} />
                <span className={zone ? 'green-dot on' : 'green-dot'} />
            </li>
        )
    }
}


export class PopulationPanelStatus extends Component {
    componentDidMount(){
        this.props.dispatch(get_population_status())
    }

    render() {
        var rows = [];
        rows = this.props.population.map(pt => <ProductionTypeRow {... pt} />);
        
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
    })).isRequired
};


function select(state) {
    return {
        population: state.population
    }
}


// Wrap the component to inject dispatch and state into it
export default connect(select)(PopulationPanelStatus)


ReactDOM.render(
    <Provider store={store}>
        <PopulationPanelStatus />
    </Provider>,
    document.getElementById('population_panel_status')
);

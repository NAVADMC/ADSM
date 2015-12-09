'use strict';

import $ from 'jquery';
import React, { Component, PropTypes } from 'react';
import ReactDOM from 'react-dom';
import { connect, Provider } from 'react-redux';
import {store, dispatch} from './GlobalStore'
import { get_population_status } from './actions/actions';


export class PopulationPanelStatus extends Component {
    componentDidMount(){
        dispatch(get_population_status())
    }

    render() {
        return (
            <div className="page">
                <h1>"Hello"</h1>
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


ReactDOM.render(
    <Provider store={store}>
        <PopulationPanelStatus />
    </Provider>,
    document.getElementById('population_panel_status')
);
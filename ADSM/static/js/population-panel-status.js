'use strict';

import $ from 'jquery';
import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';


export class PopulationPanelStatus extends Component {
    render() {
        var content = this.state.clicked ? "Clicked" :"React test!";
        return (
            <div className="page">
                <h1 onClick={this.onClick}>{content}</h1>
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


React.render(
    React.createElement(PopulationPanelStatus, null),
    document.getElementById('population_panel_status')
);
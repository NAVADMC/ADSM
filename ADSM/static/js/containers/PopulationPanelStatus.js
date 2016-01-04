import $ from 'jquery';
import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import ProductionTypeRow from './ProductionTypeRow'
import { get_population_status } from '../actions/actions';
import {store} from '../GlobalStore'

import { DevTools, DebugPanel, LogMonitor } from 'redux-devtools/lib/react';
import DiffMonitor from 'redux-devtools-diff-monitor';


export class PopulationPanelStatus extends Component {
    componentDidMount(){
        this.props.dispatch(get_population_status())
    }

    render() {
        var debug_panel = ''
        if (process.env.NODE_ENV === 'development') {
            debug_panel = <DebugPanel top right bottom><DevTools store={store} monitor={DiffMonitor} visibleOnLoad={true} /></DebugPanel>
        }

        var rows = [];
        if(typeof this.props.population !== 'undefined'){
            rows = this.props.population.map(pt => <ProductionTypeRow {... pt} key={pt.name}/>);
        }
        return (
            <div>
                <h2>
                    <div className="population-super-column text-center">
                        <a href="/setup/ProductionType/">Population Production Types</a>
                    </div>
                    <div className="productiontypes-header progression-icon" ></div>
                    <div className="productiontypes-header spread-icon" ></div>
                    <div className="productiontypes-header control-icon" ></div>
                    <div className="productiontypes-header zone-icon" ></div>
                </h2>

                <ul id="ProductionTypes">
                    {rows}
                </ul>
                <div className="population-super-column text-center">
                    <a href="/setup/ProductionType/">+ define new production type</a>
                </div>

                { debug_panel }
            </div>
        );
    }
}


PopulationPanelStatus.propTypes = {
    population: PropTypes.arrayOf(PropTypes.shape({
        name: PropTypes.string.isRequired,
        unit_count: PropTypes.number.isRequired,
        progression: PropTypes.string,
        spread: PropTypes.number.isRequired,
        control: PropTypes.string,
        zone: PropTypes.string
    })).isRequired
};


function select(state) {
    return {
        population: state.population
    }
}


// Wrap the component to inject dispatch and state into it
export default connect(select)(PopulationPanelStatus)
